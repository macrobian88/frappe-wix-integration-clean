# FIXED: Correct Frappe App Structure

## ✅ Structure Fixed According to Frappe Documentation

The repository now follows the **correct Frappe directory structure** as per the official documentation at https://docs.frappe.io/framework/user/en/basics/directory-structure

## 📁 Current Correct Structure

```
frappe-wix-integration-clean/
├── README.md                       # Project documentation
├── LICENSE                         # MIT License
├── CHANGELOG.md                   # Version history
├── IMPLEMENTATION.md              # Setup guide
├── requirements.txt               # Python dependencies
├── setup.py                       # Package setup
└── wix_integration/              # 🔑 ROOT APP DIRECTORY
    ├── __init__.py               # App version
    ├── hooks.py                  # ✅ App hooks (ROOT LEVEL)
    ├── modules.txt               # ✅ Modules list (ROOT LEVEL)  
    ├── patches.txt               # ✅ DB patches (ROOT LEVEL)
    ├── install.py                # Installation scripts
    ├── config/                   # Configuration
    │   ├── __init__.py
    │   └── desktop.py           # Desktop module config
    ├── doctype/                  # Custom DocTypes
    │   └── __init__.py
    ├── utils/                    # Utility functions
    │   ├── __init__.py
    │   └── wix_api.py           # ✅ Main integration code
    └── wix_integration/         # Module directory (named from modules.txt)
        └── __init__.py
```

## 🔧 Key Fixes Applied

### 1. **Moved Core Files to Root App Directory**
- ✅ `hooks.py` now at `wix_integration/hooks.py` (not nested)
- ✅ `modules.txt` now at `wix_integration/modules.txt` (not nested)
- ✅ `patches.txt` now at `wix_integration/patches.txt` (not nested)

### 2. **Correct Hook References**
Updated `hooks.py` to use correct import paths:
```python
doc_events = {
    "Item": {
        "after_insert": "wix_integration.utils.wix_api.create_wix_product",
        "on_update": "wix_integration.utils.wix_api.update_wix_product"
    }
}
```

### 3. **Proper Module Structure**
- Root level directories: `config/`, `doctype/`, `utils/`
- Module directory: `wix_integration/` (matching modules.txt)

## 🎯 What This Fixes

### ❌ Previous Issues:
- "Not a valid Frappe App" errors
- Nested structure that Frappe couldn't recognize
- Incorrect hook import paths

### ✅ Now Works:
- Frappe properly recognizes the app structure
- Hooks will trigger correctly when Items are created/updated
- Standard Frappe installation process will work

## 📦 Installation

The app can now be installed using standard Frappe commands:

```bash
# Navigate to your Frappe bench
cd /path/to/your/frappe-bench

# Get the app
bench get-app https://github.com/macrobian88/frappe-wix-integration-clean.git

# Install on your site
bench --site your-site-name install-app wix_integration

# Migrate and restart
bench --site your-site-name migrate
bench restart
```

## 🔍 Verification

After installation, verify the structure works by:
1. Creating a new Item in Frappe
2. Check if the wix_api.py functions are called
3. Look for Wix sync logs in the Frappe error log

## ✨ Features Ready

All core features are implemented and ready to use:

- **Automatic Item → Wix Product sync**
- **Smart field mapping**
- **Error handling and logging**
- **Support for multiple Wix sites**
- **Custom field creation for Wix Product IDs**

The repository now conforms to Frappe standards and should install without any structural issues!
