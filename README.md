# Frappe-Wix Integration

🔄 **Automatically sync Frappe Items with Wix Products**

This Frappe app automatically creates and updates products in your Wix store whenever Items are created or modified in your Frappe/ERPNext system.

## 🚀 Features

- **Automatic Sync**: Items created in Frappe automatically become products in Wix
- **Real-time Updates**: Changes to Frappe Items update corresponding Wix products
- **Field Mapping**: Smart mapping between Frappe Item fields and Wix Product fields
- **Error Handling**: Comprehensive error logging and handling
- **Multiple Sites**: Support for multiple Wix sites
- **Configurable**: Easy to customize field mappings and sync behavior

## 🏗️ Architecture

```
Frappe Item Creation/Update → Document Hook → Wix API → Wix Product Creation/Update
```

## 📋 Available Wix Sites

Choose which Wix site to integrate with:

1. **Dev Sitex1077548723** (ID: `63a7b738-6d1c-447a-849a-fab973366a06`)
2. **kokofresh** (ID: `a57521a4-3ecd-40b8-852c-462f2af558d2`)
3. **The Byte Catalyst | Impact Mentor** (ID: `bc24ec89-d58d-4b00-9c00-997dc4bb2025`)

## 🔗 Field Mapping

| Frappe Item Field | Wix Product Field | Description |
|-------------------|-------------------|-------------|
| `item_name` | `product.name` | Product name |
| `description` | `product.plainDescription` | Product description |
| `standard_rate` | `product.variantsInfo.variants[0].price.actualPrice.amount` | Product price |
| `item_code` | `product.variantsInfo.variants[0].sku` | SKU/Product code |
| `weight_per_unit` | `product.variantsInfo.variants[0].physicalProperties.weight` | Product weight |
| `stock_uom` | Used for physical properties | Unit of measure |

## 📦 Installation

### Prerequisites
- Frappe Framework v14/v15+
- Python 3.8+
- Access to Wix site with API permissions

### Quick Install

```bash
# Navigate to your Frappe/ERPNext bench
cd /path/to/your/frappe-bench

# Get the app from GitHub
bench get-app https://github.com/macrobian88/frappe-wix-integration-clean.git

# Install on your site
bench --site your-site-name install-app wix_integration

# Run migrations and restart
bench --site your-site-name migrate
bench restart
```

### Manual Installation

1. Clone this repository into your `frappe-bench/apps/` directory:
   ```bash
   cd /path/to/frappe-bench/apps/
   git clone https://github.com/macrobian88/frappe-wix-integration-clean.git wix_integration
   ```

2. Install the app:
   ```bash
   cd /path/to/frappe-bench
   bench --site your-site-name install-app wix_integration
   bench --site your-site-name migrate
   bench restart
   ```

## ⚙️ Configuration

After installation:

1. **Configure Wix Site ID**: Update the Wix site ID in `wix_integration/utils/wix_api.py`:
   ```python
   DEFAULT_WIX_SITE = "kokofresh"  # Change to your preferred site
   ```

2. **Set up Authentication**: Configure Wix API authentication (via MCP or direct API)
3. **Test Integration**: Create a test Item in Frappe to verify the sync works

## 🧪 Testing

### Test the Integration

1. **Create a test item** in Frappe:
   ```
   Item Code: TEST-WIX-001
   Item Name: Test Product for Wix
   Is Sales Item: ✅
   Standard Rate: 29.99
   Description: Testing Wix integration
   ```

2. **Save the item** - the integration should automatically trigger
3. **Check for success**: Look for green notification "Product successfully synced to Wix!"
4. **Verify custom field**: Check if `wix_product_id` field is populated

## 🔧 Development Setup

### Local Development

```bash
# Clone the repository
git clone https://github.com/macrobian88/frappe-wix-integration-clean.git
cd frappe-wix-integration-clean

# Install in development mode
bench get-app . --skip-assets
bench --site your-site install-app wix_integration
```

## 📝 Usage

1. **Create/Update Items**: Simply create or update Items in Frappe as usual
2. **Automatic Sync**: The app automatically syncs changes to Wix
3. **Monitor Logs**: Check Frappe logs for sync status and any errors
4. **Custom Fields**: The app automatically creates a `wix_product_id` field to track synced items

## 🐛 Troubleshooting

### Common Issues

- **Sync not working**: Check that items meet sync conditions (sales item, has price, not disabled)
- **Authentication errors**: Verify Wix API credentials and site configuration
- **Field mapping issues**: Review field mappings in `utils/wix_api.py`

### Debug Mode

Enable debug logging by setting `developer_mode = 1` in your site config.

### Getting Help

1. Check the [Issues](https://github.com/macrobian88/frappe-wix-integration-clean/issues) page
2. Review the [Implementation Guide](IMPLEMENTATION.md)
3. Create a new issue with detailed error information

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📊 Project Status

- ✅ Basic Item → Product sync
- ✅ Field mapping
- ✅ Error handling
- ✅ Multiple site support
- ⏳ Bidirectional sync (Wix → Frappe)
- ⏳ Bulk sync operations
- ⏳ Advanced field mapping UI
- ⏳ Settings DocType for easy configuration

## 🔄 Version

**Current Version**: v0.0.1 (Initial Release)

---

**Made with ❤️ for the Frappe/ERPNext community**

For detailed setup instructions, see [IMPLEMENTATION.md](IMPLEMENTATION.md)
