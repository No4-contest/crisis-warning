from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import franchise
from dotenv import load_dotenv
import os

# 환경 변수 로드
load_dotenv()

# FastAPI 앱 생성
app = FastAPI(
    title="가맹점 폐업 위험 분석 API",
    description="AI 기반 가맹점 상권 분석 및 생존 전략 제안 시스템",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React 개발 서버
        "http://localhost:3001",
        os.getenv("FRONTEND_URL", "http://localhost:3000")
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 라우터 등록
app.include_router(franchise.router)


@app.get("/")
async def root():
    """API 루트"""
    return {
        "message": "가맹점 폐업 위험 분석 API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """헬스 체크"""
    return {
        "status": "healthy",
        "service": "franchise-analysis-api"
    }


@app.on_event("startup")
async def startup_event():
    """앱 시작 시 실행"""
    print("=" * 50)
    print("🚀 가맹점 분석 API 서버 시작")
    print("=" * 50)
    
    # 데이터 로더 초기화
    from app.services.data_loader import data_loader
    try:
        data_loader.load_store_features()
        data_loader.load_store_diagnosis_results()
        data_loader.load_cluster_metadata()
        data_loader.load_feature_dictionary()
        data_loader.load_risk_checklist_rules()
        data_loader.load_store_monthly_timeseries()
        data_loader.load_sales_predict()
        print("✅ 모든 데이터 로드 완료")
    except Exception as e:
        print(f"⚠️  데이터 로드 중 오류: {e}")
    
    print("=" * 50)


@app.on_event("shutdown")
async def shutdown_event():
    """앱 종료 시 실행"""
    print("🛑 서버 종료")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )