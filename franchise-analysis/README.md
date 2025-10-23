# 🏪 가맹점 폐업 위험 분석 시스템

AI 기반 상권 진단 및 생존 전략 제안 웹 서비스  
> 가맹점별 폐업 위험도를 예측하고, 주요 리스크 요인과 개선 전략을 자동으로 제시합니다.

---

## 📋 목차
1. [프로젝트 개요](#프로젝트-개요)
2. [프로젝트 구조](#프로젝트-구조)
3. [설치 및 실행](#설치-및-실행)
4. [데이터 구성](#데이터-구성)
5. [API 문서](#api-문서)
6. [문제 해결](#문제-해결)

---

## 💡 프로젝트 개요

이 시스템은 **가맹점의 폐업 위험도를 예측**하고,  
**클러스터별 특성과 리스크 진단 결과를 기반으로 전략을 제안**하는 AI 웹 서비스입니다.  

- **모델 기반 분석:** 매출·임대료·유동인구 등 주요 지표를 활용  
- **리스크 진단:** 규칙 기반 진단표(Rule-based Checklist)와 통계 지표 비교  
- **AI 전략 제안:** LLM을 통해 가맹점별 맞춤형 개선 전략 제시  
- **시각화 대시보드:** 클러스터 지표, 리스크 요인, 매출 추이 등 시각적 분석 제공  

---

## 📂 프로젝트 구조

```
franchise-analysis/
├── backend/ # FastAPI 백엔드
│ ├── app/
│ │ ├── api/ # API 엔드포인트
│ │ │ └── init.py
│ │ ├── models/ # 데이터 스키마
│ │ │ ├── schemas.py
│ │ │ └── init.py
│ │ ├── services/ # 비즈니스 로직
│ │ │ ├── analyzer.py # 리스크 진단 및 클러스터 분석
│ │ │ ├── data_loader.py # 데이터 로드/캐싱
│ │ │ ├── llm_service.py # LLM 기반 전략 제안
│ │ │ └── init.py
│ │ ├── main.py # FastAPI 진입점
│ │ └── init.py
│ ├── data/ # 분석용 데이터
│ │ ├── final_features_per_store.csv
│ │ ├── risk_checklist_rules.csv
│ │ ├── sales_predict_result.csv
│ │ ├── store_diagnosis_results.csv
│ │ └── store_monthly_timeseries.csv
│ ├── requirements.txt
│ └── .env
│
└── frontend/ # React 프론트엔드
├── public/
│ └── index.html
├── src/
│ ├── components/
│ │ ├── Charts/ # 그래프 시각화 컴포넌트
│ │ │ ├── ComparisonChart.jsx
│ │ │ ├── DistributionChart.jsx
│ │ │ ├── SalesDeclineChart.jsx
│ │ │ └── TrendLineChart.jsx
│ │ ├── ClusterIndicators.jsx
│ │ ├── LLMSuggestion.jsx
│ │ ├── ModelResults.jsx
│ │ ├── RiskFactors.jsx
│ │ ├── RiskIndicators.jsx
│ │ ├── SearchForm.jsx
│ │ ├── StatsCard.jsx
│ │ └── ViolationsTable.jsx
│ ├── services/
│ │ └── api.js
│ ├── App.jsx
│ ├── index.css
│ └── index.jsx
├── package.json
└── .env
```


---

## ⚙️ 설치 및 실행

### 1️⃣ 백엔드

```bash
cd backend

# 가상환경 생성 및 활성화
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)

# 패키지 설치
pip install -r requirements.txt

# 환경 변수 설정
cp .env.example .env

# 서버 실행
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- API 문서: http://localhost:8000/docs
- Swagger UI 제공


### 2️⃣ 프론트엔드 설치 및 실행

```bash
cd frontend

# 패키지 설치
npm install

# 환경 변수 설정
cp .env.example .env

# 개발 서버 실행
npm start
```

- 웹 앱 접속: http://localhost:3000

## 📊 데이터 구성

| 파일명 | 설명 |
|--------|------|
| `final_features_per_store.csv` | 각 가맹점의 주요 피처 |
| `risk_checklist_rules.csv` | 리스크 점검표 (규칙 기반 진단용) |
| `sales_predict_result.csv` | 매출 예측 결과 |
| `store_diagnosis_results.csv` | 가맹점별 진단 결과 |
| `store_monthly_timeseries.csv` | 월별 시계열 데이터 |

---

## 📡 API 문서

| 기능 | 엔드포인트 | 메서드 | 설명 |
|------|-------------|--------|------|
| 가맹점 진단 조회 | `/api/franchise/{store_id}` | `GET` | 특정 가맹점의 위험도 및 리스크 요인 조회 |
| 신규 가맹점 진단 | `/api/franchise/predict` | `POST` | 신규 점포의 예상 위험도 및 전략 제안 |
| 클러스터 통계 조회 | `/api/cluster/{cluster_id}` | `GET` | 상권 클러스터별 평균 지표 제공 |

---

## 🔑 환경 변수 설정

### 백엔드 (.env)
```
# LLM API 키 (둘 중 하나만 설정)
OPENAI_API_KEY=sk-

# 또는
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# CORS 설정
FRONTEND_URL=http://localhost:3000

# 데이터 디렉토리 (선택사항, 기본값 사용 가능)
DATA_DIR=./data
MODELS_DIR=./models
```


### 프론트엔드 (.env)
```
# 백엔드 API URL
REACT_APP_API_URL=http://localhost:8000

# 개발 환경 설정
NODE_ENV=development
```

