import json
from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def _ensure_dir() -> None:
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def save_graph_json(graph_data: dict, filename: str = "tolima_graph.json") -> Path:
    _ensure_dir()
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(graph_data, f, ensure_ascii=False, indent=2)
    print(f"[+] Grafo guardado en {path}")
    return path


def save_coordinates_json(
    muni_dict: dict, filename: str = "tolima_coordinates.json"
) -> Path:
    _ensure_dir()
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        json.dump(muni_dict, f, ensure_ascii=False, indent=2)
    print(f"[+] Coordenadas guardadas en {path}")
    return path


def load_graph_json(filename: str = "tolima_graph.json") -> dict:
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[!] No se encontró {path}. Ejecuta main.py para generarlo.")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_coordinates_json(filename: str = "tolima_coordinates.json") -> dict:
    path = DATA_DIR / filename
    if not path.exists():
        print(f"[!] No se encontró {path}. Ejecuta main.py para generarlo.")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
