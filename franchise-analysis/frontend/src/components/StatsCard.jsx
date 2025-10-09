import React from 'react';
import { MapPin, Store, Users, DollarSign, AlertCircle, TrendingUp, TrendingDown } from 'lucide-react';

const StatsCard = ({ type, title, value, subtitle, trend, risk }) => {
  // 아이콘 선택
  const getIcon = () => {
    switch (type) {
      case 'location':
        return <MapPin size={20} />;
      case 'cluster':
        return <Store size={20} />;
      case 'traffic':
        return <Users size={20} />;
      case 'money':
        return <DollarSign size={20} />;
      case 'risk':
        return <AlertCircle size={20} />;
      default:
        return <Store size={20} />;
    }
  };

  // 위험도 색상
  const getRiskColor = () => {
    if (!risk) return 'bg-white';
    if (risk >= 70) return 'bg-red-50 border-red-200';
    if (risk >= 40) return 'bg-orange-50 border-orange-200';
    return 'bg-green-50 border-green-200';
  };

  const getRiskTextColor = () => {
    if (!risk) return 'text-gray-800';
    if (risk >= 70) return 'text-red-600';
    if (risk >= 40) return 'text-orange-600';
    return 'text-green-600';
  };

  // 트렌드 아이콘
  const getTrendIcon = () => {
    if (!trend) return null;
    return trend > 0 ? (
      <TrendingUp size={16} className="text-green-500" />
    ) : (
      <TrendingDown size={16} className="text-red-500" />
    );
  };

  return (
    <div className={`rounded-lg shadow-md p-4 border transition hover:shadow-lg ${getRiskColor()}`}>
      {/* 헤더 */}
      <div className="flex items-center gap-2 text-gray-600 mb-2">
        {getIcon()}
        <span className="text-sm font-semibold">{title}</span>
      </div>

      {/* 메인 값 */}
      <div className="flex items-baseline gap-2 mb-1">
        <p className={`text-2xl font-bold ${getRiskTextColor()}`}>
          {value}
        </p>
        {trend !== undefined && trend !== null && (
          <div className="flex items-center gap-1">
            {getTrendIcon()}
            <span className={`text-sm font-medium ${trend > 0 ? 'text-green-600' : 'text-red-600'}`}>
              {Math.abs(trend)}%
            </span>
          </div>
        )}
      </div>

      {/* 부제목 */}
      {subtitle && (
        <p className="text-sm text-gray-500">{subtitle}</p>
      )}

      {/* 위험도 게이지 (risk가 있을 때만) */}
      {risk !== undefined && (
        <div className="mt-3">
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className={`h-2 rounded-full transition-all duration-500 ${
                risk >= 70 ? 'bg-red-500' : risk >= 40 ? 'bg-orange-500' : 'bg-green-500'
              }`}
              style={{ width: `${risk}%` }}
            />
          </div>
        </div>
      )}
    </div>
  );
};

export default StatsCard;