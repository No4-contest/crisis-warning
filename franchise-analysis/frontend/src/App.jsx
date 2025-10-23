import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import StatsCard from './components/StatsCard';
import RiskIndicators from './components/RiskIndicators';
import TrendLineChart from './components/Charts/TrendLineChart';
import ModelResults from './components/ModelResults';
import LLMSuggestion from './components/LLMSuggestion';
import { getFranchiseReport } from './services/api';
import { Store, FileText, AlertTriangle } from 'lucide-react';

function App() {
  const [reportData, setReportData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 가맹점 리포트 검색
  const handleSearch = async (storeId) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getFranchiseReport(storeId);
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

        {/* 로딩 오버레이 */}
        {loading && (
          <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
            <div className="bg-white rounded-lg p-8 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto mb-4"></div>
              <p className="text-gray-600">분석 중입니다...</p>
            </div>
          </div>
        )}

        {/* 리포트 결과 */}
        {reportData && (
          <div className="mt-6 space-y-6 animate-fade-in">
            {/* 1. 상단 공통 정보 영역 */}
            <div className="bg-white rounded-xl shadow-lg p-6 border-l-4 border-indigo-500 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
              <div className="flex items-center gap-3 mb-4">
                <FileText className="text-indigo-600" size={24} />
                <h2 className="text-2xl font-bold text-gray-800">
                  {reportData.storeInfo.name} 리포트
                </h2>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="bg-blue-50 rounded-lg p-4 hover:bg-blue-100 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5">
                  <div className="text-sm text-blue-600 font-semibold">가맹점명</div>
                  <div className="text-lg font-bold text-blue-800">{reportData.storeInfo.name}</div>
                </div>
                <div className="bg-green-50 rounded-lg p-4 hover:bg-green-100 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5">
                  <div className="text-sm text-green-600 font-semibold">클러스터</div>
                  <div className="text-lg font-bold text-green-800">{reportData.storeInfo.clusterName}</div>
                </div>
                <div className="bg-purple-50 rounded-lg p-4 hover:bg-purple-100 transition-all duration-200 hover:shadow-md hover:-translate-y-0.5">
                  <div className="text-sm text-purple-600 font-semibold">상권</div>
                  <div className="text-lg font-bold text-purple-800">{reportData.storeInfo.tradingArea}</div>
                </div>
              </div>
            </div>

            {/* 2. 모델 진단 결과 영역 */}
            <ModelResults 
              results={reportData.modelResults} 
              salesPredictions={reportData.salesPredictions}
            />

            {/* 3. 위험 지표 현황 (위반된 룰 + 클러스터 지표 통합) */}
            <RiskIndicators 
              violations={reportData.ruleViolations}
              indicators={reportData.clusterIndicators}
            />

            {/* 4. 트렌드 그래프 영역 */}
            <TrendLineChart data={reportData.trendData} />

            {/* 6. 전략 제안 영역 */}
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