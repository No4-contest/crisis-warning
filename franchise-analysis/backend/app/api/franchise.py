from fastapi import APIRouter, HTTPException
from app.models.schemas import (
    FranchiseReportResponse,
    FranchiseReportRequest,
    ErrorResponse,
    StoreInfo,
    Statistics,
    ModelResults,
    ClusterIndicator,
    TrendData,
    RuleViolation,
    SalesPrediction,
    LLMSuggestion
)
from app.services.analyzer import analyzer
from app.services.llm_service import llm_service

router = APIRouter(prefix="/api/franchise", tags=["franchise"])


@router.get("/report/{store_id}", response_model=FranchiseReportResponse)
async def get_franchise_report(store_id: str):
    """
    가맹점 리포트 생성
    
    - **store_id**: 점포 ID (예: 000F03E44A)
    """
    try:
        # 1. 리포트 데이터 생성
        report_data = analyzer.generate_franchise_report(store_id)
        
        # 2. LLM 전략 제안
        print(f"🔍 디버깅: LLM 전략 생성 시작")
        llm_result = llm_service.generate_strategy(report_data)
        print(f"🔍 디버깅: llm_result = {llm_result}")
        
        # 3. 응답 구성
        store_data = report_data['store_data']
        location_info = report_data['location_info'] or {}
        cluster_metadata = report_data['cluster_metadata'] or {}
        diagnosis_results = report_data['diagnosis_results'] or {}
        
        # 위험도 레벨 결정
        risk_score = diagnosis_results.get('total_risk_score', 50)
        if risk_score >= 80:
            risk_level = '치명적'
        elif risk_score >= 60:
            risk_level = '높음'
        elif risk_score >= 40:
            risk_level = '중간'
        else:
            risk_level = '낮음'
        
        response = FranchiseReportResponse(
            storeInfo=StoreInfo(
                id=store_data['store_id'],
                name=store_data.get('store_name', ''),
                tradingArea=location_info.get('business_district', ''),
                industry=store_data.get('industry', ''),
                cluster=str(store_data.get('static_cluster', '0')),
                clusterName=cluster_metadata.get('cluster_name', f'클러스터 {store_data.get("static_cluster", "0")}'),
                latitude=float(store_data.get('x', 0)),
                longitude=float(store_data.get('y', 0)),
                riskLevel=risk_level,
                riskScore=float(risk_score)
            ),
            modelResults=ModelResults(
                salesPrediction=float(report_data['model_results']['sales_prediction']),
                eventPrediction=report_data['model_results']['event_prediction'],
                survivalProbability=float(report_data['model_results']['survival_probability']),
                riskScore=float(report_data['model_results']['risk_score'])
            ),
            ruleViolations=[
                RuleViolation(**violation) for violation in report_data['rule_violations']
            ],
            clusterIndicators=[
                ClusterIndicator(**item) for item in report_data['cluster_indicators']
            ],
            trendData=[
                TrendData(**item) for item in report_data['trend_data']
            ],
            salesPredictions=[
                SalesPrediction(
                    targetMonth=pred['target_month'],
                    horizon=int(pred['horizon']),
                    yhatGrade=int(pred['yhat_grade']),
                    yhatProb=float(pred['yhat_prob']),
                    pLow56=float(pred['p_low56']),
                    riskWorsenGe2=float(pred['risk_worsen_ge2']),
                    yT=int(pred['y_t'])
                ) for pred in report_data['sales_predictions']
            ],
            statistics=Statistics(
                clusterClosureRate=float(cluster_metadata.get('closure_rate', 0)),
                industryAvgClosureRate=15.0,  # 기본값
                nearbyStores=int(store_data.get('nearby_stores', 0)),
                avgMonthlyFootTraffic=int(store_data.get('foot_traffic', 0)),
                rentIncreaseRate=float(store_data.get('rent_increase_rate', 0))
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
