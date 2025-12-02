import streamlit as st
import json
from datetime import datetime
import pandas as pd
from pathlib import Path
import requests

# 페이지 설정
st.set_page_config(
    page_title="모터스포츠 정보 센터",
    page_icon="🏎️",
    layout="wide"
)

# 데이터 파일 경로
DATA_FILE = Path("data/motorsports.json")

def load_data():
    """데이터 파일 로드"""
    try:
        if not DATA_FILE.exists():
            st.warning("⚠️ 데이터 파일을 찾을 수 없습니다. 관리자에게 문의하세요.")
            return {"motorsports": []}
        
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict) or "motorsports" not in data:
                st.error("❌ 데이터 형식이 올바르지 않습니다.")
                return {"motorsports": []}
            return data
    except json.JSONDecodeError as e:
        st.error(f"❌ JSON 파일 형식 오류: {str(e)}")
        return {"motorsports": []}
    except Exception as e:
        st.error(f"❌ 데이터를 불러오는 중 오류가 발생했습니다: {str(e)}")
        return {"motorsports": []}

def save_data(data):
    """데이터를 JSON 파일에 저장"""
    try:
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"❌ 데이터 저장 중 오류가 발생했습니다: {str(e)}")
        return False

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
        st.error(f"❌ F1 일정 가져오기 실패: {str(e)}")
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
                    "season_points": None  # 시즌 누적 포인트는 별도 계산 필요
                })
        
        return results
    except Exception as e:
        st.error(f"❌ F1 결과 가져오기 실패: {str(e)}")
        return []


def format_date(date_str):
    """날짜 문자열을 포맷팅"""
    if not date_str or not isinstance(date_str, str):
        return "날짜 정보 없음"
    try:
        date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return date_obj.strftime("%Y년 %m월 %d일")
    except ValueError:
        return date_str
    except Exception:
        return "날짜 형식 오류"

def display_schedule(schedule_data):
    """경기 일정을 달력 형식으로 표시"""
    if not schedule_data:
        st.info("ℹ️ 아직 경기 일정이 등록되지 않았습니다. 죄송합니다.")
        return
    
    if not isinstance(schedule_data, list):
        st.warning("⚠️ 경기 일정 데이터 형식이 올바르지 않습니다.")
        return
    
    # 날짜순으로 정렬
    try:
        sorted_schedule = sorted(
            schedule_data, 
            key=lambda x: x.get('date', '') if isinstance(x, dict) else ''
        )
    except Exception:
        sorted_schedule = schedule_data
    
    # 달력 형식으로 표시하기 위해 월별로 그룹화
    schedule_by_month = {}
    for event in sorted_schedule:
        if not isinstance(event, dict):
            continue
        date_str = event.get('date', '')
        if not date_str:
            continue
        try:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            month_key = date_obj.strftime("%Y년 %m월")
            if month_key not in schedule_by_month:
                schedule_by_month[month_key] = []
            schedule_by_month[month_key].append(event)
        except (ValueError, TypeError):
            continue
    
    if not schedule_by_month:
        st.info("ℹ️ 유효한 경기 일정이 없습니다. 죄송합니다.")
        return
    
    # 월별로 표시
    for month, events in schedule_by_month.items():
        st.subheader(f"📅 {month}")
        
        # 표 형식으로 일정 표시
        try:
            schedule_df = pd.DataFrame([
                {
                    "날짜": format_date(event.get('date', '')),
                    "경기명": event.get('event', '정보 없음'),
                    "장소": event.get('location', '정보 없음')
                }
                for event in events
            ])
            st.dataframe(schedule_df, use_container_width=True, hide_index=True)
        except Exception as e:
            st.error(f"일정 표시 중 오류가 발생했습니다: {str(e)}")

def display_results(results_data):
    """경기 결과를 표 형식으로 표시"""
    if not results_data:
        st.info("ℹ️ 아직 경기 결과가 등록되지 않았습니다. 죄송합니다.")
        return
    
    if not isinstance(results_data, list):
        st.warning("⚠️ 경기 결과 데이터 형식이 올바르지 않습니다.")
        return
    
    # 날짜순으로 정렬 (최신순)
    try:
        sorted_results = sorted(
            results_data, 
            key=lambda x: x.get('date', '') if isinstance(x, dict) else '',
            reverse=True
        )
    except Exception:
        sorted_results = results_data
    
    # 표 형식으로 결과 표시
    try:
        results_df = pd.DataFrame([
            {
                "날짜": format_date(result.get('date', '')),
                "경기명": result.get('event', '정보 없음'),
                "우승자": result.get('winner', '정보 없음'),
                "포인트": result.get('points', '정보 없음'),
                "시즌 누적 포인트": result.get('season_points', '정보 없음')
            }
            for result in sorted_results if isinstance(result, dict)
        ])
        
        if results_df.empty:
            st.info("ℹ️ 유효한 경기 결과가 없습니다. 죄송합니다.")
        else:
            st.dataframe(results_df, use_container_width=True, hide_index=True)
    except Exception as e:
        st.error(f"결과 표시 중 오류가 발생했습니다: {str(e)}")

