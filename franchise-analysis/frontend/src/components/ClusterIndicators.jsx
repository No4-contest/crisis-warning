import React from 'react';
import { BarChart3, TrendingUp, TrendingDown } from 'lucide-react';

const ClusterIndicators = ({ indicators }) => {
  const getIndicatorColor = (indicator) => {
    const { value, clusterAvg, isPositive } = indicator;
    const ratio = clusterAvg > 0 ? value / clusterAvg : 0;
    
    if (isPositive) {
      // 높을수록 좋은 지표
      if (ratio >= 1.2) return 'text-green-600 bg-green-50 border-green-200';
      if (ratio >= 0.8) return 'text-blue-600 bg-blue-50 border-blue-200';
      return 'text-red-600 bg-red-50 border-red-200';
    } else {
      // 낮을수록 좋은 지표
      if (ratio <= 0.8) return 'text-green-600 bg-green-50 border-green-200';
      if (ratio <= 1.2) return 'text-blue-600 bg-blue-50 border-blue-200';
      return 'text-red-600 bg-red-50 border-red-200';
    }
  };

  const getTrendIcon = (indicator) => {
    const { value, clusterAvg, isPositive } = indicator;
    const ratio = clusterAvg > 0 ? value / clusterAvg : 0;
    
    if (isPositive) {
      return ratio >= 1 ? <TrendingUp className="text-green-600" size={16} /> : <TrendingDown className="text-red-600" size={16} />;
    } else {
      return ratio <= 1 ? <TrendingUp className="text-green-600" size={16} /> : <TrendingDown className="text-red-600" size={16} />;
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <BarChart3 className="text-indigo-600" size={24} />
        클러스터별 주요 지표
      </h3>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {indicators.map((indicator, index) => (
          <div 
            key={index}
            className={`rounded-lg p-4 border-2 ${getIndicatorColor(indicator)}`}
          >
            <div className="flex items-center justify-between mb-2">
              <h4 className="font-semibold text-gray-800">{indicator.name}</h4>
              {getTrendIcon(indicator)}
            </div>
            
            <div className="space-y-2">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">내 점포</span>
                <span className="font-bold text-lg">
                  {Number(indicator.value).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{indicator.unit}
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">클러스터 평균</span>
                <span className="text-sm">
                  {Number(indicator.clusterAvg).toLocaleString(undefined, { minimumFractionDigits: 2, maximumFractionDigits: 2 })}{indicator.unit}
                </span>
              </div>

              {/* 비교 막대 그래프 (내 점포 vs 클러스터 평균) */}
              <div className="mt-2">
                {(() => {
                  const max = Math.max(
                    Math.abs(Number(indicator.value) || 0),
                    Math.abs(Number(indicator.clusterAvg) || 0),
                    1
                  );
                  const myWidth = Math.min(100, Math.round((Math.abs(Number(indicator.value) || 0) / max) * 100));
                  const avgWidth = Math.min(100, Math.round((Math.abs(Number(indicator.clusterAvg) || 0) / max) * 100));
                  return (
                    <div className="space-y-2">
                      <div className="text-xs text-gray-500">비교</div>
                      <div className="w-full bg-gray-100 rounded h-2 overflow-hidden">
                        <div
                          className="bg-indigo-500 h-2"
                          style={{ width: `${myWidth}%` }}
                          title={`내 점포: ${indicator.value}`}
                        />
                      </div>
                      <div className="w-full bg-gray-100 rounded h-2 overflow-hidden">
                        <div
                          className="bg-gray-400 h-2"
                          style={{ width: `${avgWidth}%` }}
                          title={`클러스터 평균: ${indicator.clusterAvg}`}
                        />
                      </div>
                      <div className="flex justify-between text-xs text-gray-500">
                        <span>내 점포</span>
                        <span>클러스터 평균</span>
                      </div>
                    </div>
                  );
                })()}
              </div>
              
              <div className="mt-2 p-2 bg-gray-50 rounded text-xs text-gray-600">
                {indicator.description}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ClusterIndicators;
