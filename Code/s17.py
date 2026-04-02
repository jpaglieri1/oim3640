import requests
import os
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv('OPENWEATHER_API_KEY')

url = (f'https://api.openweathermap.org/data/2.5/weather?q=Boston&appid=(API_KEY)&units=imperial')

print(url)
data = requests.get(url).json()
print(f'Boston: {data['main']['temp']}F')

##response = requests.get("https://oim.108122.xyz/mass", headers={"X-Token": "jackiejackie"},)
