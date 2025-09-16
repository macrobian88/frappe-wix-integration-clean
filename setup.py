from setuptools import setup, find_packages

# Read version from the __init__.py file without importing it
def get_version():
    with open("wix_integration/__init__.py", "r") as f:
        content = f.read()
        for line in content.splitlines():
            if line.startswith("__version__"):
                return line.split("=")[1].strip().strip('"').strip("'")
    return "0.0.1"

with open("requirements.txt") as f:
    install_requires = f.read().strip().split("\n")

setup(
    name="wix_integration",
    version=get_version(),
    description="Integration between Frappe and Wix for automatic product sync",
    author="Your Company",
    author_email="your-email@example.com",
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=install_requires
)
