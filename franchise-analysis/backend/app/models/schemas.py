from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


# ============================================
# 요청 스키마
# ============================================

class FranchiseReportRequest(BaseModel):
    """가맹점 리포트 조회 요청"""
    franchiseId: str = Field(..., description="가맹점 ID")


# ============================================
# 응답 스키마
# ============================================

class StoreInfo(BaseModel):
    """가맹점 기본 정보"""
    id: str
    name: str
    tradingArea: str
    industry: str
    cluster: str
    latitude: float
    longitude: float
    closureRisk: float


class ModelResults(BaseModel):
    """모델 예측 결과"""
    salesPrediction: float = Field(..., description="매출 예측값")
    eventPrediction: str = Field(..., description="이벤트 예측 (예: 매출 급감, 경쟁 심화 등)")
    survivalProbability: float = Field(..., description="생존 가능성 (0-100%)")
    riskScore: float = Field(..., description="위험도 점수")


class ClusterIndicator(BaseModel):
    """클러스터별 주요 지표"""
    name: str = Field(..., description="지표명")
    value: float = Field(..., description="현재값")
    clusterAvg: float = Field(..., description="클러스터 평균")
    unit: str = Field(..., description="단위")
    description: str = Field(..., description="지표 설명")
    isPositive: bool = Field(..., description="높을수록 좋은 지표인지")


class SalesDeclineData(BaseModel):
    """매출 급감 예상 그래프 데이터"""
    month: str
    predictedSales: float
    currentSales: Optional[float] = None


class Statistics(BaseModel):
    """통계 정보"""
    clusterClosureRate: float
    industryAvgClosureRate: float
    nearbyStores: int
    avgMonthlyFootTraffic: int
    rentIncreaseRate: float


class ComparisonData(BaseModel):
    """비교 데이터 (차트용)"""
    variable: str
    myStore: float
    clusterAvg: float
    unit: str


class DistributionData(BaseModel):
    """분포 데이터"""
    range: str
    myStore: int
    cluster: int


class RiskFactor(BaseModel):
    """위험 요인"""
    factor: str
    severity: str  # 'high', 'medium', 'low'
    description: str
    value: Optional[str] = None
    benchmark: Optional[str] = None


class LLMSuggestion(BaseModel):
    """LLM 전략 제안"""
    summary: str
    strategies: List[str]


class FranchiseReportResponse(BaseModel):
    """가맹점 리포트 응답"""
    storeInfo: StoreInfo
    modelResults: ModelResults
    clusterIndicators: List[ClusterIndicator]
    salesDeclineData: List[SalesDeclineData]
    statistics: Statistics
    llmSuggestion: LLMSuggestion


# ============================================
# 기타 스키마
# ============================================

class ErrorResponse(BaseModel):
    """에러 응답"""
    detail: str
    code: Optional[str] = None


class ClusterInfo(BaseModel):
    """클러스터 정보"""
    cluster_id: str
    cluster_name: str
    total_stores: int
    closure_rate: float
    avg_foot_traffic: float
    avg_rent: float