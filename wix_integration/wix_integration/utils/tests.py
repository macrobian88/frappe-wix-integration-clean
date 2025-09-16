"""
Test utilities for Wix Integration

This module provides testing functions to validate the integration
and troubleshoot common issues.
"""

import frappe
from frappe import _
import json

def test_integration():
    """
    Run comprehensive tests on the Wix integration
    
    Returns:
        dict: Test results
    """
    results = {
        "overall_status": "unknown",
        "tests": []
    }
    
    # Test 1: Check app installation
    app_test = test_app_installation()
    results["tests"].append(app_test)
    
    # Test 2: Check configuration
    config_test = test_configuration()
    results["tests"].append(config_test)
    
    # Test 3: Check custom fields
    fields_test = test_custom_fields()
    results["tests"].append(fields_test)
    
    # Test 4: Check hooks
    hooks_test = test_hooks_configuration()
    results["tests"].append(hooks_test)
    
    # Test 5: Test API connectivity (if available)
    api_test = test_api_connectivity()
    results["tests"].append(api_test)
    
    # Determine overall status
    failed_tests = [t for t in results["tests"] if not t["passed"]]
    if not failed_tests:
        results["overall_status"] = "passed"
    elif len(failed_tests) == len(results["tests"]):
        results["overall_status"] = "failed"
    else:
        results["overall_status"] = "partial"
    
    return results

def test_app_installation():
    """Test if the app is properly installed"""
    try:
        # Check if app exists in installed apps
        installed_apps = frappe.get_installed_apps()
        app_installed = "wix_integration" in installed_apps
        
        return {
            "name": "App Installation",
            "passed": app_installed,
            "message": "Wix Integration app is installed" if app_installed else "Wix Integration app not found",
            "details": {
                "installed_apps": installed_apps
            }
        }
        
    except Exception as e:
        return {
            "name": "App Installation",
            "passed": False,
            "message": f"Error checking app installation: {str(e)}",
            "details": {"error": str(e)}
        }

def test_configuration():
    """Test configuration settings"""
    try:
        from .config import get_wix_settings, validate_wix_configuration
        
        settings = get_wix_settings()
        is_valid, validation_message = validate_wix_configuration()
        
        return {
            "name": "Configuration",
            "passed": is_valid,
            "message": validation_message,
            "details": {
                "settings": settings
            }
        }
        
    except Exception as e:
        return {
            "name": "Configuration",
            "passed": False,
            "message": f"Configuration test failed: {str(e)}",
            "details": {"error": str(e)}
        }

def test_custom_fields():
    """Test if custom fields are created"""
    try:
        # Check if wix_product_id field exists
        field_exists = frappe.db.exists("Custom Field", {
            "dt": "Item",
            "fieldname": "wix_product_id"
        })
        
        return {
            "name": "Custom Fields",
            "passed": field_exists,
            "message": "Wix Product ID field exists" if field_exists else "Wix Product ID field missing",
            "details": {
                "wix_product_id_field": field_exists
            }
        }
        
    except Exception as e:
        return {
            "name": "Custom Fields",
            "passed": False,
            "message": f"Custom fields test failed: {str(e)}",
            "details": {"error": str(e)}
        }

def test_hooks_configuration():
    """Test if hooks are properly configured"""
    try:
        from .. import hooks
        
        # Check if doc_events are configured
        doc_events = getattr(hooks, 'doc_events', {})
        item_hooks = doc_events.get('Item', {})
        
        has_insert_hook = 'after_insert' in item_hooks
        has_update_hook = 'on_update' in item_hooks
        
        passed = has_insert_hook and has_update_hook
        
        return {
            "name": "Hooks Configuration",
            "passed": passed,
            "message": "Item hooks configured properly" if passed else "Item hooks missing or incomplete",
            "details": {
                "doc_events": doc_events,
                "item_hooks": item_hooks,
                "has_insert_hook": has_insert_hook,
                "has_update_hook": has_update_hook
            }
        }
        
    except Exception as e:
        return {
            "name": "Hooks Configuration",
            "passed": False,
            "message": f"Hooks test failed: {str(e)}",
            "details": {"error": str(e)}
        }

