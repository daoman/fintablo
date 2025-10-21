# fintablo — custom Python wrapper for FinTablo API (full SDK)

This package provides a lightweight, human-friendly wrapper around the FinTablo API.
It exposes grouped endpoint helpers under `client.<resource>`.

## Install (development)
```bash
pip install -e .
pip install pytest requests-mock
```

## Usage
```python
from fintablo import FinTabloClient
client = FinTabloClient(token="YOUR_TOKEN")
client._attach_endpoints(client)  # attach endpoints
client.categories.list()
```
