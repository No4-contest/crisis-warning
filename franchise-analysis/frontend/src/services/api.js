import axios from 'axios';

// 백엔드 API 베이스 URL
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Axios 인스턴스 생성
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// 요청 인터셉터 (로딩, 에러 처리 등)
apiClient.interceptors.request.use(
  (config) => {
    console.log(`API 요청: ${config.method?.toUpperCase()} ${config.url}`);
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 응답 인터셉터
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('API 에러:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

// ============================================
// 📌 API 함수들
// ============================================

/**
 * 기존 가맹점 정보 조회
 * @param {string} franchiseId - 가맹점 ID
 * @returns {Promise} 가맹점 분석 데이터
 */
export const getFranchiseAnalysis = async (franchiseId) => {
  try {
    const response = await apiClient.get(`/api/franchise/${franchiseId}`);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || '가맹점 조회에 실패했습니다.');
  }
};

/**
 * 신규 가맹점 클러스터 예측 및 분석
 * @param {Object} storeData - 신규 점포 정보
 * @returns {Promise} 예측된 클러스터 및 분석 데이터
 */
export const predictNewStore = async (storeData) => {
  try {
    const response = await apiClient.post('/api/franchise/predict', storeData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || '신규 점포 분석에 실패했습니다.');
  }
};

/**
 * LLM 기반 전략 제안
 * @param {Object} analysisData - 분석된 데이터
 * @returns {Promise} LLM 생성 전략
 */
export const getLLMSuggestion = async (analysisData) => {
  try {
    const response = await apiClient.post('/api/llm/analyze', analysisData);
    return response.data;
  } catch (error) {
    throw new Error(error.response?.data?.detail || 'AI 분석에 실패했습니다.');
  }
};

/**
 * 전체 클러스터 목록 조회 (선택사항)
 * @returns {Promise} 클러스터 리스트
 */
export const getClusters = async () => {
  try {
    const response = await apiClient.get('/api/clusters');
    return response.data;
  } catch (error) {
    throw new Error('클러스터 정보를 불러올 수 없습니다.');
  }
};

/**
 * 상권별 통계 조회 (선택사항)
 * @param {string} tradingArea - 상권명
 * @returns {Promise} 상권 통계
 */
export const getTradingAreaStats = async (tradingArea) => {
  try {
    const response = await apiClient.get(`/api/stats/trading-area/${tradingArea}`);
    return response.data;
  } catch (error) {
    throw new Error('상권 정보를 불러올 수 없습니다.');
  }
};

export default apiClient;