import React from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Target, BarChart3 } from 'lucide-react';

const ModelResults = ({ results, salesPredictions = [] }) => {
  const getSurvivalColor = (probability) => {
    if (probability >= 70) return 'text-green-600';
    if (probability >= 50) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskColor = (score) => {
    if (score <= 30) return 'text-green-600';
    if (score <= 60) return 'text-yellow-600';
    return 'text-red-600';
  };

  const getRiskStatus = (score) => {
    if (score <= 30) return { 
      text: '낮음', 
      color: 'text-green-600', 
      bg: 'bg-green-100',
      cardBg: 'from-green-50 to-green-100',
      border: 'border-green-500',
      icon: 'text-green-600'
    };
    if (score <= 60) return { 
      text: '보통', 
      color: 'text-yellow-600', 
      bg: 'bg-yellow-100',
      cardBg: 'from-yellow-50 to-yellow-100',
      border: 'border-yellow-500',
      icon: 'text-yellow-600'
    };
    return { 
      text: '높음', 
      color: 'text-red-600', 
      bg: 'bg-red-100',
      cardBg: 'from-red-50 to-red-100',
      border: 'border-red-500',
      icon: 'text-red-600'
    };
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <Target className="text-indigo-600" size={24} />
        모델 예측 결과
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* 매출 트렌드 예측 - salesPredictions 기반 */}
        {salesPredictions && salesPredictions.length > 0 && (
          <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 border-l-4 border-blue-500 hover:shadow-lg transition-all duration-300">
            <div className="flex items-center gap-2 mb-2">
              <TrendingUp className="text-blue-600" size={20} />
              <h4 className="font-semibold text-gray-700">매출 트렌드</h4>
            </div>
            {(() => {
              const pred = salesPredictions[0]; // 1개월 후 예측
              const gradeDiff = pred.yhatGrade - pred.yT;
              let trendText = '유지';
              let trendColor = 'text-gray-600';
              let trendIcon = '➡️';
              
              if (gradeDiff <= -1) {
                trendText = '상승';
                trendColor = 'text-green-600';
                trendIcon = '📈';
              } else if (gradeDiff >= 1) {
                trendText = '하락';
                trendColor = 'text-red-600';
                trendIcon = '📉';
              }
              
              return (
                <>
                  <p className={`text-3xl font-bold ${trendColor} flex items-center gap-2`}>
                    <span>{trendIcon}</span>
                    <span>{trendText}</span>
                  </p>
                  <p className="text-sm text-gray-600 mt-1">
                    {pred.yT}구간 → {pred.yhatGrade}구간
                  </p>
                </>
              );
            })()}
          </div>
        )}

        {/* 생존 가능성 */}
        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4 border-l-4 border-green-500 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
          <div className="flex items-center gap-2 mb-2">
            <Target className="text-green-600" size={20} />
            <h4 className="font-semibold text-gray-700">생존 가능성</h4>
          </div>
          <p className={`text-2xl font-bold ${getSurvivalColor(results.survivalProbability)}`}>
            {Number(results.survivalProbability).toFixed(2)}%
          </p>
          <p className="text-sm text-gray-600">6개월 후</p>
        </div>

        {/* 위험도 점수 */}
        <div className={`bg-gradient-to-r ${getRiskStatus(results.riskScore).cardBg} rounded-lg p-4 border-l-4 ${getRiskStatus(results.riskScore).border} hover:shadow-lg transition-all duration-300 hover:-translate-y-1`}>
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className={getRiskStatus(results.riskScore).icon} size={20} />
            <h4 className="font-semibold text-gray-700">위험도 점수</h4>
          </div>
          <p className={`text-2xl font-bold ${getRiskColor(results.riskScore)}`}>
            {Number(results.riskScore).toFixed(2)}
          </p>
          <div className="flex items-center gap-2 mt-1">
            <span className={`text-xs px-2 py-1 rounded-full ${getRiskStatus(results.riskScore).bg} ${getRiskStatus(results.riskScore).color}`}>
              {getRiskStatus(results.riskScore).text}
            </span>
            <span className="text-sm text-gray-600">점 (0-100)</span>
          </div>
        </div>
      </div>

      {/* 매출 등급 예측 정보 */}
      {salesPredictions && salesPredictions.length > 0 && (
        <div className="mt-6">
          <h4 className="text-lg font-bold text-gray-700 mb-4 flex items-center gap-2">
            <BarChart3 className="text-indigo-600" size={20} />
            매출 등급 예측 (향후 1~3개월)
          </h4>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {salesPredictions.map((pred, idx) => {
              const getPredictionStatus = () => {
                const gradeDiff = pred.yhatGrade - pred.yT;
                if (gradeDiff <= -2) return { text: '상향', color: 'text-green-600', bg: 'bg-green-50', icon: '🔼' };
                if (gradeDiff >= 2) return { text: '악화', color: 'text-red-600', bg: 'bg-red-50', icon: '⚠️' };
                if (gradeDiff > 0) return { text: '하락', color: 'text-orange-600', bg: 'bg-orange-50', icon: '🔻' };
                if (gradeDiff < 0) return { text: '개선', color: 'text-blue-600', bg: 'bg-blue-50', icon: '✅' };
                return { text: '유지', color: 'text-gray-600', bg: 'bg-gray-50', icon: '➡️' };
              };

              const status = getPredictionStatus();
              const isHighRisk = pred.pLow56 >= 0.5 || pred.riskWorsenGe2 >= 0.3;

              return (
                <div 
                  key={idx} 
                  className={`${status.bg} rounded-lg p-4 border-2 ${isHighRisk ? 'border-red-300' : 'border-gray-200'} hover:shadow-md transition-all duration-200`}
                >
                  <div className="flex items-center justify-between mb-3">
                    <div>
                      <div className="text-sm font-semibold text-gray-500">
                        {pred.horizon}개월 후 ({pred.targetMonth})
                      </div>
                      <div className="text-xs text-gray-400">현재: {pred.yT}구간</div>
                    </div>
                    <span className="text-2xl">{status.icon}</span>
                  </div>

                  <div className="space-y-2">
                    <div className="flex items-baseline gap-2">
                      <span className="text-sm text-gray-600">예측 등급:</span>
                      <span className={`text-2xl font-bold ${status.color}`}>
                        {pred.yhatGrade}구간
                      </span>
                      <span className={`text-xs px-2 py-1 rounded-full ${status.bg} ${status.color} font-semibold`}>
                        {status.text}
                      </span>
                    </div>

                    <div className="text-xs text-gray-600 space-y-1 bg-white bg-opacity-50 rounded p-2">
                      <div className="flex justify-between">
                        <span>하위권 확률:</span>
                        <span className={`font-semibold ${pred.pLow56 >= 0.5 ? 'text-red-600' : 'text-gray-700'}`}>
                          {(pred.pLow56 * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>급락 위험:</span>
                        <span className={`font-semibold ${pred.riskWorsenGe2 >= 0.3 ? 'text-red-600' : 'text-gray-700'}`}>
                          {(pred.riskWorsenGe2 * 100).toFixed(1)}%
                        </span>
                      </div>
                      <div className="flex justify-between">
                        <span>예측 확률:</span>
                        <span className="font-semibold text-gray-700">
                          {(pred.yhatProb * 100).toFixed(1)}%
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>

          {/* 요약 메시지 */}
          {salesPredictions.length > 0 && (
            <div className="mt-4 bg-blue-50 border-l-4 border-blue-500 rounded-lg p-4">
              <p className="text-sm text-blue-800">
                {(() => {
                  const firstPred = salesPredictions[0];
                  const gradeDiff = firstPred.yhatGrade - firstPred.yT;
                  
                  if (firstPred.pLow56 >= 0.5 && firstPred.riskWorsenGe2 >= 0.3) {
                    return `⚠️ ${firstPred.targetMonth}에 ${firstPred.yhatGrade}구간으로 악화될 가능성이 있습니다. 하위권 확률 ${(firstPred.pLow56 * 100).toFixed(1)}%, 급락 위험 ${(firstPred.riskWorsenGe2 * 100).toFixed(1)}%로 높은 수준입니다.`;
                  } else if (firstPred.pLow56 < 0.2 && firstPred.riskWorsenGe2 < 0.1) {
                    return `✅ 향후 비교적 안정적일 것으로 예측됩니다. 하위권 확률 ${(firstPred.pLow56 * 100).toFixed(1)}%, 급락 위험 ${(firstPred.riskWorsenGe2 * 100).toFixed(1)}%로 낮은 수준입니다.`;
                  } else {
                    return `🏪 ${firstPred.horizon}개월 후 예상 매출 구간은 ${firstPred.yhatGrade}구간입니다. (현재 ${firstPred.yT} → 예측 ${firstPred.yhatGrade}, 하위권 확률 ${(firstPred.pLow56 * 100).toFixed(1)}%, 급락 위험 ${(firstPred.riskWorsenGe2 * 100).toFixed(1)}%)`;
                  }
                })()}
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default ModelResults;
