# 🏎️ 모터스포츠 정보 센터

모터스포츠 정보를 한 곳에서 쉽게 확인할 수 있는 웹 애플리케이션입니다.

## 📋 프로젝트 개요

한국에서 모터스포츠가 대중화되지 않은 상황에서, 모터스포츠 팬들이 여러 플랫폼을 일일이 찾아다니지 않고도 한 곳에서 경기 일정, 결과, 공식 SNS 정보를 확인할 수 있도록 돕는 서비스입니다.

## ✨ 주요 기능

1. **모터스포츠 선택**: 원하는 모터스포츠를 선택할 수 있습니다.
2. **공식 SNS 바로가기**: 각 모터스포츠의 공식 웹사이트, YouTube, Instagram, Twitter/X로 바로 이동할 수 있습니다.
3. **경기 일정 확인**: 달력 형식으로 경기 일정을 월별로 확인할 수 있습니다.
4. **경기 결과 확인**: 지난 경기 결과와 시즌 누적 포인트를 표 형식으로 확인할 수 있습니다.

## 🛠️ 기술 스택

- **프로그래밍 언어**: Python 3.8+
- **프레임워크**: Streamlit
- **데이터 형식**: JSON
- **개발 도구**: Cursor AI

## 📦 설치 및 실행

### 1. 필요한 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 애플리케이션 실행

```bash
streamlit run app.py
```

브라우저에서 자동으로 열리며, 기본 주소는 `http://localhost:8501`입니다.

## 📁 프로젝트 구조

```
.
├── app.py                  # Streamlit 메인 애플리케이션
├── requirements.txt        # 필요한 Python 패키지 목록
├── README.md              # 프로젝트 설명서
└── data/
    └── motorsports.json    # 모터스포츠 데이터 (경기 일정, 결과, SNS 링크)
```

## 📊 데이터 관리

데이터는 `data/motorsports.json` 파일에 저장되며, 관리자가 직접 입력합니다.

### 데이터 구조 예시

```json
{
  "motorsports": [
    {
      "id": "f1",
      "name": "포뮬러 1 (F1)",
      "sns_links": {
        "official_website": "https://www.formula1.com/",
        "youtube": "https://www.youtube.com/@Formula1",
        "instagram": "https://www.instagram.com/f1/",
        "twitter": "https://twitter.com/F1"
      },
      "schedule": [
        {
          "date": "2024-10-27",
          "event": "US Grand Prix",
          "location": "Austin, USA"
        }
      ],
      "results": [
        {
          "date": "2024-10-20",
          "event": "Qatar Grand Prix",
          "winner": "Max Verstappen",
          "points": 25,
          "season_points": 524
        }
      ]
    }
  ]
}
```

### 데이터 추가 방법

1. `data/motorsports.json` 파일을 엽니다.
2. `motorsports` 배열에 새로운 모터스포츠 정보를 추가합니다.
3. 각 필드를 올바르게 입력합니다:
   - `id`: 고유 식별자 (영문 소문자, 언더스코어 사용)
   - `name`: 모터스포츠 이름
   - `sns_links`: 공식 SNS 링크들
   - `schedule`: 경기 일정 배열 (날짜 형식: YYYY-MM-DD)
   - `results`: 경기 결과 배열

## 🧪 테스트

### 예외 상황 테스트

1. **데이터 파일 없음**: `data/motorsports.json` 파일을 삭제하고 실행
2. **빈 데이터**: JSON 파일의 `motorsports` 배열을 비우고 실행
3. **잘못된 JSON 형식**: JSON 파일에 문법 오류를 추가하고 실행
4. **경기 일정/결과 없음**: 특정 모터스포츠의 `schedule` 또는 `results`를 빈 배열로 설정

## ⚠️ 주의사항

- 데이터는 관리자가 수동으로 입력해야 합니다.
- 날짜 형식은 반드시 `YYYY-MM-DD` 형식을 따라야 합니다.
- JSON 파일을 수정할 때는 문법 오류가 없도록 주의하세요.

## 📝 개발 일정

- 1차시: ChatGPT 프롬프트 작성 및 환경 구성
- 2~4차시: 개발
- 5~6차시: 코드 분석
- 7차시: 테스트
- 8차시: 배포

## 🚀 배포

Streamlit Cloud를 사용하여 배포할 수 있습니다:

1. GitHub에 프로젝트를 업로드합니다.
2. [Streamlit Cloud](https://streamlit.io/cloud)에 접속하여 로그인합니다.
3. "New app"을 클릭하고 GitHub 저장소를 선택합니다.
4. 메인 파일 경로를 `app.py`로 설정합니다.
5. 배포를 시작합니다.

## 📄 라이선스

이 프로젝트는 교육 목적으로 제작되었습니다.

## 👤 작성자

모터스포츠 정보 센터 개발팀

---

**모터스포츠를 사랑하는 모든 분들을 위해 만들어졌습니다. 🏎️💨**

