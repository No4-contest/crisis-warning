import React from 'react';
import { AlertTriangle, AlertCircle, Info } from 'lucide-react';

const RiskFactors = ({ factors }) => {
  // 심각도별 아이콘
  const getSeverityIcon = (severity) => {
    switch (severity) {
      case 'high':
        return <AlertTriangle size={20} />;
      case 'medium':
        return <AlertCircle size={20} />;
      case 'low':
        return <Info size={20} />;
      default:
        return <Info size={20} />;
    }
  };

  // 심각도별 색상
  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'high':
        return 'bg-red-100 text-red-800 border-red-300';
      case 'medium':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'low':
        return 'bg-yellow-100 text-yellow-800 border-yellow-300';
      default:
        return 'bg-gray-100 text-gray-800 border-gray-300';
    }
  };

  // 심각도 텍스트
  const getSeverityText = (severity) => {
    switch (severity) {
      case 'high':
        return '높음';
      case 'medium':
        return '중간';
      case 'low':
        return '낮음';
      default:
        return '알 수 없음';
    }
  };

  // 심각도별 정렬 (높음 -> 중간 -> 낮음)
  const sortedFactors = [...factors].sort((a, b) => {
    const order = { high: 0, medium: 1, low: 2 };
    return order[a.severity] - order[b.severity];
  });

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xl font-bold text-gray-800">⚠️ 주요 위험 요인</h2>
        <span className="text-sm text-gray-500">총 {factors.length}개 발견</span>
      </div>

      {factors.length === 0 ? (
        <div className="text-center py-8">
          <Info size={48} className="mx-auto text-gray-300 mb-3" />
          <p className="text-gray-500">발견된 위험 요인이 없습니다.</p>
          <p className="text-sm text-gray-400 mt-1">현재 상태가 양호합니다! 👍</p>
        </div>
      ) : (
        <div className="space-y-3">
          {sortedFactors.map((risk, idx) => (
            <div
              key={idx}
              className={`p-4 rounded-lg border-2 transition hover:shadow-md ${getSeverityColor(risk.severity)}`}
            >
              <div className="flex items-start gap-3">
                {/* 아이콘 */}
                <div className="flex-shrink-0 mt-1">
                  {getSeverityIcon(risk.severity)}
                </div>

                {/* 내용 */}
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-2">
                    <span className="font-bold text-lg">{risk.factor}</span>
                    <span className="text-xs px-3 py-1 rounded-full bg-white shadow-sm font-semibold">
                      위험도: {getSeverityText(risk.severity)}
                    </span>
                  </div>
                  <p className="text-sm leading-relaxed">{risk.description}</p>

                  {/* 추가 정보 (있을 경우) */}
                  {risk.value && (
                    <div className="mt-2 pt-2 border-t border-current/20">
                      <p className="text-xs font-mono">
                        현재값: <span className="font-bold">{risk.value}</span>
                        {risk.benchmark && (
                          <> | 기준값: <span className="font-bold">{risk.benchmark}</span></>
                        )}
                      </p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* 요약 통계 */}
      {factors.length > 0 && (
        <div className="mt-6 pt-4 border-t border-gray-200">
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-2xl font-bold text-red-600">
                {factors.filter(f => f.severity === 'high').length}
              </p>
              <p className="text-xs text-gray-600">높은 위험</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-orange-600">
                {factors.filter(f => f.severity === 'medium').length}
              </p>
              <p className="text-xs text-gray-600">중간 위험</p>
            </div>
            <div>
              <p className="text-2xl font-bold text-yellow-600">
                {factors.filter(f => f.severity === 'low').length}
              </p>
              <p className="text-xs text-gray-600">낮은 위험</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default RiskFactors;