import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const DistributionChart = ({ data, title, variable }) => {
  // 커스텀 툴팁
  const CustomTooltip = ({ active, payload, label }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-gray-800 mb-2">{label}</p>
          {payload.map((entry, index) => (
            <p key={index} className="text-sm" style={{ color: entry.color }}>
              {entry.name}: <span className="font-bold">{entry.value}개 점포</span>
            </p>
          ))}
        </div>
      );
    }
    return null;
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h2 className="text-xl font-bold text-gray-800 mb-2">
        {title || '📈 클러스터 내 위험도 분포'}
      </h2>
      {variable && (
        <p className="text-sm text-gray-600 mb-4">변수: {variable}</p>
      )}
      
      <ResponsiveContainer width="100%" height={300}>
        <AreaChart 
          data={data}
          margin={{ top: 10, right: 30, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorCluster" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#94a3b8" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#94a3b8" stopOpacity={0.1}/>
            </linearGradient>
            <linearGradient id="colorMyStore" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#6366f1" stopOpacity={0.8}/>
              <stop offset="95%" stopColor="#6366f1" stopOpacity={0.3}/>
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="range" 
            tick={{ fontSize: 12 }}
            label={{ value: '위험도 구간', position: 'insideBottom', offset: -5 }}
          />
          <YAxis 
            tick={{ fontSize: 12 }}
            label={{ value: '점포 수', angle: -90, position: 'insideLeft' }}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ paddingTop: '10px' }}
            iconType="circle"
          />
          <Area 
            type="monotone" 
            dataKey="cluster" 
            stroke="#94a3b8" 
            fillOpacity={1}
            fill="url(#colorCluster)"
            name="클러스터 분포"
          />
          <Area 
            type="monotone" 
            dataKey="myStore" 
            stroke="#6366f1" 
            fillOpacity={1}
            fill="url(#colorMyStore)"
            name="우리 점포"
            strokeWidth={3}
          />
        </AreaChart>
      </ResponsiveContainer>

      {/* 해석 가이드 */}
      <div className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
        <div className="p-3 bg-gray-50 rounded-lg border border-gray-200">
          <p className="text-xs text-gray-600 mb-1">클러스터 평균 위치</p>
          <p className="text-sm font-semibold text-gray-800">
            {data.find(d => d.cluster === Math.max(...data.map(x => x.cluster)))?.range || 'N/A'}
          </p>
        </div>
        <div className="p-3 bg-indigo-50 rounded-lg border border-indigo-200">
          <p className="text-xs text-indigo-600 mb-1">우리 점포 위치</p>
          <p className="text-sm font-semibold text-indigo-800">
            {data.find(d => d.myStore > 0)?.range || 'N/A'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default DistributionChart;