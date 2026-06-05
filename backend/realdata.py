import requests
def get_starlink_data():
  url="https://celestrak.org/NORAD/elements/gp.php?GROUP=starlink&FORMAT=json"
  response=requests.get(url)
  if response.status_code==200:
    return response.json()
  return[]
## TEST
data=get_starlink_data()
print("Satellites:", len(data))