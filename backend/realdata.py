import requests
def get_starlink_data():
  url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=json"
  try:
      response=requests.get(url, timeout=10)
      print ("status:",response.status_code)
      if response.status_code==200:
         return response.json()
      print("Error:", response.text[:200])
      return[]
  except Exception as e:
      print("Request failed:", e)
      return[]

## TEST
data=get_starlink_data()
print("Satellites:", len(data))
for sat in data[:5]:
  print(sat)