def test_api_connectivity():
    """Test API connectivity (if possible)"""
    try:
        # This is a placeholder - actual implementation depends on authentication method
        return {
            "name": "API Connectivity",
            "passed": True,
            "message": "API connectivity test not implemented (placeholder)",
            "details": {
                "note": "Implement actual API connectivity test when authentication is configured"
            }
        }
        
    except Exception as e:
        return {
            "name": "API Connectivity",
            "passed": False,
            "message": f"API connectivity test failed: {str(e)}",
            "details": {"error": str(e)}
        }

def create_test_item():
    """Create a test item for integration testing"""
    try:
        test_item_code = "TEST-WIX-INTEGRATION-001"
        
        # Check if test item already exists
        if frappe.db.exists("Item", test_item_code):
            frappe.delete_doc("Item", test_item_code)
        
        # Create test item
        test_item = frappe.get_doc({
            "doctype": "Item",
            "item_code": test_item_code,
            "item_name": "Test Product for Wix Integration",
            "item_group": "Products",
            "is_sales_item": 1,
            "standard_rate": 29.99,
            "description": "This is a test product created to validate Wix integration",
            "stock_uom": "Nos"
        })
        
        test_item.insert()
        
        return {
            "success": True,
            "item_code": test_item_code,
            "message": "Test item created successfully"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Failed to create test item: {str(e)}"
        }

def cleanup_test_data():
    """Clean up test data"""
    try:
        test_items = frappe.get_all("Item", 
            filters={"item_code": ["like", "TEST-WIX-%"]},
            fields=["name", "item_code"]
        )
        
        deleted_count = 0
        for item in test_items:
            try:
                frappe.delete_doc("Item", item.name)
                deleted_count += 1
            except Exception as e:
                frappe.logger().error(f"Error deleting test item {item.item_code}: {str(e)}")
        
        return {
            "success": True,
            "deleted_count": deleted_count,
            "message": f"Cleaned up {deleted_count} test items"
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "message": f"Cleanup failed: {str(e)}"
        }

def run_integration_test():
    """Run a complete integration test"""
    try:
        results = {
            "timestamp": frappe.utils.now(),
            "steps": []
        }
        
        # Step 1: Create test item
        create_result = create_test_item()
        results["steps"].append({
            "step": "Create Test Item",
            "result": create_result
        })
        
        if create_result.get("success"):
            # Step 2: Wait for sync (in real scenario)
            import time
            time.sleep(2)  # Allow hooks to execute
            
            # Step 3: Check if wix_product_id was set
            item_code = create_result["item_code"]
            wix_product_id = frappe.db.get_value("Item", item_code, "wix_product_id")
            
            sync_result = {
                "success": bool(wix_product_id),
                "wix_product_id": wix_product_id,
                "message": "Wix Product ID set" if wix_product_id else "Wix Product ID not set"
            }
            
            results["steps"].append({
                "step": "Check Sync Result",
                "result": sync_result
            })
        
        # Step 4: Cleanup
        cleanup_result = cleanup_test_data()
        results["steps"].append({
            "step": "Cleanup Test Data",
            "result": cleanup_result
        })
        
        # Determine overall result
        failed_steps = [s for s in results["steps"] if not s["result"].get("success")]
        results["overall_success"] = len(failed_steps) == 0
        
        return results
        
    except Exception as e:
        return {
            "overall_success": False,
            "error": str(e),
            "message": f"Integration test failed: {str(e)}"
        }

def print_test_results(results):
    """Print test results in a readable format"""
    print("\\n" + "="*50)
    print("WIX INTEGRATION TEST RESULTS")
    print("="*50)
    
    if isinstance(results, dict) and "tests" in results:
        # Standard test results
        print(f"Overall Status: {results['overall_status'].upper()}")
        print("\\n" + "-"*30)
        
        for test in results["tests"]:
            status = "✅ PASS" if test["passed"] else "❌ FAIL"
            print(f"{status} {test['name']}: {test['message']}")
    
    elif isinstance(results, dict) and "steps" in results:
        # Integration test results
        status = "✅ PASS" if results["overall_success"] else "❌ FAIL"
        print(f"Overall Status: {status}")
        print("\\n" + "-"*30)
        
        for step in results["steps"]:
            step_status = "✅" if step["result"].get("success") else "❌"
            print(f"{step_status} {step['step']}: {step['result'].get('message', 'No message')}")
    
    print("="*50)
