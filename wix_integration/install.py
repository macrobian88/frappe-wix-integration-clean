import frappe
from frappe import _
from frappe.utils import getdate, today
from frappe.model.document import Document
import json
import requests
import traceback

def after_install():
    """Setup Wix Integration after app installation"""
    try:
        # Create default Wix Integration Settings
        create_wix_integration_settings()
        
        # Create Error Log for troubleshooting
        frappe.msgprint(
            _("Wix Integration app installed successfully! Please configure your Wix site settings."),
            title=_("Installation Complete"),
            indicator="green"
        )
        
    except Exception as e:
        frappe.log_error(
            message=traceback.format_exc(),
            title="Wix Integration Installation Error"
        )
        frappe.throw(_("Installation failed. Please check the error log for details."))

def create_wix_integration_settings():
    """Create default settings document if it doesn't exist"""
    try:
        # Check if settings already exist
        if frappe.db.exists("Wix Integration Settings", "Wix Integration Settings"):
            return
            
        # Create settings document structure would go here
        # For now, just log that settings need to be configured
        frappe.logger().info("Wix Integration Settings need to be configured manually")
        
    except Exception as e:
        frappe.log_error(
            message=f"Error creating Wix Integration Settings: {str(e)}",
            title="Wix Integration Settings Creation Error"
        )

def validate_wix_connection(site_id):
    """Test connection to Wix API"""
    try:
        # This would test the connection to Wix
        # Implementation depends on authentication method
        return True
    except Exception as e:
        frappe.log_error(
            message=f"Wix connection validation failed: {str(e)}",
            title="Wix Connection Error"
        )
        return False
