import requests

resposne = requests.get('https://sportsdataapi.onrender.com/nba/players/stats/20002712?season=2024')
print(resposne.json())