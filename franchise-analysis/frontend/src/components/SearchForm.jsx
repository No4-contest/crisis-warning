import React, { useState } from 'react';
import { Search } from 'lucide-react';

const SearchForm = ({ onSearch, loading }) => {
  const [storeId, setStoreId] = useState('');
  const [errors, setErrors] = useState({});

  // 점포 검색
  const handleSearch = () => {
    if (!storeId.trim()) {
      setErrors({ storeId: '점포 ID를 입력해주세요.' });
      return;
    }
    setErrors({});
    onSearch(storeId);
  };

  // Enter 키 처리
  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSearch();
    }
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-6">
      <div>
        <label className="block text-sm font-semibold text-gray-700 mb-2">
          점포 ID 검색
        </label>
        <div className="flex gap-3">
          <div className="flex-1">
            <input
              type="text"
              placeholder="예: 000F03E44A"
              value={storeId}
              onChange={(e) => setStoreId(e.target.value)}
              onKeyPress={handleKeyPress}
              className={`w-full px-4 py-3 border rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-transparent ${
                errors.storeId ? 'border-red-500' : 'border-gray-300'
              }`}
            />
            {errors.storeId && (
              <p className="text-red-500 text-sm mt-1">{errors.storeId}</p>
            )}
          </div>
          <button
            onClick={handleSearch}
            disabled={loading}
            className="px-6 py-3 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 disabled:bg-gray-300 disabled:cursor-not-allowed flex items-center gap-2 transition"
          >
            <Search size={20} />
            {loading ? '리포트 생성 중...' : '리포트 생성'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default SearchForm;