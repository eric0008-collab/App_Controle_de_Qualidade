import json
import os
from pathlib import Path

APP_DATA = Path(__file__).parent


JSON_PATH = APP_DATA / "produtos.json"
def _load_produtos() -> dict:
    """Carrega o dicionário de produtos do arquivo JSON."""
    if os.path.exists(JSON_PATH):
        with open(JSON_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
# Dicionário com mapeamento de códigos para nomes dos produtos
    default = {
        "01": "produto1",
        "02": "produto2",
        "03": "produto3"
    }

    _save_produtos(default)
    return default

def _save_produtos(produtos: dict):
    """Salva o dicionário de produtos no arquivo JSON."""
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(produtos, f, ensure_ascii=False, indent=4)

# dicionário em memória
produtos = _load_produtos()

def get_nome_produto(codigo: str) -> str:
    """
    Retorna o nome do produto correspondente ao código informado.
    Se o código não existir no dicionário, retorna uma string vazia.
    """
    return produtos.get(codigo, "")

def add_produto(codigo: str, nome: str):
    """
    Adiciona um novo produto ao dicionário e persiste no JSON.
    Se o código já existir, sobrescreve o nome.
    """
    produtos[codigo] = nome
    _save_produtos(produtos)