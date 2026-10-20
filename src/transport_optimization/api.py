import math
import time

import requests

API_COLOMBIA_BASE = "https://api-colombia.com/api/v1"
OSRM_BASE = "http://router.project-osrm.org/route/v1/driving"


NAME_FIXES = {
    "Espinal": "El Espinal",
    "Rio Blanco": "Rioblanco",
    "Falán": "Falan",
    "Mariquita": "San Sebastián de Mariquita",
}

HARDCODED_BACKUPS = {
    "Armero": (-74.8964, 5.0412),
    "Dolores": (-74.9123, 3.5351),
}

IGNORE = ["Suárez"]


def get_tolima_cities() -> list:
    print("[*] Consultando departamentos en API-Colombia...")
    response = requests.get(f"{API_COLOMBIA_BASE}/Department", timeout=10)
    response.raise_for_status()
    departments = response.json()

    tolima = next(
        (d for d in departments if d.get("name", "").strip().lower() == "tolima"),
        None,
    )
    if not tolima:
        raise ValueError("No se encontró el departamento del Tolima en la API.")

    print(f"[+] ¡Tolima encontrado! ID: {tolima['id']}")
    cities_resp = requests.get(
        f"{API_COLOMBIA_BASE}/Department/{tolima['id']}/cities", timeout=15
    )

    if cities_resp.status_code == 200:
        return cities_resp.json()
    return []


def get_city_coordinates(
    city_name: str, retries: int = 3
) -> tuple[float, float] | None:
    clean_name = city_name.strip()

    if clean_name in HARDCODED_BACKUPS:
        return HARDCODED_BACKUPS[clean_name]

    if clean_name in IGNORE:
        return None

    search_name = NAME_FIXES.get(clean_name, clean_name)
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": search_name, "count": 5, "language": "es", "format": "json"}

    for attempt in range(retries):
        try:
            res = requests.get(url, params=params, timeout=15)
            time.sleep(0.3)

            if res.status_code == 200:
                results = res.json().get("results", [])
                for r in results:
                    admin = r.get("admin1", "")
                    country = r.get("country", "")
                    if ("Tolima" in admin) or (country == "Colombia"):
                        return float(r["longitude"]), float(r["latitude"])
            break

        except requests.exceptions.Timeout:
            print(
                f"    [!] Timeout con {search_name}, reintentando ({attempt + 1}/{retries})..."
            )
            time.sleep(1)
        except Exception as e:
            print(f"    [!] Error con {search_name}: {e}")
            break

    return None


def haversine_km(lon1: float, lat1: float, lon2: float, lat2: float) -> float:
    R = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dphi = p2 - p1
    dl = math.radians(lon2 - lon1)
    a = math.sin(dphi / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * R * math.asin(math.sqrt(a))


def fetch_osrm_route(
    lon1: float, lat1: float, lon2: float, lat2: float
) -> tuple[float, list[list[float]]] | None:
    url = f"{OSRM_BASE}/{lon1},{lat1};{lon2},{lat2}?overview=full&geometries=geojson"
    try:
        response = requests.get(url, timeout=20)
        time.sleep(0.15)  # Pausa para que OSRM no bloquee la IP
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and data.get("routes"):
                route = data["routes"][0]
                distance = round(route["distance"] / 1000.0, 2)
                return distance, route["geometry"]["coordinates"]
    except Exception:
        pass
    return None


def passes_through_other_city(
    route_coords: list[list[float]],
    muni_dict: dict,
    origin: str,
    target: str,
    threshold_km: float = 4.0,
) -> str | None:

    step = max(1, len(route_coords) // 300)
    sampled = route_coords[::step]
    if route_coords[-1] is not sampled[-1]:
        sampled.append(route_coords[-1])

    lons = [p[0] for p in sampled]
    lats = [p[1] for p in sampled]
    margin = threshold_km / 111.0  # ~1 grado ≈ 111 km
    min_lon, max_lon = min(lons) - margin, max(lons) + margin
    min_lat, max_lat = min(lats) - margin, max(lats) + margin

    for name, c in muni_dict.items():
        if name in (origin, target):
            continue
        if not (min_lon <= c["lon"] <= max_lon and min_lat <= c["lat"] <= max_lat):
            continue
        for lon, lat in sampled:
            if haversine_km(lon, lat, c["lon"], c["lat"]) <= threshold_km:
                return name
    return None