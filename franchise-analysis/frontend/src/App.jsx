import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import StatsCard from './components/StatsCard';
import ComparisonChart from './components/Charts/ComparisonChart';
import DistributionChart from './components/Charts/DistributionChart';
import RiskFactors from './components/RiskFactors';
import LLMSuggestion from './components/LLMSuggestion';
import { getFranchiseAnalysis, predictNewStore } from './services/api';
import { Store } from 'lucide-react';

function App() {
  const [mode, setMode] = useState('existing'); // 'existing' or 'new'
  const [analysisData, setAnalysisData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // 기존 가맹점 검색
  const handleSearch = async (franchiseId) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await getFranchiseAnalysis(franchiseId);
      setAnalysisData(data);
    } catch (err) {
      setError(err.message);
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  // 신규 가맹점 분석
  const handleNewStoreSubmit = async (formData) => {
    setLoading(true);
    setError(null);
    
    try {
      const data = await predictNewStore(formData);
      setAnalysisData(data);
    } catch (err) {
      setError(err.message);
      setAnalysisData(null);
    } finally {
      setLoading(false);
    }
  };

  // 모드 변경 시 데이터 초기화
  const handleModeChange = (newMode) => {
    setMode(newMode);
    setAnalysisData(null);
    setError(null);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-6">
      <div className="max-w-7xl mx-auto">
        {/* 헤더 */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            🏪 가맹점 폐업 위험 분석
          </h1>
          <p className="text-gray-600">
            AI 기반 상권 분석 및 생존 전략 제안 시스템
          </p>
        </div>

        {/* 모드 선택 */}
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => handleModeChange('existing')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition ${
              mode === 'existing'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            기존 가맹점 조회
          </button>
          <button
            onClick={() => handleModeChange('new')}
            className={`flex-1 py-3 px-6 rounded-lg font-semibold transition ${
              mode === 'new'
                ? 'bg-indigo-600 text-white shadow-lg'
                : 'bg-white text-gray-600 hover:bg-gray-50'
            }`}
          >
            신규 입점 분석
          </button>
        </div>

        {/* 검색/입력 폼 */}
        <SearchForm
          mode={mode}
          onSearch={handleSearch}
          onNewStoreSubmit={handleNewStoreSubmit}
          loading={loading}
        />

        {/* 에러 메시지 */}
        {error && (
          <div className="mt-6 bg-red-50 border-2 border-red-300 rounded-lg p-4">
            <p className="text-red-800 font-semibold">⚠️ 오류가 발생했습니다</p>
            <p className="text-red-600 text-sm mt-1">{error}</p>
          </div>
        )}

        {/* 분석 결과 */}
        {analysisData && (
          <div className="mt-6 space-y-6 animate-fade-in">
            {/* 기본 정보 카드들 */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
              <StatsCard
                type="location"
                title="상권 정보"
                value={analysisData.storeInfo.tradingArea}
                subtitle={analysisData.storeInfo.industry}
              />
              <StatsCard
                type="cluster"
                title="클러스터"
                value={analysisData.storeInfo.cluster}
                subtitle={`폐업률 ${analysisData.statistics.clusterClosureRate}%`}
              />
              <StatsCard
                type="traffic"
                title="유동인구"
                value={analysisData.statistics.avgMonthlyFootTraffic.toLocaleString()}
                subtitle="월 평균"
              />
              <StatsCard
                type="risk"
                title="폐업 위험도"
                value={`${analysisData.storeInfo.closureRisk}%`}
                risk={analysisData.storeInfo.closureRisk}
              />
            </div>

            {/* 주요 변수 비교 차트 */}
            {analysisData.comparisonData && (
              <ComparisonChart data={analysisData.comparisonData} />
            )}

            {/* 분포 차트 */}
            {analysisData.distributionData && (
              <DistributionChart data={analysisData.distributionData} />
            )}

            {/* 위험 요인 */}
            {analysisData.riskFactors && (
              <RiskFactors factors={analysisData.riskFactors} />
            )}

            {/* AI 전략 제안 */}
            {analysisData.llmSuggestion && (
              <LLMSuggestion suggestion={analysisData.llmSuggestion} />
            )}
          </div>
        )}

        {/* 초기 상태 안내 */}
        {!analysisData && !loading && !error && (
          <div className="mt-12 bg-white rounded-xl shadow-lg p-12 text-center">
            <Store size={64} className="mx-auto text-gray-300 mb-4" />
            <h3 className="text-xl font-semibold text-gray-600 mb-2">
              가맹점 정보를 입력해주세요
            </h3>
            <p className="text-gray-500">
              기존 가맹점 ID를 조회하거나 신규 입점 정보를 입력하면<br />
              AI가 자동으로 상권을 분석하고 전략을 제안해드립니다.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;