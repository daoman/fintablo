from setuptools import setup, find_packages

setup(
    name="fintablo",
    version="0.1.0",
    description="Custom lightweight Python wrapper for FinTablo API",
    packages=find_packages(),
    install_requires=["requests>=2.20.0"],
    include_package_data=True,
    author="Generated",
    license="MIT",
)
