# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Bidirectional sync (Wix → Frappe) support
- Settings DocType for easy configuration
- Image sync support
- Category/collection mapping
- Bulk sync operations
- Sync status dashboard

### Changed
- Enhanced error handling
- Improved logging

### Fixed
- Memory leaks in long-running sync operations

## [0.0.1] - 2024-09-16

### Added
- Initial release of Frappe-Wix Integration
- Basic Item → Wix Product sync functionality
- Support for create and update operations via Frappe hooks
- Comprehensive field mapping between Frappe Items and Wix Products
- Error handling and logging system
- Support for multiple Wix sites configuration
- MCP integration framework (placeholder)
- Test utilities for validation
- Configuration management system
- Automatic custom field creation for storing Wix Product IDs

### Features
- **Automatic Sync**: Items created/updated in Frappe automatically sync to Wix
- **Field Mapping**: Smart mapping of fields (name, description, price, SKU, weight)
- **Site Selection**: Support for multiple Wix sites (Dev, kokofresh, Byte Catalyst)
- **Conditional Sync**: Only sync sales items with valid pricing
- **Error Handling**: Comprehensive error logging and user notifications
- **Custom Fields**: Automatic creation of `wix_product_id` field in Item doctype

### Technical Implementation
- Document hooks for `after_insert` and `on_update` events on Item doctype
- Modular architecture with separate utilities for API, config, MCP, and testing
- Proper Frappe app structure with all required files
- Support for both MCP and direct API authentication methods

### File Structure
```
wix_integration/
├── __init__.py                     # App version
├── install.py                      # Post-install setup
└── wix_integration/               # Inner module
    ├── __init__.py                # Module version
    ├── hooks.py                   # App configuration and hooks
    ├── modules.txt                # Module definition
    ├── patches.txt                # Database patches
    ├── config/                    # Frappe configuration
    │   ├── __init__.py
    │   └── desktop.py            # Desktop module config
    ├── doctype/                   # Custom doctypes (future)
    │   └── __init__.py
    └── utils/                     # Core utilities
        ├── __init__.py
        ├── wix_api.py            # Main API integration
        ├── config.py             # Configuration utilities
        ├── mcp_integration.py    # MCP framework
        └── tests.py              # Test utilities
```

### Configuration
- Pre-configured Wix sites with IDs
- Configurable sync conditions
- Field mapping customization support
- Multiple authentication methods

### Documentation
- Comprehensive README with features and installation
- Detailed implementation guide with step-by-step instructions
- Troubleshooting section for common issues
- Development roadmap and contribution guidelines

---

## Version History Summary

- **v0.0.1** (2024-09-16): Initial release with core sync functionality
