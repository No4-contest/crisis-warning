import React from 'react';
import { AlertTriangle, XCircle, AlertCircle, Info } from 'lucide-react';

const ViolationsTable = ({ violations }) => {
  if (!violations || violations.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
        <div className="flex items-center gap-3 mb-4">
          <AlertTriangle className="text-green-600" size={24} />
          <h3 className="text-xl font-bold text-gray-800">룰 위반 현황</h3>
        </div>
        <div className="text-center py-8">
          <div className="text-green-600 text-4xl mb-2">✅</div>
          <p className="text-gray-600">위반된 룰이 없습니다. 모든 기준을 만족하고 있습니다.</p>
        </div>
      </div>
    );
  }

  const getRiskIcon = (riskLevel) => {
    switch (riskLevel) {
      case '치명적':
        return <XCircle className="text-red-500" size={20} />;
      case '경고':
        return <AlertTriangle className="text-orange-500" size={20} />;
      case '주의':
        return <AlertCircle className="text-yellow-500" size={20} />;
      default:
        return <Info className="text-blue-500" size={20} />;
    }
  };

  const getRiskColor = (riskLevel) => {
    switch (riskLevel) {
      case '치명적':
        return 'bg-red-50 border-red-200';
      case '경고':
        return 'bg-orange-50 border-orange-200';
      case '주의':
        return 'bg-yellow-50 border-yellow-200';
      default:
        return 'bg-blue-50 border-blue-200';
    }
  };

  const getTextColor = (riskLevel) => {
    switch (riskLevel) {
      case '치명적':
        return 'text-red-800';
      case '경고':
        return 'text-orange-800';
      case '주의':
        return 'text-yellow-800';
      default:
        return 'text-blue-800';
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
      <div className="flex items-center gap-3 mb-6">
        <AlertTriangle className="text-red-600" size={24} />
        <h3 className="text-xl font-bold text-gray-800">위반된 룰 현황</h3>
        <span className="bg-red-100 text-red-800 px-2 py-1 rounded-full text-sm font-semibold">
          {violations.length}개 위반
        </span>
      </div>

      <div className="overflow-x-auto">
        <table className="w-full">
          <thead>
            <tr className="border-b border-gray-200">
              <th className="text-left py-3 px-4 font-semibold text-gray-700">위험도</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">룰 내용</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">특성</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">현재값</th>
              <th className="text-left py-3 px-4 font-semibold text-gray-700">임계값</th>
            </tr>
          </thead>
          <tbody>
            {violations.map((violation, index) => (
              <tr 
                key={index}
                className={`border-b border-gray-100 hover:bg-gray-50 transition-colors duration-200 ${getRiskColor(violation.riskLevel)}`}
              >
                <td className="py-4 px-4">
                  <div className="flex items-center gap-2">
                    {getRiskIcon(violation.riskLevel)}
                    <span className={`font-semibold ${getTextColor(violation.riskLevel)}`}>
                      {violation.riskLevel}
                    </span>
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="font-medium text-gray-800">
                    {violation.ruleText}
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="text-gray-600">
                    {violation.featureKorean}
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="font-semibold text-gray-800">
                    {typeof violation.currentValue === 'number' 
                      ? violation.currentValue.toFixed(2) 
                      : violation.currentValue}
                  </div>
                </td>
                <td className="py-4 px-4">
                  <div className="text-gray-600">
                    {typeof violation.threshold === 'number' 
                      ? violation.threshold.toFixed(2) 
                      : violation.threshold}
                    <span className="text-sm text-gray-500 ml-1">
                      ({violation.direction})
                    </span>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      <div className="mt-4 text-sm text-gray-600">
        <p>💡 위반된 룰들을 개선하여 위험도를 낮출 수 있습니다.</p>
      </div>
    </div>
  );
};

export default ViolationsTable;
