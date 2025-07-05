import requests


def get_produto(target_codigo):
    URL_API = "URL_API"
    resp = requests.get(URL_API)
    resp.raise_for_status()
    data = resp.json()
    for row in data:
        if str(row.get("CÓD SAP")) == str(target_codigo):
            return row.get("PRODUTO")
    return None