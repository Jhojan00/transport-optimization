import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"
JSON_PATH = DATA_DIR / "distances.json"

def save_graph_json(data: dict) -> None:
    # Guardar el diccionario de distancias en el archivo JSON
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"Grafo persistido correctamente en: {JSON_PATH}")

def load_graph_json() -> dict:
    # Cargar el JSON crudo para posteriormente montarlo en memoria
    if not JSON_PATH.exists():
        return {}
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        return json.load(f)