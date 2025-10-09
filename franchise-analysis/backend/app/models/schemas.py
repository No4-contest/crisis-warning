from pydantic import BaseModel, Field
from typing import List, Optional


# ============================================
# 요청 스키마
# ============================================

class NewStoreRequest(BaseModel):
    """신규 가맹점 정보 입력"""
    tradingArea: str = Field(..., description="상권명")
    industry: str = Field(..., description="업종")
    latitude: float = Field(..., description="위도")
    longitude: float = Field(..., description="경도")
    monthlyRent: Optional[float] = Field(None, description="월 임대료 (만원)")
    nearbyStores: Optional[int] = Field(None, description="경쟁 점포 수")
    footTraffic: Optional[int] = Field(None, description="월 평균 유동인구")
    rentIncreaseRate: Optional[float] = Field(None, description="임대료 상승률 (%)")
    salesGrowthRate: Optional[float] = Field(None, description="매출 성장률 (%)")


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


class AnalysisResponse(BaseModel):
    """전체 분석 응답"""
    storeInfo: StoreInfo
    statistics: Statistics
    comparisonData: List[ComparisonData]
    distributionData: List[DistributionData]
    riskFactors: List[RiskFactor]
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