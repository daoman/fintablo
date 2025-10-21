import requests
from .exceptions import FinTabloError
from .endpoints import (
    CategoryAPI,
    MoneybagAPI,
    PartnerAPI,
    DirectionAPI,
    MoneybagGroupAPI,
    TransactionAPI,
    DealAPI,
    ProjectAPI,
    CurrencyAPI,
    UserAPI,
    AccountAPI,
    InvoiceAPI,
    ReportAPI,
    SettingsAPI,
    BalanceAPI
)

class FinTabloClient:
    """Main FinTablo API client.

    :param token: Bearer token for Authorization header.
    :param base_url: Base URL for API (default: https://api.fintablo.ru)
    :param timeout: request timeout in seconds
    """
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
    """Attach endpoint group instances to a FinTabloClient instance.

    Call this after creating the client:
        client = FinTabloClient(token='T'); _attach_endpoints(client)
    """
    # filled in by file generator (endpoints are created below)


def _attach_endpoints(client):
    client.category = CategoryAPI(client)
    client.moneybag = MoneybagAPI(client)
    client.partner = PartnerAPI(client)
    client.direction = DirectionAPI(client)
    client.moneybag_group = MoneybagGroupAPI(client)
    client.transaction = TransactionAPI(client)
    client.deal = DealAPI(client)
    client.project = ProjectAPI(client)
    client.currency = CurrencyAPI(client)
    client.user = UserAPI(client)
    client.account = AccountAPI(client)
    client.invoice = InvoiceAPI(client)
    client.report = ReportAPI(client)
    client.settings = SettingsAPI(client)
    client.balance = BalanceAPI(client)

