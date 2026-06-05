import requests


def get_active_satellite_data():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"

    try:
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            return response.json()

        print("API Blocked:", response.status_code, response.text[:200])
        return []

    except Exception as e:
        print("Request failed:", e)
        return []