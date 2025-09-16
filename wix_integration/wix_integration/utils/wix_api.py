"""
Wix API Integration Module

This module handles the core integration with Wix API for creating and updating products.
It maps Frappe Item fields to Wix Product fields and handles all API communications.
"""

import frappe
import requests
import json
import traceback
from frappe import _
from frappe.utils import getdate, today, get_datetime

# Wix Site Configuration
WIX_SITES = {
    "dev": "63a7b738-6d1c-447a-849a-fab973366a06",
    "kokofresh": "a57521a4-3ecd-40b8-852c-462f2af558d2", 
    "byte_catalyst": "bc24ec89-d58d-4b00-9c00-997dc4bb2025"
}

# Default Wix site (can be configured)
DEFAULT_WIX_SITE = "dev"

def create_wix_product(doc, method=None):
    """
    Create a new product in Wix when a Frappe Item is created
    
    Args:
        doc: Frappe Item document
        method: Hook method (after_insert)
    """
    try:
        frappe.logger().info(f"Starting Wix product creation for Item: {doc.item_code}")
        
        # Skip if this item shouldn't be synced
        if not should_sync_item(doc):
            frappe.logger().info(f"Skipping Wix sync for Item: {doc.item_code}")
            return
            
        # Get Wix site ID (configurable)
        site_id = get_wix_site_id()
        
        # Map Frappe Item to Wix Product format
        wix_product_data = map_item_to_wix_product(doc)
        
        # Call Wix API to create product
        response = call_wix_create_product_api(site_id, wix_product_data)
        
        if response and response.get("success"):
            # Store the Wix product ID in the Frappe Item
            wix_product_id = response.get("product_id")
            store_wix_product_id(doc, wix_product_id)
            
            frappe.logger().info(f"Successfully created Wix product {wix_product_id} for Item {doc.item_code}")
            
            # Show success message to user
            frappe.msgprint(
                _(f"Product '{doc.item_name}' successfully synced to Wix!"),
                title=_("Wix Sync Success"),
                indicator="green"
            )
        else:
            error_msg = response.get("error", "Unknown error") if response else "No response from Wix API"
            handle_wix_api_error("create", doc.item_code, error_msg)
            
    except Exception as e:
        error_msg = f"Exception in create_wix_product: {str(e)}\\n{traceback.format_exc()}"
        frappe.log_error(
            message=error_msg,
            title=f"Wix Product Creation Failed - {doc.item_code}"
        )
        
        # Don't block the Item creation, just log the error
        frappe.logger().error(f"Failed to create Wix product for {doc.item_code}: {str(e)}")

def update_wix_product(doc, method=None):
    """
    Update existing Wix product when Frappe Item is updated
    
    Args:
        doc: Frappe Item document
        method: Hook method (on_update)
    """
    try:
        frappe.logger().info(f"Starting Wix product update for Item: {doc.item_code}")
        
        # Skip if this item shouldn't be synced
        if not should_sync_item(doc):
            return
            
        # Get the stored Wix product ID
        wix_product_id = get_wix_product_id(doc)
        if not wix_product_id:
            # If no Wix product ID exists, create a new product instead
            frappe.logger().info(f"No Wix product ID found for {doc.item_code}, creating new product")
            create_wix_product(doc, method)
            return
            
        # Get Wix site ID
        site_id = get_wix_site_id()
        
        # Map updated Frappe Item to Wix Product format
        wix_product_data = map_item_to_wix_product(doc)
        
        # Call Wix API to update product
        response = call_wix_update_product_api(site_id, wix_product_id, wix_product_data)
        
        if response and response.get("success"):
            frappe.logger().info(f"Successfully updated Wix product {wix_product_id} for Item {doc.item_code}")
        else:
            error_msg = response.get("error", "Unknown error") if response else "No response from Wix API"
            handle_wix_api_error("update", doc.item_code, error_msg)
            
    except Exception as e:
        error_msg = f"Exception in update_wix_product: {str(e)}\\n{traceback.format_exc()}"
        frappe.log_error(
            message=error_msg,
            title=f"Wix Product Update Failed - {doc.item_code}"
        )
        
        frappe.logger().error(f"Failed to update Wix product for {doc.item_code}: {str(e)}")

def should_sync_item(doc):
    """
    Determine if an Item should be synced to Wix
    
    Args:
        doc: Frappe Item document
        
    Returns:
        bool: True if item should be synced
    """
    # Skip if item is disabled
    if doc.disabled:
        return False
        
    # Skip if item is not for sale
    if not doc.is_sales_item:
        return False
        
    # Skip items without a standard rate
    if not doc.standard_rate or doc.standard_rate <= 0:
        return False
        
    # Add more conditions as needed
    return True

