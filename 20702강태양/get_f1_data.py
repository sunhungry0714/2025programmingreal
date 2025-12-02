#!/usr/bin/env python
# -*- coding: utf-8 -*-
import requests
import json
from pathlib import Path
from datetime import datetime

DATA_FILE = Path("data/motorsports.json")

def fetch_f1_schedule(year=None):
    """F1 경기 일정을 API에서 가져오기"""
    if year is None:
        year = datetime.now().year
    
    try:
        url = f"http://ergast.com/api/f1/{year}.json"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        schedule = []
        races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
        
        for race in races:
            location = race.get('Circuit', {}).get('Location', {})
            locality = location.get('locality', '')
            country = location.get('country', '')
            location_str = f"{locality}, {country}" if locality and country else (locality or country or '정보 없음')
            
            schedule.append({
                "date": race.get('date', ''),
                "event": race.get('raceName', ''),
                "location": location_str
            })
        
        return schedule
    except Exception as e:
        print(f"❌ F1 일정 가져오기 실패: {str(e)}")
        return []

def fetch_f1_results(year=None):
    """F1 경기 결과를 API에서 가져오기"""
    if year is None:
        year = datetime.now().year
    
    try:
        url = f"http://ergast.com/api/f1/{year}/results.json?limit=1000"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        results = []
        races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
        
        for race in races:
            # 우승자 찾기
            winner = None
            points = 0
            for result in race.get('Results', []):
                if result.get('position') == '1':
                    driver = result.get('Driver', {})
                    winner = f"{driver.get('givenName', '')} {driver.get('familyName', '')}".strip()
                    points = int(result.get('points', 0))
                    break
            
            if winner:
                results.append({
                    "date": race.get('date', ''),
                    "event": race.get('raceName', ''),
                    "winner": winner,
                    "points": points,
                    "season_points": None
                })
        
        return results
    except Exception as e:
        print(f"❌ F1 결과 가져오기 실패: {str(e)}")
        return []

# JSON 파일 읽기
with open(DATA_FILE, 'r', encoding='utf-8') as f:
    data = json.load(f)

motorsports_list = data.get("motorsports", [])

# F1 데이터 찾기
f1_index = None
for i, ms in enumerate(motorsports_list):
    if ms.get("id") == "f1":
        f1_index = i
        break

if f1_index is None:
    print("⚠️ F1 데이터를 찾을 수 없습니다.")
    exit(1)

print("📅 F1 경기 일정을 가져오는 중...")
schedule = fetch_f1_schedule()
print(f"✅ {len(schedule)}개의 경기 일정을 가져왔습니다.")

print("🏆 F1 경기 결과를 가져오는 중...")
results = fetch_f1_results()
print(f"✅ {len(results)}개의 경기 결과를 가져왔습니다.")

# 데이터 업데이트
motorsports_list[f1_index]["schedule"] = schedule
motorsports_list[f1_index]["results"] = results

data["motorsports"] = motorsports_list

# 파일에 저장
with open(DATA_FILE, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ F1 데이터가 성공적으로 업데이트되었습니다!")


