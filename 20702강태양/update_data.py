import requests
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("data/motorsports.json")
year = datetime.now().year

# F1 일정 가져오기
print("Fetching F1 schedule...")
url1 = f"http://ergast.com/api/f1/{year}.json"
r1 = requests.get(url1, timeout=10)
data1 = r1.json()
races1 = data1.get('MRData', {}).get('RaceTable', {}).get('Races', [])

schedule = []
for race in races1:
    location = race.get('Circuit', {}).get('Location', {})
    locality = location.get('locality', '')
    country = location.get('country', '')
    location_str = f"{locality}, {country}" if locality and country else (locality or country or '정보 없음')
    schedule.append({
        "date": race.get('date', ''),
        "event": race.get('raceName', ''),
        "location": location_str
    })

print(f"Got {len(schedule)} schedules")

# F1 결과 가져오기
print("Fetching F1 results...")
url2 = f"http://ergast.com/api/f1/{year}/results.json?limit=1000"
r2 = requests.get(url2, timeout=10)
data2 = r2.json()
races2 = data2.get('MRData', {}).get('RaceTable', {}).get('Races', [])

results = []
for race in races2:
    for result in race.get('Results', []):
        if result.get('position') == '1':
            driver = result.get('Driver', {})
            winner = f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip()
            points = int(result.get('points', 0))
            results.append({
                "date": race.get('date', ''),
                "event": race.get('raceName', ''),
                "winner": winner,
                "points": points,
                "season_points": None
            })
            break

print(f"Got {len(results)} results")

# JSON 파일 읽기 및 업데이트
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

motorsports_list = data.get("motorsports", [])
f1_index = None
for i, ms in enumerate(motorsports_list):
    if ms.get("id") == "f1":
        f1_index = i
        break

if f1_index is not None:
    motorsports_list[f1_index]["schedule"] = schedule
    motorsports_list[f1_index]["results"] = results
    data["motorsports"] = motorsports_list
    
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    print("Successfully updated F1 data!")
else:
    print("F1 data not found in JSON file")


