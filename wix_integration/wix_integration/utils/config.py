"""
Configuration utilities for Wix Integration

This module handles configuration management, settings validation,
and provides helper functions for the integration.
"""

import frappe
from frappe import _

def get_wix_settings():
    """Get Wix integration settings"""
    settings = {
        'enabled': True,
        'default_site': 'dev',
        'auto_sync': True,
        'sync_on_create': True,
        'sync_on_update': True,
        'sites': {
            'dev': {
                'site_id': '63a7b738-6d1c-447a-849a-fab973366a06',
                'name': 'Dev Sitex1077548723'
            },
            'kokofresh': {
                'site_id': 'a57521a4-3ecd-40b8-852c-462f2af558d2',
                'name': 'kokofresh'
            },
            'byte_catalyst': {
                'site_id': 'bc24ec89-d58d-4b00-9c00-997dc4bb2025',
                'name': 'The Byte Catalyst | Impact Mentor'
            }
        }
    }
    
    return settings

def validate_wix_configuration():
    """Validate Wix integration configuration"""
    settings = get_wix_settings()
    
    if not settings.get('enabled'):
        return False, "Wix integration is disabled"
        
    default_site = settings.get('default_site')
    if not default_site:
        return False, "No default Wix site configured"
        
    sites = settings.get('sites', {})
    if default_site not in sites:
        return False, f"Default site '{default_site}' not found in configured sites"
        
    site_config = sites[default_site]
    if not site_config.get('site_id'):
        return False, f"No site ID configured for '{default_site}'"
        
    return True, "Configuration is valid"

def get_field_mapping():
    """Get field mapping between Frappe Item and Wix Product"""
    return {
        'frappe_to_wix': {
            'item_name': 'product.name',
            'description': 'product.plainDescription', 
            'standard_rate': 'product.variantsInfo.variants[0].price.actualPrice.amount',
            'item_code': 'product.variantsInfo.variants[0].sku',
            'weight_per_unit': 'product.variantsInfo.variants[0].physicalProperties.weight.value',
            'stock_uom': 'product.variantsInfo.variants[0].physicalProperties.weight.unit'
        },
        'wix_to_frappe': {
            'product.name': 'item_name',
            'product.plainDescription': 'description',
            'product.variantsInfo.variants[0].price.actualPrice.amount': 'standard_rate',
            'product.variantsInfo.variants[0].sku': 'item_code'
        }
    }

def get_sync_filters():
    """Get filters for determining which items should be synced"""
    return {
        'include_conditions': [
            {'field': 'is_sales_item', 'operator': '=', 'value': 1},
            {'field': 'disabled', 'operator': '=', 'value': 0},
            {'field': 'standard_rate', 'operator': '>', 'value': 0}
        ],
        'exclude_conditions': [
            {'field': 'is_fixed_asset', 'operator': '=', 'value': 1},
            {'field': 'item_group', 'operator': 'in', 'value': ['Services', 'Raw Material']}
        ]
    }

def log_sync_activity(item_code, action, status, details=None):
    """Log sync activity for monitoring and debugging"""
    try:
        log_data = {
            'item_code': item_code,
            'action': action,  # 'create', 'update', 'delete'
            'status': status,  # 'success', 'failed', 'skipped'
            'timestamp': frappe.utils.now(),
            'details': details or {}
        }
        
        frappe.logger().info(f"Wix Sync Activity: {log_data}")
        
        # Optionally store in a custom DocType for tracking
        # create_sync_log(log_data)
        
    except Exception as e:
        frappe.logger().error(f"Error logging sync activity: {str(e)}")

def create_sync_log(log_data):
    """Create a sync log entry (requires custom DocType)"""
    # This would create a record in a custom "Wix Sync Log" DocType
    # Implementation depends on whether you want to create such a DocType
    pass

def format_currency(amount, currency_code="USD"):
    """Format currency for Wix API"""
    return {
        "amount": str(amount),
        "currency": currency_code
    }

def sanitize_text_for_wix(text):
    """Sanitize text fields for Wix API"""
    if not text:
        return ""
        
    # Remove HTML tags if any
    import re
    clean_text = re.sub(r'<[^>]+>', '', str(text))
    
    # Limit length if needed
    max_length = 1000  # Adjust based on Wix limits
    if len(clean_text) > max_length:
        clean_text = clean_text[:max_length] + "..."
        
    return clean_text.strip()

def get_default_currency():
    """Get default currency from Frappe settings"""
    return frappe.defaults.get_global_default("currency") or "USD"
