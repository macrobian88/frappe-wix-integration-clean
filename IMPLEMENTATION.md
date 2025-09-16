# Implementation Guide: Frappe-Wix Integration

## 🚀 Quick Start

This guide will help you install and configure the Frappe-Wix integration on your system.

## 📋 Prerequisites

Before installing, ensure you have:

- **Frappe Framework v14/v15** installed and working
- **ERPNext** (optional, but recommended)
- **Python 3.8+**
- **Access to a Wix site** with appropriate permissions
- **Git** installed on your system

## 📦 Installation Steps

### Step 1: Clone and Install the App

```bash
# Navigate to your Frappe bench directory
cd /path/to/your/frappe-bench

# Get the app from GitHub
bench get-app https://github.com/macrobian88/frappe-wix-integration-clean.git

# Install the app on your site (replace 'your-site' with your actual site name)
bench --site your-site install-app wix_integration

# Run migrations to set up the database
bench --site your-site migrate

# Restart your bench to load the new app
bench restart
```

### Step 2: Verify Installation

1. Login to your Frappe/ERPNext site
2. Check if "Wix Integration" appears in the modules list
3. Go to **Settings > Integrations** and look for Wix-related settings

### Step 3: Configure Wix Site

Choose your target Wix site from the available options:

| Site Name | Site ID | Purpose |
|-----------|---------|---------|
| **Dev Sitex1077548723** | `63a7b738-6d1c-447a-849a-fab973366a06` | Development/Testing |
| **kokofresh** | `a57521a4-3ecd-40b8-852c-462f2af558d2` | Production Site |
| **The Byte Catalyst** | `bc24ec89-d58d-4b00-9c00-997dc4bb2025` | Mentor Site |

Update the configuration in:
```python
# wix_integration/wix_integration/utils/wix_api.py
DEFAULT_WIX_SITE = "kokofresh"  # Change this to your preferred site
```

## 🔧 Configuration Options

### Field Mapping

The integration automatically maps these fields:

| Frappe Item Field | Wix Product Field | Notes |
|-------------------|-------------------|-------|
| `item_name` | `product.name` | Product title |
| `description` | `product.plainDescription` | Product description |
| `standard_rate` | `product.variantsInfo.variants[0].price.actualPrice.amount` | Price |
| `item_code` | `product.variantsInfo.variants[0].sku` | SKU/Product code |
| `weight_per_unit` | `product.variantsInfo.variants[0].physicalProperties.weight` | Weight |

### Sync Conditions

Items are synced to Wix if they meet these conditions:

✅ **Included Items:**
- `is_sales_item` = 1 (Sales items only)
- `disabled` = 0 (Active items only)  
- `standard_rate` > 0 (Items with valid price)

❌ **Excluded Items:**
- Fixed assets (`is_fixed_asset` = 1)
- Service items or raw materials
- Disabled items
- Items without pricing

## 🔑 Authentication Setup

### Option 1: Wix MCP Integration (Recommended)

If you have access to Wix MCP tools:

1. Install Claude with Wix MCP
2. Authenticate your Wix account
3. The integration will automatically use MCP for API calls

### Option 2: Direct API Integration

For direct Wix API access:

1. Get Wix API credentials from your Wix site
2. Update the authentication in `wix_api.py`:

```python
def call_wix_create_product_api(site_id, product_data):
    headers = {
        'Authorization': f'Bearer {YOUR_WIX_API_TOKEN}',
        'Content-Type': 'application/json'
    }
    
    url = f'https://www.wixapis.com/stores/v3/products'
    # Implementation continues...
```

## 🧪 Testing the Integration

### Test Item Creation

1. **Create a test item** in Frappe:
   ```
   Item Code: TEST-PRODUCT-001
   Item Name: Test Product for Wix
   Item Group: Products
   Is Sales Item: ✅
   Standard Rate: 25.00
   Description: This is a test product for Wix integration
   ```

