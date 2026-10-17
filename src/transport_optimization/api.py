import time
import requests

API_COLOMBIA_BASE = "https://api-colombia.com/api/v1"
OSRM_BASE = "http://router.project-osrm.org/route/v1/driving"

# Correcciones de nombres para la API de mapas
NAME_FIXES = {
    "Espinal": "El Espinal",
    "Rio Blanco": "Rioblanco",
    "Falán": "Falan",
    "Mariquita": "San Sebastián de Mariquita"
}

# Solo para los municipios rebeldes que Open-Meteo confunde con otros países
HARDCODED_BACKUPS = {
    "Armero": (-74.8964, 5.0412),
    "Dolores": (-74.9123, 3.5351)
}

def get_tolima_cities() -> list:
    print("[*] Consultando departamentos en API-Colombia...")
    response = requests.get(f"{API_COLOMBIA_BASE}/Department", timeout=10)
    response.raise_for_status()
    departments = response.json()
    
    tolima = next((d for d in departments if d.get("name", "").strip().lower() == "tolima"), None)
    if not tolima:
        raise ValueError("No se encontró el departamento del Tolima en la API.")
        
    print(f"[+] ¡Tolima encontrado! ID: {tolima['id']}")
    cities_resp = requests.get(f"{API_COLOMBIA_BASE}/Department/{tolima['id']}/cities", timeout=15)
    
    if cities_resp.status_code == 200:
        return cities_resp.json()
    return []

def get_city_coordinates(city_name: str, retries: int = 3) -> tuple[float, float] | None:
    clean_name = city_name.strip()
    
    # Revisar si está en la lista de rebeldes primero
    if clean_name in HARDCODED_BACKUPS:
        return HARDCODED_BACKUPS[clean_name]
        
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
                    # Filtro criminal y estricto: Tiene que ser en Tolima o al menos Colombia
                    if ("Tolima" in admin) or (country == "Colombia"):
                        return float(r["longitude"]), float(r["latitude"])
            break # Si respondió bien pero no halló nada, salimos del ciclo de reintentos
            
        except requests.exceptions.Timeout:
            print(f"    [!] Timeout con {search_name}, reintentando ({attempt + 1}/{retries})...")
            time.sleep(1)
        except Exception as e:
            print(f"    [!] Error con {search_name}: {e}")
            break
            
    return None

def fetch_osrm_distance(lon1: float, lat1: float, lon2: float, lat2: float) -> float | None:
    url = f"{OSRM_BASE}/{lon1},{lat1};{lon2},{lat2}?overview=false"
    try:
        response = requests.get(url, timeout=10)
        time.sleep(0.15) # Pausa cortita vital para que OSRM no nos bloquee la IP
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == "Ok" and data.get("routes"):
                return round(data["routes"][0]["distance"] / 1000.0, 2)
    except Exception:
        pass # Ignoramos errores de red puntuales para que no se caiga el script completo
    return None