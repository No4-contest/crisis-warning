from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    AnalysisResponse, 
    NewStoreRequest, 
    ErrorResponse,
    StoreInfo,
    Statistics,
    ComparisonData,
    DistributionData,
    RiskFactor,
    LLMSuggestion
)
from app.services.analyzer import analyzer
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api/franchise", tags=["franchise"])


@router.get("/{franchise_id}", response_model=AnalysisResponse)
async def get_franchise_analysis(franchise_id: str):
    """
    기존 가맹점 종합 분석
    
    - **franchise_id**: 가맹점 ID (예: FR-12345)
    """
    try:
        # 1. 데이터 분석
        analysis = analyzer.analyze_franchise(franchise_id)
        
        # 2. LLM 전략 제안
        llm_result = llm_service.generate_strategy(analysis)
        
        # 3. 응답 구성
        franchise = analysis['franchise']
        cluster_stats = analysis['cluster_stats']
        industry_stats = analysis['industry_stats'] or {}
        
        response = AnalysisResponse(
            storeInfo=StoreInfo(
                id=franchise['franchise_id'],
                name=franchise.get('name', ''),
                tradingArea=franchise['trading_area'],
                industry=franchise['industry'],
                cluster=f"{cluster_stats['cluster_id']} ({cluster_stats['cluster_name']})",
                latitude=franchise['latitude'],
                longitude=franchise['longitude'],
                closureRisk=float(franchise['closure_risk'])
            ),
            statistics=Statistics(
                clusterClosureRate=float(cluster_stats.get('closure_rate', 0)),
                industryAvgClosureRate=float(industry_stats.get('closure_rate', 0)),
                nearbyStores=int(franchise.get('nearby_stores', 0)),
                avgMonthlyFootTraffic=int(franchise.get('foot_traffic', 0)),
                rentIncreaseRate=float(franchise.get('rent_increase_rate', 0))
            ),
            comparisonData=[
                ComparisonData(**item) for item in analysis['comparison_data']
            ],
            distributionData=[
                DistributionData(**item) for item in analysis['distribution_data']
            ],
            riskFactors=[
                RiskFactor(**item) for item in analysis['risk_factors']
            ],
            llmSuggestion=LLMSuggestion(
                summary=llm_result['summary'],
                strategies=llm_result['strategies']
            )
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류 발생: {str(e)}")


@router.post("/predict", response_model=AnalysisResponse)
async def predict_new_store(request: NewStoreRequest):
    """
    신규 가맹점 클러스터 예측 및 분석
    
    - **request**: 신규 점포 정보 (상권, 업종, 위치 등)
    """
    try:
        # 1. 신규 점포 분석
        store_data = request.dict()
        analysis = analyzer.predict_new_store(store_data)
        
        # 2. LLM 전략 제안
        llm_result = llm_service.generate_strategy(analysis)
        
        # 3. 응답 구성
        franchise = analysis['franchise']
        cluster_stats = analysis['cluster_stats']
        industry_stats = analysis['industry_stats'] or {}
        
        response = AnalysisResponse(
            storeInfo=StoreInfo(
                id=franchise['franchise_id'],
                name=franchise['name'],
                tradingArea=franchise['trading_area'],
                industry=franchise['industry'],
                cluster=f"{cluster_stats['cluster_id']} ({cluster_stats.get('cluster_name', '미분류')})",
                latitude=franchise['latitude'],
                longitude=franchise['longitude'],
                closureRisk=float(franchise['closure_risk'])
            ),
            statistics=Statistics(
                clusterClosureRate=float(cluster_stats.get('closure_rate', 0)),
                industryAvgClosureRate=float(industry_stats.get('closure_rate', 0)),
                nearbyStores=int(franchise.get('nearby_stores', 0)),
                avgMonthlyFootTraffic=int(cluster_stats.get('avg_foot_traffic', 0)),
                rentIncreaseRate=float(store_data.get('rentIncreaseRate', 0))
            ),
            comparisonData=[
                ComparisonData(**item) for item in analysis['comparison_data']
            ],
            distributionData=[
                DistributionData(**item) for item in analysis['distribution_data']
            ],
            riskFactors=[
                RiskFactor(**item) for item in analysis['risk_factors']
            ],
            llmSuggestion=LLMSuggestion(
                summary=llm_result['summary'],
                strategies=llm_result['strategies']
            )
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"예측 중 오류 발생: {str(e)}")