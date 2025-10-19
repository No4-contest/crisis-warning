import React from 'react';
import { TrendingUp, TrendingDown, AlertTriangle, Target } from 'lucide-react';

const ModelResults = ({ results }) => {
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

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <Target className="text-indigo-600" size={24} />
        모델 예측 결과
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* 매출 예측 */}
        <div className="bg-gradient-to-r from-blue-50 to-blue-100 rounded-lg p-4 border-l-4 border-blue-500">
          <div className="flex items-center gap-2 mb-2">
            <TrendingUp className="text-blue-600" size={20} />
            <h4 className="font-semibold text-gray-700">매출 예측</h4>
          </div>
          <p className="text-2xl font-bold text-blue-600">
            {Number(results.salesPrediction).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </p>
          <p className="text-sm text-gray-600">만원</p>
        </div>

        {/* 이벤트 예측 */}
        <div className="bg-gradient-to-r from-purple-50 to-purple-100 rounded-lg p-4 border-l-4 border-purple-500">
          <div className="flex items-center gap-2 mb-2">
            <AlertTriangle className="text-purple-600" size={20} />
            <h4 className="font-semibold text-gray-700">이벤트 예측</h4>
          </div>
          <p className="text-lg font-bold text-purple-600">
            {results.eventPrediction}
          </p>
        </div>

        {/* 생존 가능성 */}
        <div className="bg-gradient-to-r from-green-50 to-green-100 rounded-lg p-4 border-l-4 border-green-500">
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
        <div className="bg-gradient-to-r from-red-50 to-red-100 rounded-lg p-4 border-l-4 border-red-500">
          <div className="flex items-center gap-2 mb-2">
            <TrendingDown className="text-red-600" size={20} />
            <h4 className="font-semibold text-gray-700">위험도 점수</h4>
          </div>
          <p className={`text-2xl font-bold ${getRiskColor(results.riskScore)}`}>
            {Number(results.riskScore).toFixed(2)}
          </p>
          <p className="text-sm text-gray-600">점 (0-100)</p>
        </div>
      </div>
    </div>
  );
};

export default ModelResults;
