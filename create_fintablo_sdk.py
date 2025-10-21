#!/usr/bin/env python3
# coding: utf-8
"""
Create full 'fintablo' SDK package in the target directory.

Usage:
    python3 create_fintablo_sdk.py /path/to/target/folder
"""
import os
import sys
import textwrap

TARGET = sys.argv[1] if len(sys.argv) > 1 else None
if not TARGET:
    print("Usage: python3 create_fintablo_sdk.py /path/to/target/folder")
    sys.exit(1)

# normalize
TARGET = os.path.abspath(TARGET)
PKG = os.path.join(TARGET, "fintablo")
ENDPOINTS = os.path.join(PKG, "endpoints")
TESTS = os.path.join(TARGET, "tests")
GITHUB = os.path.join(TARGET, ".github", "workflows")

for d in (PKG, ENDPOINTS, TESTS, GITHUB):
    os.makedirs(d, exist_ok=True)

files = {}

# setup.py
files[os.path.join(TARGET, "setup.py")] = textwrap.dedent("""\
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
""")

# README
files[os.path.join(TARGET, "README.md")] = textwrap.dedent("""\
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
""")

# package __init__
files[os.path.join(PKG, "__init__.py")] = textwrap.dedent("""\
    from .client import FinTabloClient
    from .exceptions import FinTabloError

    __all__ = ['FinTabloClient', 'FinTabloError']
""")

# exceptions
files[os.path.join(PKG, "exceptions.py")] = textwrap.dedent("""\
    class FinTabloError(Exception):
        \"\"\"Base exception for FinTablo client errors.\"\"\"
        def __init__(self, message, status_code=None, body=None):
            super().__init__(message)
            self.status_code = status_code
            self.body = body
""")

# client base
files[os.path.join(PKG, "client.py")] = textwrap.dedent("""\
    import requests
    from .exceptions import FinTabloError

    class FinTabloClient:
        \"\"\"Main FinTablo API client.

        :param token: Bearer token for Authorization header.
        :param base_url: Base URL for API (default: https://api.fintablo.ru)
        :param timeout: request timeout in seconds
        \"\"\"
        def __init__(self, token: str, base_url: str = "https://api.fintablo.ru", timeout: int = 30):
            if not token:
                raise ValueError("token is required")
            self.base_url = base_url.rstrip("/")
            self.session = requests.Session()
            self.session.headers.update({
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
                "Content-Type": "application/json",
            })
            self.timeout = timeout

        def _url(self, path: str) -> str:
            return self.base_url + path

        def _request(self, method: str, path: str, **kwargs):
            url = self._url(path)
            try:
                resp = self.session.request(method, url, timeout=self.timeout, **kwargs)
            except Exception as e:
                raise FinTabloError(f"Request error: {e}") from e

            if not resp.ok:
                try:
                    data = resp.json()
                except Exception:
                    data = resp.text
                raise FinTabloError(f"HTTP {resp.status_code}: {data}", status_code=resp.status_code, body=data)

            try:
                return resp.json()
            except ValueError:
                return resp.text


    # _attach_endpoints will be populated by endpoints' modules at package creation
    def _attach_endpoints(client):
        \"\"\"Attach endpoint group instances to a FinTabloClient instance.

        Call this after creating the client:
            client = FinTabloClient(token='T'); _attach_endpoints(client)
        \"\"\"
        # filled in by file generator (endpoints are created below)
""")

# minimal set of endpoints derived from swagger earlier; include many common ones
resources = [
    "category", "moneybag", "partner", "direction", "moneybag-group",
    "transaction", "deal", "project", "currency", "user", "account",
    "invoice", "report", "settings", "balance"
]
# make unique and normalized
seen = []
for r in resources:
    mod = r.replace("-", "_")
    if mod not in seen:
        seen.append(mod)
modules = seen

