import requests

def get_satellite_data():
    url = "https://celestrak.org/NORAD/elements/gp.php?GROUP=stations&FORMAT=json"

    try:
        response = requests.get(url, timeout=15)

        if response.status_code == 200:
            text = response.text.strip()

            if text.startswith("["):
                return response.json()

            print("API returned text, not JSON:")
            print(text[:200])
            return []

        print("API Error:", response.status_code)
        return []

    except Exception as e:
        print("Request failed:", e)
        return []