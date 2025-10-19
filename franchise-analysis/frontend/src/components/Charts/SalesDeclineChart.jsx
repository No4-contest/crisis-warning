import React from 'react';
import { TrendingDown, TrendingUp } from 'lucide-react';

const SalesDeclineChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">매출 급감 예상 그래프</h3>
        <p className="text-gray-500 text-center py-8">데이터가 없습니다.</p>
      </div>
    );
  }

  const maxSales = Math.max(...data.map(d => d.predictedSales));
  const minSales = Math.min(...data.map(d => d.predictedSales));

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <TrendingDown className="text-red-600" size={24} />
        매출 급감 예상 그래프
      </h3>
      
      <div className="space-y-4">
        {/* 차트 영역: 꺾은선 그래프 */}
        <div className="relative h-64 bg-gray-50 rounded-lg p-4">
          <svg className="w-full h-full">
            {(() => {
              const paddingX = 32;
              const paddingY = 16;
              const width = 800; // virtual width reference
              const height = 256; // virtual height reference
              const points = data.map((d, i) => {
                const x = paddingX + (i * (width - paddingX * 2)) / (data.length - 1 || 1);
                const y = paddingY + (1 - (d.predictedSales - minSales) / (maxSales - minSales || 1)) * (height - paddingY * 2);
                return { x, y, label: d.month, value: d.predictedSales };
              });
              const path = points.map((p, i) => `${i === 0 ? 'M' : 'L'} ${p.x},${p.y}`).join(' ');
              return (
                <g transform="scale(1,1)">
                  <path d={path} fill="none" stroke="#4f46e5" strokeWidth="3" />
                  {points.map((p, i) => (
                    <g key={i}>
                      <circle cx={p.x} cy={p.y} r="3" fill="#4f46e5" />
                      <text x={p.x} y={p.y - 8} textAnchor="middle" className="fill-gray-600 text-[10px]">
                        {Number(p.value).toLocaleString()}
                      </text>
                      <text x={p.x} y={height - 2} textAnchor="middle" className="fill-gray-500 text-[10px]">
                        {p.label}
                      </text>
                    </g>
                  ))}
                </g>
              );
            })()}
          </svg>
          {/* Y축 범례 */}
          <div className="absolute left-0 top-0 h-full flex flex-col justify-between text-xs text-gray-500 p-2">
            <span>{maxSales.toLocaleString()}</span>
            <span>{minSales.toLocaleString()}</span>
          </div>
        </div>
        
        {/* 범례 */}
        <div className="flex items-center justify-center gap-6 text-sm">
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-blue-400 rounded"></div>
            <span className="text-gray-600">예상 매출</span>
          </div>
          <div className="flex items-center gap-2">
            <div className="w-3 h-3 bg-red-400 rounded"></div>
            <span className="text-gray-600">매출 하락</span>
          </div>
        </div>
        
        {/* 요약 정보 */}
        <div className="bg-gray-50 rounded-lg p-4">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-center">
            <div>
              <p className="text-sm text-gray-600">현재 매출</p>
              <p className="text-lg font-bold text-gray-800">
                {data[0]?.predictedSales?.toLocaleString() || 0}만원
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">6개월 후 예상</p>
              <p className="text-lg font-bold text-red-600">
                {data[data.length - 1]?.predictedSales?.toLocaleString() || 0}만원
              </p>
            </div>
            <div>
              <p className="text-sm text-gray-600">예상 하락률</p>
              <p className="text-lg font-bold text-red-600">
                {data.length > 1 ? 
                  (((data[0]?.predictedSales - data[data.length - 1]?.predictedSales) / data[0]?.predictedSales) * 100).toFixed(1) 
                  : 0}%
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SalesDeclineChart;