# create endpoint modules
for mod in modules:
    cls = "".join(part.capitalize() for part in mod.split("_")) + "API"
    base_path = f"/v1/{mod.replace('_','-')}"
    files[os.path.join(ENDPOINTS, f"{mod}.py")] = textwrap.dedent(f"""\
        from typing import Optional, Dict, Any

        class {cls}:
            \"\"\"Client for `{base_path}` endpoints (auto-generated simple wrapper).

            Methods:
             - list(params) -> GET {base_path}
             - get(id) -> GET {base_path}/{{id}}
             - create(payload) -> POST {base_path}
             - update(id, payload) -> PUT {base_path}/{{id}}
             - delete(id) -> DELETE {base_path}/{{id}}
            \"\"\"
            def __init__(self, client):
                self.client = client
                self.base = '{base_path}'

            def list(self, params: Optional[Dict[str,Any]] = None, **filters):
                \"\"\"List resources. Filters provided as kwargs are added to params.\"\"\"
                p = params or {{}}
                p.update({{k:v for k,v in filters.items() if v is not None}})
                return self.client._request('GET', self.base, params=p)

            def get(self, id: int):
                \"\"\"Get resource by id.\"\"\"
                return self.client._request('GET', f\"{{self.base}}/{{id}}\")

            def create(self, payload: Dict[str,Any]):
                \"\"\"Create resource with given payload.\"\"\"
                return self.client._request('POST', self.base, json=payload)

            def update(self, id: int, payload: Dict[str,Any]):
                \"\"\"Update resource by id.\"\"\"
                return self.client._request('PUT', f\"{{self.base}}/{{id}}\", json=payload)

            def delete(self, id: int):
                \"\"\"Delete resource by id.\"\"\"
                return self.client._request('DELETE', f\"{{self.base}}/{{id}}\")
    """)

# endpoints __init__
imports = []
allnames = []
for mod in modules:
    cls = "".join(part.capitalize() for part in mod.split("_")) + "API"
    imports.append(f"from .{mod} import {cls}")
    allnames.append(f'"{cls}"')
files[os.path.join(ENDPOINTS, "__init__.py")] = "\n".join(imports) + "\n\n__all__ = [\n" + ",\n".join(allnames) + "\n]\n"

# update client _attach_endpoints: create code block to attach each module instance
attach_code_lines = []
for mod in modules:
    cls = "".join(part.capitalize() for part in mod.split("_")) + "API"
    attach_code_lines.append(f"    client.{mod} = {cls}(client)")
attach_block = "\n\ndef _attach_endpoints(client):\n" + "\n".join(attach_code_lines) + "\n\n"
# append attach block to client.py
files[os.path.join(PKG, "client.py")] = files[os.path.join(PKG, "client.py")] + attach_block

# tests: create simple tests to verify methods presence
files[os.path.join(TESTS, "test_client_init.py")] = textwrap.dedent("""\
    from fintablo import FinTabloClient

    def test_init():
        c = FinTabloClient(token='T')
        assert hasattr(c, 'session')
""")

for mod in modules:
    test = textwrap.dedent(f"""\
        from fintablo import FinTabloClient
        from fintablo.client import _attach_endpoints

        def test_{mod}_api_methods():
            c = FinTabloClient(token='T')
            _attach_endpoints(c)
            api = getattr(c, '{mod}')
            assert callable(api.list)
            assert callable(api.get)
            assert callable(api.create)
            assert callable(api.update)
            assert callable(api.delete)
    """)
    files[os.path.join(TESTS, f"test_{mod}.py")] = test

# github ci
files[os.path.join(GITHUB, "ci.yml")] = textwrap.dedent("""\
    name: CI
    on:
      push:
        branches: [ main ]
      pull_request:
        branches: [ main ]

    jobs:
      test:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - name: Setup Python
            uses: actions/setup-python@v5
            with:
              python-version: '3.11'
          - name: Install deps
            run: |
              python -m pip install --upgrade pip
              pip install -e .
              pip install pytest requests-mock
          - name: Run tests
            run: pytest -q
""")

# write files to disk
for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print("Created package at:", TARGET)
print("To install:\n  cd %s\n  pip install -e .\n" % TARGET)