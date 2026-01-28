# fintablo — Python клиент для FinTablo API

Этот пакет предлагает полную обертку для Финтабло API созданную на основе swagger.
Эндпоинты сгруппированы следующим образом `client.<resource>`.

## Установка
```bash
pip install -e .
pip install pytest requests-mock

```

## Использование
```python
from fintablo import FinTabloClient
client = FinTabloClient(token="YOUR_TOKEN")
client._attach_endpoints(client)  # attach endpoints
client.categories.list()

# ⚠️ exceptions.py

class FinTabloError(Exception):
    pass


class FinTabloAPIError(FinTabloError):
    def __init__(self, status_code: int, message: str, payload=None):
        super().__init__(f"{status_code}: {message}")
        self.status_code = status_code
        self.payload = payload
```
