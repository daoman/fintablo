from typing import Optional, Dict, Any

class MoneybagGroupAPI:
    """Client for `/v1/moneybag-group` endpoints (auto-generated simple wrapper).

    Methods:
     - list(params) -> GET /v1/moneybag-group
     - get(id) -> GET /v1/moneybag-group/{id}
     - create(payload) -> POST /v1/moneybag-group
     - update(id, payload) -> PUT /v1/moneybag-group/{id}
     - delete(id) -> DELETE /v1/moneybag-group/{id}
    """
    def __init__(self, client):
        self.client = client
        self.base = '/v1/moneybag-group'

    def list(self, params: Optional[Dict[str,Any]] = None, **filters):
        """List resources. Filters provided as kwargs are added to params."""
        p = params or {}
        p.update({k:v for k,v in filters.items() if v is not None})
        return self.client._request('GET', self.base, params=p)

    def get(self, id: int):
        """Get resource by id."""
        return self.client._request('GET', f"{self.base}/{id}")

    def create(self, payload: Dict[str,Any]):
        """Create resource with given payload."""
        return self.client._request('POST', self.base, json=payload)

    def update(self, id: int, payload: Dict[str,Any]):
        """Update resource by id."""
        return self.client._request('PUT', f"{self.base}/{id}", json=payload)

    def delete(self, id: int):
        """Delete resource by id."""
        return self.client._request('DELETE', f"{self.base}/{id}")
