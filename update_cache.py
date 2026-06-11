from backend.realdata import get_satellite_data
import json

data = get_satellite_data()

if len(data) > 0:
    with open("data/active_satellites.json", "w") as f:
        json.dump(data, f)

    print("Updated:", len(data))
else:
    print("API failed. Cache not updated.")

from datetime import datetime

with open("data/last_update.txt", "w") as f:
    f.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))