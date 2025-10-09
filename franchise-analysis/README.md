# 🏪 가맹점 폐업 위험 분석 시스템

AI 기반 상권 분석 및 생존 전략 제안 웹 서비스

---

## 📋 목차
1. [프로젝트 구조](#프로젝트-구조)
2. [설치 방법](#설치-방법)
3. [실행 방법](#실행-방법)
4. [CSV 데이터 준비](#csv-데이터-준비)
5. [API 문서](#api-문서)

---

## 📂 프로젝트 구조

```
franchise-analysis/
├── backend/                    # FastAPI 백엔드
│   ├── app/
│   │   ├── main.py            # 메인 앱
│   │   ├── api/
│   │   │   └── franchise.py   # API 엔드포인트
│   │   ├── services/
│   │   │   ├── data_loader.py # CSV 로더
│   │   │   ├── analyzer.py    # 분석 로직
│   │   │   └── llm_service.py # LLM 서비스
│   │   └── models/
│   │       └── schemas.py     # 데이터 스키마
│   ├── data/                  # CSV 데이터 파일
│   │   ├── franchises.csv
│   │   ├── clusters.csv
│   │   └── statistics.csv
│   ├── models/                # 학습된 모델
│   │   ├── cluster_model.pkl
│   │   └── scaler.pkl
│   ├── requirements.txt
│   └── .env
│
└── frontend/                  # React 프론트엔드
    ├── src/
    │   ├── components/
    │   ├── services/
    │   └── App.jsx
    ├── package.json
    └── .env
```

---

## 🛠️ 설치 방법

### 1️⃣ 백엔드 설치

```bash
cd backend

# 가상환경 생성
python -m venv venv

# 가상환경 활성화
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 패키지 설치
pip install -r requirements.txt
```

### 2️⃣ 프론트엔드 설치

```bash
cd frontend

# 패키지 설치
npm install
```

---

## 🚀 실행 방법

### 1️⃣ 백엔드 실행

```bash
cd backend

# 환경 변수 설정 (.env 파일 생성)
cp .env.example .env
# .env 파일 편집하여 API 키 입력

# 서버 실행
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**접속 주소:**
- API 서버: http://localhost:8000
- API 문서: http://localhost:8000/docs

### 2️⃣ 프론트엔드 실행

```bash
cd frontend

# 환경 변수 설정
cp .env.example .env

# 개발 서버 실행
npm start
```

**접속 주소:**
- 웹 앱: http://localhost:3000

---

## 📊 CSV 데이터 준비

### 1. `backend/data/franchises.csv`

**필수 컬럼:**
```csv
franchise_id,name,trading_area,industry,latitude,longitude,cluster_id,is_closed,closure_risk,monthly_rent,nearby_stores,foot_traffic,foot_traffic_change_rate,sales_growth_rate,rent_increase_rate
FR-12345,강남점,강남역 상권,카페,37.4979,127.0276,C-3,0,72,350,45,125000,-15,5,12
```

**컬럼 설명:**
- `franchise_id`: 가맹점 고유 ID
- `name`: 점포명
- `trading_area`: 상권명
- `industry`: 업종
- `latitude`, `longitude`: 좌표
- `cluster_id`: 클러스터 ID (C-1, C-2 형식)
- `is_closed`: 폐업 여부 (0=생존, 1=폐업)
- `closure_risk`: 폐업 위험도 (0-100)
- `monthly_rent`: 월 임대료 (만원)
- `nearby_stores`: 경쟁 점포 수
- `foot_traffic`: 유동인구
- `foot_traffic_change_rate`: 유동인구 변화율 (%)
- `sales_growth_rate`: 매출 성장률 (%)
- `rent_increase_rate`: 임대료 상승률 (%)

### 2. `backend/data/clusters.csv`

```csv
cluster_id,cluster_name,total_stores,closure_rate,avg_foot_traffic,avg_rent,avg_nearby_stores,avg_foot_traffic_change_rate,avg_sales_growth_rate,avg_rent_increase_rate
C-1,홍대 고밀도 상권,234,22.5,105000,320,42,-5,3.2,8
C-2,주거지역 밀집,189,18.3,78000,180,28,-2,5.1,6
C-3,강남 프리미엄,156,15.2,145000,420,38,-3,8.5,12
```

### 3. `backend/models/cluster_model.pkl` (학습된 모델)

**모델 생성 예시:**
```python
import pickle
from sklearn.cluster import KMeans
import pandas as pd

# 데이터 로드 및 학습
df = pd.read_csv('data/franchises.csv')
features = df[['latitude', 'longitude', 'monthly_rent', 'nearby_stores', 'foot_traffic']]

model = KMeans(n_clusters=4, random_state=42)
model.fit(features)

# 모델 저장
with open('models/cluster_model.pkl', 'wb') as f:
    pickle.dump(model, f)
```

---

## 📡 API 문서

### 1. 기존 가맹점 조회

**엔드포인트:** `GET /api/franchise/{franchise_id}`

**응답 예시:**
```json
{
  "storeInfo": {
    "id": "FR-12345",
    "name": "강남점",
    "closureRisk": 72.0
  },
  "statistics": {
    "clusterClosureRate": 18.5
  },
  "comparisonData": [...],
  "riskFactors": [...],
  "llmSuggestion": {
    "summary": "이 가맹점은 고위험군입니다.",
    "strategies": [...]
  }
}
```

### 2. 신규 가맹점 예측

**엔드포인트:** `POST /api/franchise/predict`

**요청 바디:**
```json
{
  "tradingArea": "강남역 상권",
  "industry": "카페",
  "latitude": 37.4979,
  "longitude": 127.0276,
  "monthlyRent": 350,
  "nearbyStores": 45
}
```

---

## 🔑 환경 변수 설정

### 백엔드 (.env)
```bash
OPENAI_API_KEY=sk-...
# 또는
ANTHROPIC_API_KEY=sk-ant-...

FRONTEND_URL=http://localhost:3000
```

### 프론트엔드 (.env)
```bash
REACT_APP_API_URL=http://localhost:8000
```

---

## 🐛 문제 해결

### 1. CSV 파일을 찾을 수 없습니다
→ `backend/data/` 폴더에 CSV 파일들이 있는지 확인

### 2. 모델 파일을 찾을 수 없습니다
→ `backend/models/` 폴더에 `cluster_model.pkl` 파일 생성

### 3. CORS 에러
→ 백엔드 `.env`의 `FRONTEND_URL` 확인

### 4. LLM API 호출 실패
→ API 키가 없어도 기본 전략이 제공됩니다

---

## 📞 문의

문제가 발생하면 이슈를 등록해주세요!