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

### Method 1: Install from GitHub

```bash
# Navigate to your Frappe/ERPNext site
cd /path/to/your/frappe-bench

# Get the app
bench get-app https://github.com/macrobian88/frappe-wix-integration-clean.git

# Install on your site
bench --site your-site-name install-app wix_integration

# Restart and migrate
bench --site your-site-name migrate
bench restart
```

### Method 2: Manual Installation

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

1. **Configure Wix Site ID**: Update the Wix site ID in the app settings
2. **Set up Authentication**: Configure Wix API authentication (via MCP or direct API)
3. **Test Integration**: Create a test Item in Frappe to verify the sync works

## 🔧 Development Setup

### Prerequisites
- Frappe Framework v14/15+
- Python 3.8+
- Access to Wix site with API permissions

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

## 🐛 Troubleshooting

### Common Issues

- **"Not a valid Frappe App" error**: Ensure you're using this clean repository
- **Sync not working**: Check Wix API credentials and site ID configuration
- **Field mapping issues**: Review the field mapping configuration in the utils

### Debug Mode

Enable debug logging by setting `developer_mode = 1` in your site config.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Commit changes: `git commit -m 'Add amazing feature'`
4. Push to branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

If you encounter any issues:

1. Check the [Issues](https://github.com/macrobian88/frappe-wix-integration-clean/issues) page
2. Create a new issue with detailed information
3. Include Frappe logs and error messages

## 📊 Project Status

- ✅ Basic Item → Product sync
- ✅ Field mapping
- ✅ Error handling
- ⏳ Bidirectional sync (Wix → Frappe)
- ⏳ Bulk sync operations
- ⏳ Advanced field mapping UI

---

**Made with ❤️ for the Frappe/ERPNext community**
