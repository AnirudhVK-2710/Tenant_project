import requests 

url = "https://weather-api99.p.rapidapi.com/weather"

querystring = {"city":"Dubai"}

headers = {
	"x-rapidapi-key": "b3bb6a3311mshf6bb8cd52bf24c1p17cb80jsn3913ab9e48dc",
	"x-rapidapi-host": "weather-api99.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(response.json())