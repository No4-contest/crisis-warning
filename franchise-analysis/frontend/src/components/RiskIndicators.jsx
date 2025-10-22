import React from 'react';
import { AlertTriangle, TrendingDown, TrendingUp, Minus } from 'lucide-react';

const RiskIndicators = ({ violations, indicators }) => {
  const getRiskIcon = (level) => {
    switch(level) {
      case '치명적': return <AlertTriangle className="text-red-600" size={20} />;
      case '높음': return <AlertTriangle className="text-orange-600" size={18} />;
      case '중간': return <AlertTriangle className="text-yellow-600" size={16} />;
      default: return <AlertTriangle className="text-blue-600" size={14} />;
    }
  };

  const getRiskBadgeColor = (level) => {
    switch(level) {
      case '치명적': return 'bg-red-100 text-red-800 border-red-300';
      case '높음': return 'bg-orange-100 text-orange-800 border-orange-300';
      case '중간': return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default: return 'bg-blue-100 text-blue-800 border-blue-300';
    }
  };

  const getRowBgColor = (level) => {
    switch(level) {
      case '치명적': return 'bg-red-50 hover:bg-red-100';
      case '높음': return 'bg-orange-50 hover:bg-orange-100';
      case '중간': return 'bg-yellow-50 hover:bg-yellow-100';
      default: return 'bg-blue-50 hover:bg-blue-100';
    }
  };

  const getComparisonIcon = (storeValue, threshold, isPositive) => {
    const diff = storeValue - threshold;
    if (isPositive) {
      // 높을수록 좋은 지표
      if (diff > 0) return <TrendingUp className="text-green-600" size={16} />;
      if (diff < 0) return <TrendingDown className="text-red-600" size={16} />;
    } else {
      // 낮을수록 좋은 지표
      if (diff < 0) return <TrendingUp className="text-green-600" size={16} />;
      if (diff > 0) return <TrendingDown className="text-red-600" size={16} />;
    }
    return <Minus className="text-gray-600" size={16} />;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <AlertTriangle className="text-red-600" size={24} />
        위험 지표 현황
      </h3>

      {violations && violations.length > 0 ? (
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead>
              <tr className="bg-gray-100 border-b-2 border-gray-300">
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">위험도</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">지표명</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">현재값</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">비교</th>
                <th className="px-4 py-3 text-center text-sm font-semibold text-gray-700">임계값</th>
                <th className="px-4 py-3 text-left text-sm font-semibold text-gray-700">상태</th>
              </tr>
            </thead>
            <tbody>
              {violations.map((violation, idx) => (
                <tr 
                  key={idx} 
                  className={`${getRowBgColor(violation.riskLevel)} border-b border-gray-200 transition-colors duration-200`}
                >
                  <td className="px-4 py-3">
                    <div className="flex items-center gap-2">
                      {getRiskIcon(violation.riskLevel)}
                      <span className={`text-xs px-2 py-1 rounded-full border ${getRiskBadgeColor(violation.riskLevel)} font-semibold`}>
                        {violation.riskLevel}
                      </span>
                    </div>
                  </td>
                  <td className="px-4 py-3">
                    <div className="font-medium text-gray-800">{violation.featureKorean}</div>
                    <div className="text-xs text-gray-500 mt-1">{violation.ruleText}</div>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="font-bold text-gray-900">
                      {violation.currentValue.toLocaleString()}
                    </span>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <div className="flex items-center justify-center">
                      {getComparisonIcon(violation.currentValue, violation.threshold, violation.direction === '>=')}
                    </div>
                  </td>
                  <td className="px-4 py-3 text-center">
                    <span className="text-gray-600">
                      {violation.threshold.toLocaleString()}
                    </span>
                  </td>
                  <td className="px-4 py-3">
                    <span className="text-xs text-gray-600">
                      {violation.direction === '<=' ? '▼ 기준 이하' : '▲ 기준 이상'}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <div className="text-center py-8 bg-green-50 rounded-lg border-2 border-green-200">
          <p className="text-green-700 font-semibold">✅ 위반된 룰이 없습니다</p>
          <p className="text-sm text-green-600 mt-1">모든 지표가 안전 범위 내에 있습니다</p>
        </div>
      )}

      {/* 추가 정보 */}
      {violations && violations.length > 0 && (
        <div className="mt-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-sm text-gray-600">
            <span className="font-semibold">총 {violations.length}개</span>의 위험 지표가 감지되었습니다.
            {violations.filter(v => v.riskLevel === '치명적').length > 0 && (
              <span className="ml-2 text-red-600 font-semibold">
                ({violations.filter(v => v.riskLevel === '치명적').length}개 치명적)
              </span>
            )}
          </p>
        </div>
      )}
    </div>
  );
};

export default RiskIndicators;

