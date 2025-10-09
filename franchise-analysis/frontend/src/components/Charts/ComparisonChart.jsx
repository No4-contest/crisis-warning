import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Cell } from 'recharts';

const ComparisonChart = ({ data, title }) => {
  // 커스텀 툴팁
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-800 mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: <span className="font-bold">{entry.value}{entry.payload.unit || ''}</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  // 바 색상 (차이가 클수록 강조)
  const getBarColor = (value, avgValue) => {
    const diff = Math.abs(value - avgValue);
    if (diff > 15) return '#ef4444'; // 큰 차이 - 빨강
    if (diff > 5) return '#f97316'; // 중간 차이 - 주황
    return '#6366f1'; // 작은 차이 - 파랑
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-4">
        {title || '📊 주요 지표 비교 (우리 점포 vs 클러스터 평균)'}
      </h2>
      
      <ResponsiveContainer width="100%" height={350}>
        <BarChart 
          data={data}
          margin={{ top: 20, right: 30, left: 20, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="variable" 
            tick={{ fontSize: 12 }}
            angle={-15}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            label={{ value: '값 (%)', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            iconType="circle"
          />
          <Bar 
            dataKey="myStore" 
            name="우리 점포"
            radius={[8, 8, 0, 0]}
          >
            {data.map((entry, index) => (
              <Cell 
                key={`cell-${index}`} 
                fill={getBarColor(entry.myStore, entry.clusterAvg)} 
              />
            ))}
          </Bar>
          <Bar 
            dataKey="clusterAvg" 
            fill="#94a3b8" 
            name="클러스터 평균"
            radius={[8, 8, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>

      {/* 해석 가이드 */}
      <div className="mt-4 p-3 bg-blue-50 rounded-lg border border-blue-200">
        <p className="text-sm text-blue-800">
          💡 <span className="font-semibold">해석 팁:</span> 빨간색 막대는 클러스터 평균과 큰 차이를 보이는 지표입니다. 
          이런 지표들이 폐업 위험에 영향을 줄 수 있어요.
        </p>
      </div>
    </div>
  );
};

export default ComparisonChart;