import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import StatsCard from './components/StatsCard';
import ClusterIndicators from './components/ClusterIndicators';
import SalesDeclineChart from './components/Charts/SalesDeclineChart';
import ModelResults from './components/ModelResults';
import LLMSuggestion from './components/LLMSuggestion';
import { getFranchiseReport } from './services/api';
import { Store, FileText } from 'lucide-react';

function App() {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 가맹점 리포트 검색
  const handleSearch = async (franchiseId) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getFranchiseReport(franchiseId);
      setReportData(data);
    } catch (err) {
      setError(err.message);
      setReportData(null);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            📊 가맹점 리포트
          </h1>
          <p className="text-gray-600">
            AI 기반 가맹점 분석 및 맞춤형 전략 제안 시스템
          </p>
        </div>

        {/* 검색 폼 */}
        <SearchForm onSearch={handleSearch} loading={loading} />

        {/* 에러 메시지 */}
        {error && (
          <div className="mt-6 bg-red-50 border-2 border-red-300 rounded-lg p-4">
            <p className="text-red-800 font-semibold">⚠️ 오류가 발생했습니다</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
          </div>
        )}

        {/* 리포트 결과 */}
        {reportData && (
          <div className="mt-6 space-y-6 animate-fade-in">
            {/* 리포트 헤더 */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-indigo-500">
              <div className="flex items-center gap-3 mb-4">
                <FileText className="text-indigo-600" size={24} />
                <h2 className="text-2xl font-bold text-gray-800">
                  {reportData.storeInfo.name} 리포트
                </h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm text-gray-600">
                <div>
                  <span className="font-semibold">상권:</span> {reportData.storeInfo.tradingArea}
                </div>
                <div>
                  <span className="font-semibold">업종:</span> {reportData.storeInfo.industry}
                </div>
                <div>
                  <span className="font-semibold">클러스터:</span> {reportData.storeInfo.cluster}
                </div>
              </div>
            </div>

            {/* 기본 정보 카드들 */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <StatsCard
                type="location"
                title="상권 정보"
                value={reportData.storeInfo.tradingArea}
                subtitle={reportData.storeInfo.industry}
              />
              <StatsCard
                type="cluster"
                title="클러스터"
                value={reportData.storeInfo.cluster}
                subtitle={`폐업률 ${reportData.statistics.clusterClosureRate}%`}
              />
              <StatsCard
                type="traffic"
                title="유동인구"
                value={reportData.statistics.avgMonthlyFootTraffic.toLocaleString()}
                subtitle="월 평균"
              />
              <StatsCard
                type="risk"
                title="폐업 위험도"
                value={`${Number(reportData.storeInfo.closureRisk).toFixed(2)}%`}
                risk={Number(reportData.storeInfo.closureRisk)}
              />
            </div>

            {/* 모델 결과 */}
            <ModelResults results={reportData.modelResults} />

            {/* 클러스터별 주요 지표 */}
            <ClusterIndicators indicators={reportData.clusterIndicators} />

            {/* 매출 급감 예상 그래프 */}
            <SalesDeclineChart data={reportData.salesDeclineData} />

            {/* AI 전략 제안 */}
            <LLMSuggestion suggestion={reportData.llmSuggestion} />
          </div>
        )}

        {/* 초기 상태 안내 */}
        {!reportData && !loading && !error && (
          <div className="mt-12 bg-white rounded-xl shadow-lg p-12 text-center">
            <Store size={64} className="mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              가맹점 ID를 입력해주세요
            </h3>
            <p className="text-gray-500">
              가맹점 ID를 입력하면 상세한 분석 리포트와<br />
              AI 기반 맞춤형 전략을 제공해드립니다.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;