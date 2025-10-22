import React from 'react';
import { Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ComposedChart } from 'recharts';
import { TrendingUp } from 'lucide-react';

const TrendLineChart = ({ data }) => {
  if (!data || data.length === 0) {
    return (
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">트렌드 분석</h3>
        <p className="text-gray-500 text-center py-8">트렌드 데이터가 없습니다</p>
      </div>
    );
  }

  // 실제 데이터와 예측 데이터 분리
  const actualData = data.filter(d => d.type === 'actual');
  const forecastData = data.filter(d => d.type === 'forecast');
  
  // 전체 데이터 (차트용)
  const chartData = data.map(d => ({
    month: d.month,
    실제등급: d.type === 'actual' ? d.salesGrade : null,
    예측등급: d.type === 'forecast' ? d.salesGrade : null,
    순위: d.clusterRank ? d.clusterRank * 100 : null, // 0-100 스케일
    pLow56: d.pLow56,
    riskWorsen: d.riskWorsen
  }));

  // 통계 계산
  const actualGrades = actualData.filter(d => d.salesGrade).map(d => d.salesGrade);
  const avgGrade = actualGrades.length > 0 ? (actualGrades.reduce((a, b) => a + b, 0) / actualGrades.length).toFixed(1) : 0;
  const latestGrade = actualGrades.length > 0 ? actualGrades[actualGrades.length - 1] : 0;
  const forecastGrade = forecastData.length > 0 ? forecastData[0].salesGrade : null;
  const forecastRank = forecastData.length > 0 ? forecastData[0].clusterRank : null;

  return (
    <div className="bg-white rounded-xl shadow-lg p-6 hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      <h3 className="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2">
        <TrendingUp className="text-indigo-600" size={24} />
        트렌드 분석 (6개월 실적 + 3개월 예측)
      </h3>

      {/* 요약 정보 */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
        <div className="bg-blue-50 rounded-lg p-3 border-l-4 border-blue-500">
          <div className="text-xs text-blue-600 font-semibold">현재 등급</div>
          <div className="text-lg font-bold text-blue-800">{latestGrade}구간</div>
        </div>
        <div className="bg-green-50 rounded-lg p-3 border-l-4 border-green-500">
          <div className="text-xs text-green-600 font-semibold">평균 등급</div>
          <div className="text-lg font-bold text-green-800">{avgGrade}구간</div>
        </div>
        {forecastGrade && (
          <div className={`rounded-lg p-3 border-l-4 ${forecastGrade <= 3 ? 'bg-green-50 border-green-500' : 'bg-orange-50 border-orange-500'}`}>
            <div className={`text-xs font-semibold ${forecastGrade <= 3 ? 'text-green-600' : 'text-orange-600'}`}>
              예상 등급 (1개월 후)
            </div>
            <div className={`text-lg font-bold ${forecastGrade <= 3 ? 'text-green-800' : 'text-orange-800'}`}>
              {forecastGrade}구간
            </div>
          </div>
        )}
        {forecastRank !== null && (
          <div className="bg-purple-50 rounded-lg p-3 border-l-4 border-purple-500">
            <div className="text-xs text-purple-600 font-semibold">클러스터 내 순위</div>
            <div className="text-lg font-bold text-purple-800">
              상위 {(100 - forecastRank * 100).toFixed(0)}%
            </div>
          </div>
        )}
      </div>

      {/* 차트 */}
      <div className="w-full overflow-x-auto">
        <ComposedChart width={800} height={300} data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#e5e7eb" />
          <XAxis 
            dataKey="month" 
            tick={{ fontSize: 12 }}
            angle={-45}
            textAnchor="end"
            height={80}
          />
          <YAxis 
            yAxisId="left"
            label={{ value: '매출 등급', angle: -90, position: 'insideLeft', style: { fontSize: 12 } }}
            tick={{ fontSize: 12 }}
            domain={[1, 6]}
            reversed={true}
            ticks={[1, 2, 3, 4, 5, 6]}
          />
          <YAxis 
            yAxisId="right"
            orientation="right"
            label={{ value: '클러스터 순위 (%)', angle: 90, position: 'insideRight', style: { fontSize: 12 } }}
            tick={{ fontSize: 12 }}
            domain={[0, 100]}
          />
          <Tooltip 
            contentStyle={{ backgroundColor: '#fff', border: '1px solid #ccc', borderRadius: '8px', padding: '10px' }}
            formatter={(value, name) => {
              if (name === '실제등급') return [`${value}구간`, '실제 등급'];
              if (name === '예측등급') return [`${value}구간`, '예측 등급'];
              if (name === '순위') return [`상위 ${(100 - value).toFixed(0)}%`, '클러스터 순위'];
              return [value, name];
            }}
          />
          <Legend 
            wrapperStyle={{ paddingTop: '20px' }}
            formatter={(value) => {
              if (value === '실제등급') return '실제 등급 (6개월)';
              if (value === '예측등급') return '예측 등급 (3개월)';
              if (value === '순위') return '클러스터 순위 (%)';
              return value;
            }}
          />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="실제등급" 
            stroke="#3b82f6" 
            strokeWidth={3}
            dot={{ fill: '#3b82f6', r: 5 }}
            connectNulls={false}
          />
          <Line 
            yAxisId="left"
            type="monotone" 
            dataKey="예측등급" 
            stroke="#ef4444" 
            strokeWidth={3}
            strokeDasharray="5 5"
            dot={{ fill: '#ef4444', r: 5 }}
            connectNulls={false}
          />
          <Line 
            yAxisId="right"
            type="monotone" 
            dataKey="순위" 
            stroke="#a855f7" 
            strokeWidth={2}
            dot={{ fill: '#a855f7', r: 4 }}
            connectNulls={true}
          />
        </ComposedChart>
      </div>

      {/* 추가 설명 */}
      <div className="mt-4 p-3 bg-gray-50 rounded-lg border border-gray-200">
        <p className="text-sm text-gray-600">
          <span className="font-semibold">📊 그래프 설명:</span> 
          {' '}실제 6개월 매출 등급(파란선)과 예측 3개월 등급(빨간 점선)을 표시합니다. 
          등급이 낮을수록(1에 가까울수록) 우수하며, 보라색 선은 클러스터 내 순위를 나타냅니다.
          <br />
          <span className="font-semibold text-indigo-600">※ 매출 등급:</span> 1구간(최상위) ~ 6구간(하위)
        </p>
      </div>
    </div>
  );
};

export default TrendLineChart;
