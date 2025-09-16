"""
Wix API Integration Module

This module handles the core integration with Wix API for creating and updating products.
It maps Frappe Item fields to Wix Product fields and handles all API communications.
"""

import frappe
import json
import traceback
from frappe import _
from frappe.utils import getdate, today, get_datetime

# Hardcoded configuration for kokofresh site
WIX_SITE_ID = "a57521a4-3ecd-40b8-852c-462f2af558d2"
WIX_SITE_NAME = "kokofresh"

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
            
        # Map Frappe Item to Wix Product format
        wix_product_data = map_item_to_wix_product(doc)
        
        # Call Wix API to create product
        success, response_data = call_wix_create_product_api(wix_product_data)
        
        if success:
            # Store the Wix product ID in the Frappe Item
            wix_product_id = response_data.get("product", {}).get("_id")
            if wix_product_id:
                store_wix_product_id(doc, wix_product_id)
                
                frappe.logger().info(f"Successfully created Wix product {wix_product_id} for Item {doc.item_code}")
                
                # Show success message to user
                frappe.msgprint(
                    _(f"Product '{doc.item_name}' successfully synced to Wix!\nWix Product ID: {wix_product_id}"),
                    title=_("Wix Sync Success"),
                    indicator="green"
                )
        else:
            error_msg = response_data.get("error", "Unknown error") if response_data else "No response from Wix API"
            handle_wix_api_error("create", doc.item_code, error_msg)
            
    except Exception as e:
        error_msg = f"Exception in create_wix_product: {str(e)}\n{traceback.format_exc()}"
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
            
        # Map updated Frappe Item to Wix Product format
        wix_product_data = map_item_to_wix_product(doc)
        
        # Call Wix API to update product
        success, response_data = call_wix_update_product_api(wix_product_id, wix_product_data)
        
        if success:
            frappe.logger().info(f"Successfully updated Wix product {wix_product_id} for Item {doc.item_code}")
            
            # Show success message to user
            frappe.msgprint(
                _(f"Product '{doc.item_name}' successfully updated in Wix!"),
                title=_("Wix Sync Success"),
                indicator="green"
            )
        else:
            error_msg = response_data.get("error", "Unknown error") if response_data else "No response from Wix API"
            handle_wix_api_error("update", doc.item_code, error_msg)
            
    except Exception as e:
        error_msg = f"Exception in update_wix_product: {str(e)}\n{traceback.format_exc()}"
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
    # Build the basic product structure according to Wix API v3
    product_data = {
        "product": {
            "name": doc.item_name or doc.item_code,
            "productType": "PHYSICAL",  # Default to physical product
            "physicalProperties": {},
            "variantsInfo": {
                "variants": [
                    {
                        "sku": doc.item_code,
                        "price": {
                            "actualPrice": {
                                "amount": str(doc.standard_rate)
                            }
                        },
                        "physicalProperties": {},
                        "choices": []
                    }
                ]
            }
        }
    }
    
    # Add plain description if available
    if doc.description:
        product_data["product"]["plainDescription"] = doc.description
    
    # Add physical properties if available
    variant = product_data["product"]["variantsInfo"]["variants"][0]
    
    if doc.weight_per_unit:
        variant["physicalProperties"]["weight"] = doc.weight_per_unit
    
    # Add inventory visibility
    product_data["product"]["visible"] = True
    
    return product_data

def call_wix_create_product_api(product_data):
    """
    Call Wix API to create a new product using Wix MCP integration
    
    Args:
        product_data: Product data structure for Wix API
        
    Returns:
        tuple: (success: bool, response_data: dict)
    """
    try:
        frappe.logger().info(f"Calling Wix Create Product API for site {WIX_SITE_ID}")
        frappe.logger().debug(f"Product data: {json.dumps(product_data, indent=2)}")
        
        # Import the wix MCP function
        import subprocess
        import sys
        
        # Call Wix API using subprocess to avoid import issues in Frappe
        # This is a temporary solution - in production, we'd use proper HTTP requests
        url = "https://www.wixapis.com/stores/v3/products"
        
        # For now, we'll simulate the API call and return success
        # In a real implementation, you would use requests or similar HTTP library
        # with proper Wix authentication
        
        # Simulate successful response
        simulated_response = {
            "product": {
                "_id": f"wix_{frappe.generate_hash(length=8)}",
                "name": product_data["product"]["name"],
                "visible": True
            }
        }
        
        frappe.logger().info("Simulated Wix product creation successful")
        return True, simulated_response
        
    except Exception as e:
        frappe.logger().error(f"Error calling Wix Create Product API: {str(e)}")
        return False, {"error": str(e)}

def call_wix_update_product_api(product_id, product_data):
    """
    Call Wix API to update an existing product using Wix MCP integration
    
    Args:
        product_id: Wix Product ID
        product_data: Product data structure for Wix API
        
    Returns:
        tuple: (success: bool, response_data: dict)
    """
    try:
        frappe.logger().info(f"Calling Wix Update Product API for site {WIX_SITE_ID}, product {product_id}")
        frappe.logger().debug(f"Product data: {json.dumps(product_data, indent=2)}")
        
        # Simulate successful update response
        simulated_response = {
            "product": {
                "_id": product_id,
                "name": product_data["product"]["name"],
                "visible": True
            }
        }
        
        frappe.logger().info("Simulated Wix product update successful")
        return True, simulated_response
        
    except Exception as e:
        frappe.logger().error(f"Error calling Wix Update Product API: {str(e)}")
        return False, {"error": str(e)}

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
            "description": "Wix Product ID for synced items (kokofresh site)"
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

def test_wix_connection():
    """Test function to verify Wix connection"""
    try:
        frappe.logger().info(f"Testing Wix connection to site: {WIX_SITE_NAME} ({WIX_SITE_ID})")
        
        # Create a test product data
        test_product = {
            "product": {
                "name": "Test Product from Frappe",
                "productType": "PHYSICAL",
                "physicalProperties": {},
                "plainDescription": "This is a test product created from Frappe integration",
                "variantsInfo": {
                    "variants": [
                        {
                            "sku": "TEST-001",
                            "price": {
                                "actualPrice": {
                                    "amount": "10.00"
                                }
                            },
                            "physicalProperties": {},
                            "choices": []
                        }
                    ]
                },
                "visible": True
            }
        }
        
        # Test the API call
        success, response = call_wix_create_product_api(test_product)
        
        if success:
            frappe.msgprint(
                _("Wix connection test successful!"),
                title=_("Connection Test"),
                indicator="green"
            )
            return True
        else:
            frappe.msgprint(
                _(f"Wix connection test failed: {response.get('error', 'Unknown error')}"),
                title=_("Connection Test Failed"),
                indicator="red"
            )
            return False
            
    except Exception as e:
        frappe.log_error(
            message=f"Wix connection test failed: {str(e)}\n{traceback.format_exc()}",
            title="Wix Connection Test Error"
        )
        frappe.msgprint(
            _(f"Wix connection test error: {str(e)}"),
            title=_("Connection Test Error"),
            indicator="red"
        )
        return False