def map_item_to_wix_product(doc):
    """
    Map Frappe Item fields to Wix Product structure
    
    Args:
        doc: Frappe Item document
        
    Returns:
        dict: Wix Product data structure
    """
    # Build the basic product structure
    product_data = {
        "product": {
            "name": doc.item_name or doc.item_code,
            "slug": generate_product_slug(doc.item_code),
            "plainDescription": doc.description or "",
            "variantsInfo": {
                "variants": [
                    {
                        "sku": doc.item_code,
                        "price": {
                            "actualPrice": {
                                "amount": str(doc.standard_rate),
                                "currency": frappe.defaults.get_global_default("currency") or "USD"
                            }
                        },
                        "physicalProperties": {},
                        "stock": {
                            "trackInventory": True,
                            "inStock": True
                        }
                    }
                ]
            }
        }
    }
    
    # Add physical properties if available
    variant = product_data["product"]["variantsInfo"]["variants"][0]
    
    if doc.weight_per_unit:
        variant["physicalProperties"]["weight"] = {
            "value": doc.weight_per_unit,
            "unit": "kg"  # Default to kg, can be configurable
        }
    
    # Add inventory information
    if hasattr(doc, 'projected_qty') and doc.projected_qty:
        variant["stock"]["quantity"] = int(doc.projected_qty)
    
    return product_data

def generate_product_slug(item_code):
    """Generate a URL-friendly slug from item code"""
    import re
    slug = re.sub(r'[^a-zA-Z0-9-_]', '-', item_code.lower())
    slug = re.sub(r'-+', '-', slug).strip('-')
    return slug

def get_wix_site_id():
    """Get the configured Wix site ID"""
    # This can be made configurable via DocType settings
    return WIX_SITES.get(DEFAULT_WIX_SITE)

def call_wix_create_product_api(site_id, product_data):
    """
    Call Wix API to create a new product
    This is a placeholder - actual implementation depends on authentication method
    """
    try:
        # This would use either:
        # 1. Wix MCP integration (if available)
        # 2. Direct Wix REST API calls (requires API key/OAuth)
        # 3. Other authentication methods
        
        frappe.logger().info(f"Calling Wix Create Product API for site {site_id}")
        frappe.logger().debug(f"Product data: {json.dumps(product_data, indent=2)}")
        
        # Placeholder response - replace with actual API call
        return {
            "success": True,
            "product_id": f"wix_product_{frappe.generate_hash(length=8)}",
            "message": "Product created successfully"
        }
        
    except Exception as e:
        frappe.logger().error(f"Error calling Wix Create Product API: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def call_wix_update_product_api(site_id, product_id, product_data):
    """
    Call Wix API to update an existing product
    This is a placeholder - actual implementation depends on authentication method
    """
    try:
        frappe.logger().info(f"Calling Wix Update Product API for site {site_id}, product {product_id}")
        frappe.logger().debug(f"Product data: {json.dumps(product_data, indent=2)}")
        
        # Placeholder response - replace with actual API call
        return {
            "success": True,
            "product_id": product_id,
            "message": "Product updated successfully"
        }
        
    except Exception as e:
        frappe.logger().error(f"Error calling Wix Update Product API: {str(e)}")
        return {
            "success": False,
            "error": str(e)
        }

def store_wix_product_id(doc, wix_product_id):
    """Store the Wix product ID in the Frappe Item"""
    try:
        # Add custom field to Item if it doesn't exist
        if not frappe.db.exists("Custom Field", {"dt": "Item", "fieldname": "wix_product_id"}):
            create_wix_product_id_field()
            
        # Update the document with Wix product ID
        frappe.db.set_value("Item", doc.name, "wix_product_id", wix_product_id)
        frappe.db.commit()
        
    except Exception as e:
        frappe.logger().error(f"Error storing Wix product ID: {str(e)}")

def get_wix_product_id(doc):
    """Get the stored Wix product ID from Frappe Item"""
    try:
        return frappe.db.get_value("Item", doc.name, "wix_product_id")
    except:
        return None

def create_wix_product_id_field():
    """Create custom field to store Wix Product ID"""
    try:
        custom_field = frappe.get_doc({
            "doctype": "Custom Field",
            "dt": "Item",
            "fieldname": "wix_product_id",
            "label": "Wix Product ID",
            "fieldtype": "Data",
            "read_only": 1,
            "insert_after": "item_code",
            "description": "Wix Product ID for synced items"
        })
        custom_field.insert()
        frappe.db.commit()
        
    except Exception as e:
        frappe.logger().error(f"Error creating Wix Product ID field: {str(e)}")

def handle_wix_api_error(operation, item_code, error_msg):
    """Handle Wix API errors consistently"""
    frappe.log_error(
        message=f"Wix {operation} operation failed for Item {item_code}: {error_msg}",
        title=f"Wix {operation.capitalize()} Error"
    )
    
    frappe.msgprint(
        _(f"Failed to {operation} product in Wix. Please check the error log for details."),
        title=_("Wix Sync Error"),
        indicator="red"
    )
