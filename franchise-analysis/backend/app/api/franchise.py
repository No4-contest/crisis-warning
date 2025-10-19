from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    FranchiseReportResponse,
    FranchiseReportRequest,
    ErrorResponse,
    StoreInfo,
    Statistics,
    ModelResults,
    ClusterIndicator,
    SalesDeclineData,
    LLMSuggestion
)
from app.services.analyzer import analyzer
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api/franchise", tags=["franchise"])


@router.get("/report/{franchise_id}", response_model=FranchiseReportResponse)
async def get_franchise_report(franchise_id: str):
    """
    가맹점 리포트 생성
    
    - **franchise_id**: 가맹점 ID (예: FR-12345)
    """
    try:
        # 1. 리포트 데이터 생성
        report_data = analyzer.generate_franchise_report(franchise_id)
        
        # 2. LLM 전략 제안
        llm_result = llm_service.generate_strategy(report_data)
        
        # 3. 응답 구성
        franchise = report_data['franchise']
        cluster_stats = report_data['cluster_stats']
        industry_stats = report_data['industry_stats'] or {}
        
        response = FranchiseReportResponse(
            storeInfo=StoreInfo(
                id=franchise['franchise_id'],
                name=franchise.get('name', ''),
                tradingArea=franchise['trading_area'],
                industry=franchise['industry'],
                cluster=f"{cluster_stats['cluster_id']} ({cluster_stats['cluster_name']})",
                latitude=franchise['latitude'],
                longitude=franchise['longitude'],
                closureRisk=float(franchise['risk_score'])
            ),
            modelResults=ModelResults(
                salesPrediction=float(report_data['model_results']['sales_prediction']),
                eventPrediction=report_data['model_results']['event_prediction'],
                survivalProbability=float(report_data['model_results']['survival_probability']),
                riskScore=float(report_data['model_results']['risk_score'])
            ),
            clusterIndicators=[
                ClusterIndicator(**item) for item in report_data['cluster_indicators']
            ],
            salesDeclineData=[
                SalesDeclineData(**item) for item in report_data['sales_decline_data']
            ],
            statistics=Statistics(
                clusterClosureRate=float(cluster_stats.get('closure_rate', 0)),
                industryAvgClosureRate=float(industry_stats.get('closure_rate', 0)),
                nearbyStores=int(franchise.get('nearby_stores', 0)),
                avgMonthlyFootTraffic=int(franchise.get('foot_traffic', 0)),
                rentIncreaseRate=float(franchise.get('rent_increase_rate', 0))
            ),
            llmSuggestion=LLMSuggestion(
                summary=llm_result['summary'],
                strategies=llm_result['strategies']
            )
        )
        
        return response
        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"리포트 생성 중 오류 발생: {str(e)}")
