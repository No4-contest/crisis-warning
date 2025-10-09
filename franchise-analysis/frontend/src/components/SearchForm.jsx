import React, { useState } from 'react';
import { Search } from 'lucide-react';

const SearchForm = ({ mode, onSearch, onNewStoreSubmit, loading }) => {
  const [franchiseId, setFranchiseId] = useState('');
  const [newStoreForm, setNewStoreForm] = useState({
    tradingArea: '',
    industry: '',
    latitude: '',
    longitude: '',
    monthlyRent: '',
    nearbyStores: '',
    footTraffic: '',
    rentIncreaseRate: '',
    salesGrowthRate: ''
  });

  const [errors, setErrors] = useState({});

  // 기존 가맹점 검색
  const handleSearch = () => {
    if (!franchiseId.trim()) {
      setErrors({ franchiseId: '가맹점 ID를 입력해주세요.' });
      return;
    }
    setErrors({});
    onSearch(franchiseId);
  };

  // 신규 가맹점 입력 변경
  const handleInputChange = (field, value) => {
    setNewStoreForm(prev => ({ ...prev, [field]: value }));
    // 에러 초기화
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: null }));
    }
  };

  // 신규 가맹점 제출
  const handleNewStoreSubmit = () => {
    const newErrors = {};
    
    // 필수 필드 검증
    if (!newStoreForm.tradingArea.trim()) newErrors.tradingArea = '상권명을 입력해주세요.';
    if (!newStoreForm.industry.trim()) newErrors.industry = '업종을 입력해주세요.';
    if (!newStoreForm.latitude || isNaN(newStoreForm.latitude)) {
      newErrors.latitude = '올바른 위도를 입력해주세요.';
    }
    if (!newStoreForm.longitude || isNaN(newStoreForm.longitude)) {
      newErrors.longitude = '올바른 경도를 입력해주세요.';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    setErrors({});
    onNewStoreSubmit(newStoreForm);
  };

  // Enter 키 처리
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      if (mode === 'existing') {
        handleSearch();
      } else {
        handleNewStoreSubmit();
      }
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      {/* 기존 가맹점 검색 */}
      {mode === 'existing' && (
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            가맹점 ID 검색
          </label>
          <div className="flex gap-3">
            <div className="flex-1">
              <input
                type="text"
                placeholder="예: FR-12345"
                value={franchiseId}
                onChange={(e) => setFranchiseId(e.target.value)}
                onKeyPress={handleKeyPress}
                className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                  errors.franchiseId ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.franchiseId && (
                <p className="text-red-500 text-sm mt-1">{errors.franchiseId}</p>
              )}
            </div>
            <button
              onClick={handleSearch}
              disabled={loading}
              className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 transition"
            >
              <Search size={20} />
              {loading ? '분석 중...' : '분석하기'}
            </button>
          </div>
        </div>
      )}

      {/* 신규 가맹점 입력 */}
      {mode === 'new' && (
        <div>
          <h3 className="text-lg font-bold text-gray-800 mb-4">신규 입점 정보 입력</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* 상권명 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                상권명 <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                placeholder="예: 강남역 상권"
                value={newStoreForm.tradingArea}
                onChange={(e) => handleInputChange('tradingArea', e.target.value)}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 ${
                  errors.tradingArea ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.tradingArea && (
                <p className="text-red-500 text-xs mt-1">{errors.tradingArea}</p>
              )}
            </div>

            {/* 업종 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                업종 <span className="text-red-500">*</span>
              </label>
              <input
                type="text"
                placeholder="예: 카페"
                value={newStoreForm.industry}
                onChange={(e) => handleInputChange('industry', e.target.value)}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 ${
                  errors.industry ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.industry && (
                <p className="text-red-500 text-xs mt-1">{errors.industry}</p>
              )}
            </div>

            {/* 위도 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                위도 <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.0001"
                placeholder="예: 37.4979"
                value={newStoreForm.latitude}
                onChange={(e) => handleInputChange('latitude', e.target.value)}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 ${
                  errors.latitude ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.latitude && (
                <p className="text-red-500 text-xs mt-1">{errors.latitude}</p>
              )}
            </div>

            {/* 경도 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                경도 <span className="text-red-500">*</span>
              </label>
              <input
                type="number"
                step="0.0001"
                placeholder="예: 127.0276"
                value={newStoreForm.longitude}
                onChange={(e) => handleInputChange('longitude', e.target.value)}
                className={`w-full px-4 py-2 border rounded-lg focus:ring-2 focus:ring-indigo-500 ${
                  errors.longitude ? 'border-red-500' : 'border-gray-300'
                }`}
              />
              {errors.longitude && (
                <p className="text-red-500 text-xs mt-1">{errors.longitude}</p>
              )}
            </div>

            {/* 월 임대료 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                월 임대료 (만원)
              </label>
              <input
                type="number"
                placeholder="예: 350"
                value={newStoreForm.monthlyRent}
                onChange={(e) => handleInputChange('monthlyRent', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            {/* 경쟁점포 수 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                반경 500m 내 경쟁점포 수
              </label>
              <input
                type="number"
                placeholder="예: 45"
                value={newStoreForm.nearbyStores}
                onChange={(e) => handleInputChange('nearbyStores', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            {/* 유동인구 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                월 평균 유동인구
              </label>
              <input
                type="number"
                placeholder="예: 125000"
                value={newStoreForm.footTraffic}
                onChange={(e) => handleInputChange('footTraffic', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>

            {/* 임대료 상승률 */}
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">
                임대료 상승률 (%)
              </label>
              <input
                type="number"
                step="0.1"
                placeholder="예: 8.2"
                value={newStoreForm.rentIncreaseRate}
                onChange={(e) => handleInputChange('rentIncreaseRate', e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500"
              />
            </div>
          </div>

          {/* 제출 버튼 */}
          <button
            onClick={handleNewStoreSubmit}
            disabled={loading}
            className="w-full mt-6 px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed font-semibold transition"
          >
            {loading ? '분석 중...' : '입점 가능성 분석'}
          </button>
        </div>
      )}
    </div>
  );
};

export default SearchForm;