def display_driver_championship(driver_championship_data):
    """드라이버 챔피언십 포인트 순위를 표 형식으로 표시"""
    if not driver_championship_data:
        st.info("ℹ️ 드라이버 챔피언십 순위 정보가 등록되지 않았습니다.")
        return
    
    if not isinstance(driver_championship_data, list):
        st.warning("⚠️ 드라이버 챔피언십 데이터 형식이 올바르지 않습니다.")
        return
    
    try:
        # 포인트순으로 정렬 (내림차순)
        sorted_championship = sorted(
            driver_championship_data,
            key=lambda x: x.get('points', 0) if isinstance(x, dict) else 0,
            reverse=True
        )
        
        # 순위 다시 매기기 (포인트가 같을 경우를 대비)
        championship_list = []
        current_rank = 1
        prev_points = None
        
        for driver in sorted_championship:
            if not isinstance(driver, dict):
                continue
            
            points = driver.get('points', 0)
            # 포인트가 같으면 같은 순위
            if prev_points is not None and points < prev_points:
                current_rank = len(championship_list) + 1
            
            championship_list.append({
                "순위": current_rank,
                "드라이버": driver.get('driver', '정보 없음'),
                "팀": driver.get('team', '정보 없음'),
                "포인트": points
            })
            
            prev_points = points
        
        if not championship_list:
            st.info("ℹ️ 유효한 드라이버 챔피언십 데이터가 없습니다.")
            return
        
        championship_df = pd.DataFrame(championship_list)
        
        # 상위 3명 강조를 위한 정보 표시
        if len(championship_df) > 0:
            st.markdown("**🥇 1위 | 🥈 2위 | 🥉 3위**")
        
        # 표 형식으로 표시
        st.dataframe(championship_df, use_container_width=True, hide_index=True)
        
        # 상위 3명 하이라이트 (마크다운으로)
        if len(championship_list) >= 3:
            st.markdown("---")
            col1, col2, col3 = st.columns(3)
            with col1:
                if len(championship_list) >= 1:
                    st.success(f"🥇 **1위:** {championship_list[0]['드라이버']} ({championship_list[0]['포인트']}점)")
            with col2:
                if len(championship_list) >= 2:
                    st.info(f"🥈 **2위:** {championship_list[1]['드라이버']} ({championship_list[1]['포인트']}점)")
            with col3:
                if len(championship_list) >= 3:
                    st.warning(f"🥉 **3위:** {championship_list[2]['드라이버']} ({championship_list[2]['포인트']}점)")
        
    except Exception as e:
        st.error(f"드라이버 챔피언십 표시 중 오류가 발생했습니다: {str(e)}")

def main():
    # 타이틀
    st.title("🏎️ 모터스포츠 정보 센터")
    
    st.markdown("---")
    
    # 데이터 로드
    data = load_data()
    motorsports_list = data.get("motorsports", [])
    
    if not motorsports_list:
        st.warning("⚠️ 등록된 모터스포츠가 없습니다. 관리자에게 문의하세요.")
        return
    
    # 모터스포츠 선택 위젯
    motorsport_names = [ms.get("name", "이름 없음") for ms in motorsports_list]
    selected_name = st.selectbox(
        "원하는 모터스포츠를 선택하세요:",
        motorsport_names,
        index=0
    )
    
    # 선택된 모터스포츠 찾기
    selected_motorsport = None
    for ms in motorsports_list:
        if ms.get("name") == selected_name:
            selected_motorsport = ms
            break
    
    if not selected_motorsport:
        st.error("선택된 모터스포츠를 찾을 수 없습니다.")
        return
    
    st.markdown("---")
    
    # SNS 바로가기 섹션
    st.header("🔗 공식 SNS 바로가기")
    sns_links = selected_motorsport.get("sns_links", {})
    
    if sns_links and isinstance(sns_links, dict):
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if "official_website" in sns_links and sns_links["official_website"]:
                try:
                    st.link_button("🌐 공식 웹사이트", sns_links["official_website"])
                except Exception:
                    st.info("🌐 공식 웹사이트 링크 오류")
        
        with col2:
            if "youtube" in sns_links and sns_links["youtube"]:
                try:
                    st.link_button("📺 YouTube", sns_links["youtube"])
                except Exception:
                    st.info("📺 YouTube 링크 오류")
        
        with col3:
            if "instagram" in sns_links and sns_links["instagram"]:
                try:
                    st.link_button("📷 Instagram", sns_links["instagram"])
                except Exception:
                    st.info("📷 Instagram 링크 오류")
        
        with col4:
            if "twitter" in sns_links and sns_links["twitter"]:
                try:
                    st.link_button("🐦 Twitter/X", sns_links["twitter"])
                except Exception:
                    st.info("🐦 Twitter/X 링크 오류")
    else:
        st.info("ℹ️ SNS 링크가 등록되지 않았습니다.")
    
    st.markdown("---")
    
    # 경기 일정 섹션
    st.header("📅 경기 일정")
    schedule_data = selected_motorsport.get("schedule", [])
    display_schedule(schedule_data)
    
    st.markdown("---")
    
    # 경기 결과 섹션
    st.header("🏆 경기 결과")
    results_data = selected_motorsport.get("results", [])
    display_results(results_data)
    
    st.markdown("---")
    
    # 드라이버 챔피언십 포인트 순위 섹션
    st.header("🏁 드라이버 챔피언십 포인트 순위")
    driver_championship_data = selected_motorsport.get("driver_championship", [])
    display_driver_championship(driver_championship_data)
    
    # 푸터
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "모터스포츠 정보 센터"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()