2. **Save the item** - the integration should automatically trigger

3. **Check the logs** for sync activity:
   ```bash
   # View Frappe logs
   tail -f /path/to/frappe-bench/logs/worker.log
   
   # Or check error logs in Frappe
   # Go to Settings > Error Log in your Frappe site
   ```

### Expected Behavior

✅ **Success Indicators:**
- Green success message: "Product 'Test Product for Wix' successfully synced to Wix!"
- New custom field `wix_product_id` populated in the Item
- Log entries showing successful API calls

❌ **Error Indicators:**
- Red error message about sync failure
- Error log entries in Frappe Error Log
- Empty `wix_product_id` field

## 🔍 Troubleshooting

### Common Issues

#### 1. "Not a valid Frappe App" Error
- **Solution**: Ensure you're using the clean repository: `frappe-wix-integration-clean`
- **Check**: Verify file structure has `hooks.py` only in `wix_integration/wix_integration/`

#### 2. No Sync Happening
- **Check**: Item meets sync conditions (sales item, has price, not disabled)
- **Verify**: Hooks are properly configured in `hooks.py`
- **Debug**: Enable developer mode and check logs

#### 3. Wix API Errors
- **Authentication**: Verify Wix API credentials or MCP setup
- **Permissions**: Ensure your Wix account has product management permissions
- **Rate Limits**: Check if you're hitting Wix API rate limits

#### 4. Field Mapping Issues
- **Custom Fields**: Check if `wix_product_id` field was created automatically
- **Data Types**: Verify field types match between Frappe and Wix expectations

### Debug Mode

Enable detailed logging:

```python
# In site_config.json
{
    "developer_mode": 1,
    "logging": "DEBUG"
}
```

## 🔄 Advanced Configuration

### Custom Field Mapping

To modify field mapping, edit `wix_integration/utils/wix_api.py`:

```python
def map_item_to_wix_product(doc):
    product_data = {
        "product": {
            "name": doc.item_name or doc.item_code,
            "plainDescription": doc.description or "",
            # Add custom mappings here
            "customField": doc.get("your_custom_field"),
        }
    }
    return product_data
```

### Conditional Sync Rules

Modify sync conditions in `should_sync_item()` function:

```python
def should_sync_item(doc):
    # Your custom logic
    if doc.item_group == "Digital Products":
        return True
    
    # Default conditions
    return (doc.is_sales_item and 
            not doc.disabled and 
            doc.standard_rate > 0)
```

### Multiple Wix Sites

Configure multiple sites in `wix_api.py`:

```python
WIX_SITES = {
    "production": "your-production-site-id",
    "staging": "your-staging-site-id",
    "development": "your-dev-site-id"
}

# Choose site based on conditions
def get_wix_site_id():
    if frappe.conf.get("environment") == "production":
        return WIX_SITES["production"]
    else:
        return WIX_SITES["development"]
```

## 🚧 Development Roadmap

### Current Features ✅
- [x] Basic Item → Wix Product sync
- [x] Create and Update hooks
- [x] Error handling and logging
- [x] Field mapping
- [x] Sync conditions

### Planned Features 📋
- [ ] Bidirectional sync (Wix → Frappe)
- [ ] Bulk sync operations
- [ ] Settings DocType for configuration
- [ ] Sync status dashboard
- [ ] Image sync support
- [ ] Category/collection mapping

## 🆘 Getting Help

If you encounter issues:

1. **Check the logs** first - most issues are logged with helpful details
2. **Review this guide** - ensure you followed all setup steps
3. **Create an issue** on GitHub with:
   - Error messages
   - Frappe/ERPNext version
   - Steps to reproduce
   - Log excerpts (remove sensitive data)

## 📄 License

This project is open-source under the MIT License. Feel free to modify and distribute as needed.

---

**Happy syncing! 🎉**

*For additional support, please visit the [GitHub Issues](https://github.com/macrobian88/frappe-wix-integration-clean/issues) page.*
