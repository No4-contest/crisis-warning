import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from app.services.data_loader import data_loader


class Analyzer:
    """가맹점 데이터 분석"""
    
    def generate_franchise_report(self, franchise_id: str) -> Dict:
        """가맹점 리포트 생성"""
        # 1. 가맹점 정보 가져오기
        franchise = data_loader.get_franchise_by_id(franchise_id)
        if not franchise:
            raise ValueError(f"가맹점 ID {franchise_id}를 찾을 수 없습니다.")
        
        # 2. 클러스터 정보 가져오기
        cluster_stats = data_loader.get_cluster_stats(franchise['cluster_id'])
        if not cluster_stats:
            raise ValueError(f"클러스터 {franchise['cluster_id']}를 찾을 수 없습니다.")
        
        # 3. 업종 통계
        industry_stats = data_loader.get_industry_stats(franchise['industry'])
        
        # 4. 모델 결과 생성
        model_results = self._create_model_results(franchise)
        
        # 5. 클러스터별 주요 지표 생성
        cluster_indicators = self._create_cluster_indicators(franchise, cluster_stats)
        
        # 6. 매출 급감 예상 그래프 데이터
        sales_decline_data = self._create_sales_decline_data(franchise)
        
        return {
            'franchise': franchise,
            'cluster_stats': cluster_stats,
            'industry_stats': industry_stats,
            'model_results': model_results,
            'cluster_indicators': cluster_indicators,
            'sales_decline_data': sales_decline_data
        }
    
    def predict_new_store(self, store_data: Dict) -> Dict:
        """신규 가맹점 클러스터 예측 및 분석"""
        # 1. 모델 로드
        model = data_loader.load_cluster_model()
        scaler = data_loader.load_scaler()
        
        # 2. 특징 벡터 생성
        features = self._prepare_features(store_data)
        
        # 3. 스케일링 (있을 경우)
        if scaler:
            features = scaler.transform([features])
        else:
            features = [features]
        
        # 4. 클러스터 예측
        cluster_id = model.predict(features)[0]
        cluster_id_str = f"C-{cluster_id}"
        
        # 5. 해당 클러스터 통계 가져오기
        cluster_stats = data_loader.get_cluster_stats(cluster_id_str)
        if not cluster_stats:
            # 클러스터 통계가 없으면 기본값 사용
            cluster_stats = self._get_default_cluster_stats()
        
        # 6. 예측 가맹점 정보 구성
        predicted_franchise = {
            'franchise_id': 'NEW',
            'name': '신규 입점 예정',
            'trading_area': store_data['tradingArea'],
            'industry': store_data['industry'],
            'latitude': store_data['latitude'],
            'longitude': store_data['longitude'],
            'cluster_id': cluster_id_str,
            'risk_score': cluster_stats.get('closure_rate', 50.0),
            'monthly_rent': store_data.get('monthlyRent', 0),
            'nearby_stores': store_data.get('nearbyStores', 0),
            'foot_traffic': store_data.get('footTraffic', 0)
        }
        
        # 7. 비교 데이터 (클러스터 평균과 비교)
        comparison_data = self._create_comparison_data_for_new(store_data, cluster_stats)
        
        # 8. 분포 데이터 (클러스터 내 위치)
        distribution_data = self._create_distribution_data_for_cluster(cluster_id_str)
        
        # 9. 위험 요인 (클러스터 기반)
        risk_factors = self._analyze_risk_factors_for_new(store_data, cluster_stats)
        
        return {
            'franchise': predicted_franchise,
            'cluster_stats': cluster_stats,
            'industry_stats': data_loader.get_industry_stats(store_data['industry']),
            'comparison_data': comparison_data,
            'distribution_data': distribution_data,
            'risk_factors': risk_factors
        }
    
    def _prepare_features(self, store_data: Dict) -> List[float]:
        """신규 점포 데이터를 모델 입력 형태로 변환"""
        return [
            store_data['latitude'],
            store_data['longitude'],
            store_data.get('monthlyRent', 0) or 0,
            store_data.get('nearbyStores', 0) or 0,
            store_data.get('footTraffic', 0) or 0,
            store_data.get('rentIncreaseRate', 0) or 0,
        ]
    
    def _create_comparison_data(self, franchise: Dict, cluster_stats: Dict) -> List[Dict]:
        """비교 데이터 생성 (우리 점포 vs 클러스터 평균)"""
        comparisons = []
        
        # 주요 변수들 비교
        variables = [
            ('foot_traffic_change_rate', '유동인구 변화율', '%'),
            ('sales_growth_rate', '매출 성장률', '%'),
            ('rent_increase_rate', '임대료 상승률', '%'),
            ('nearby_stores_change_rate', '경쟁점포 증가율', '%'),
        ]
        
        for col, name, unit in variables:
            if col in franchise and f'avg_{col}' in cluster_stats:
                comparisons.append({
                    'variable': name,
                    'myStore': franchise.get(col, 0) or 0,
                    'clusterAvg': cluster_stats.get(f'avg_{col}', 0) or 0,
                    'unit': unit
                })
        
        return comparisons
    
    def _create_comparison_data_for_new(self, store_data: Dict, cluster_stats: Dict) -> List[Dict]:
        """신규 점포의 비교 데이터"""
        comparisons = []
        
        if store_data.get('monthlyRent') and cluster_stats.get('avg_rent'):
            comparisons.append({
                'variable': '월 임대료',
                'myStore': store_data['monthlyRent'],
                'clusterAvg': cluster_stats['avg_rent'],
                'unit': '만원'
            })
        
        if store_data.get('nearbyStores') and cluster_stats.get('avg_nearby_stores'):
            comparisons.append({
                'variable': '경쟁점포 수',
                'myStore': store_data['nearbyStores'],
                'clusterAvg': cluster_stats['avg_nearby_stores'],
                'unit': '개'
            })
        
        if store_data.get('footTraffic') and cluster_stats.get('avg_foot_traffic'):
            comparisons.append({
                'variable': '유동인구',
                'myStore': store_data['footTraffic'],
                'clusterAvg': cluster_stats['avg_foot_traffic'],
                'unit': '명'
            })
        
        return comparisons
    
    def _create_distribution_data(self, franchise: Dict) -> List[Dict]:
        """분포 데이터 생성"""
        cluster_franchises = data_loader.get_franchises_by_cluster(franchise['cluster_id'])
        
        # 위험도 구간별 분포
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
        
        distribution = []
        for i, label in enumerate(labels):
            count = len(cluster_franchises[
                (cluster_franchises['risk_score'] >= bins[i]) & 
                (cluster_franchises['risk_score'] < bins[i+1])
            ])
            
            # 우리 점포가 이 구간에 속하는지
            my_store_in_range = 1 if (
                franchise['risk_score'] >= bins[i] and 
                franchise['risk_score'] < bins[i+1]
            ) else 0
            
            distribution.append({
                'range': label,
                'cluster': count,
                'myStore': my_store_in_range
            })
        
        return distribution
    
    def _create_distribution_data_for_cluster(self, cluster_id: str) -> List[Dict]:
        """클러스터 분포 데이터"""
        cluster_franchises = data_loader.get_franchises_by_cluster(cluster_id)
        
        bins = [0, 20, 40, 60, 80, 100]
        labels = ['0-20', '20-40', '40-60', '60-80', '80-100']
        
        distribution = []
        for i, label in enumerate(labels):
            count = len(cluster_franchises[
                (cluster_franchises['risk_score'] >= bins[i]) & 
                (cluster_franchises['risk_score'] < bins[i+1])
            ])
            
            distribution.append({
                'range': label,
                'cluster': count,
                'myStore': 0
            })
        
        return distribution
    
    def _analyze_risk_factors(self, franchise: Dict, cluster_stats: Dict) -> List[Dict]:
        """위험 요인 분석"""
        factors = []
        
        # 1. 유동인구 변화율 확인
        if 'foot_traffic_change_rate' in franchise:
            change_rate = franchise['foot_traffic_change_rate']
            cluster_avg = cluster_stats.get('avg_foot_traffic_change_rate', 0)
            
            if change_rate < cluster_avg - 10:
                factors.append({
                    'factor': '유동인구 급감',
                    'severity': 'high',
                    'description': f'유동인구 변화율이 클러스터 평균보다 {abs(change_rate - cluster_avg):.1f}%p 낮습니다.',
                    'value': f'{change_rate}%',
                    'benchmark': f'{cluster_avg}%'
                })
        
        # 2. 경쟁 심화 확인
        if 'nearby_stores' in franchise:
            nearby = franchise['nearby_stores']
            cluster_avg = cluster_stats.get('avg_nearby_stores', 0)
            
            if nearby > cluster_avg * 1.3:
                factors.append({
                    'factor': '경쟁 심화',
                    'severity': 'medium',
                    'description': f'경쟁 점포 수가 클러스터 평균보다 {((nearby/cluster_avg - 1) * 100):.0f}% 많습니다.',
                    'value': f'{nearby}개',
                    'benchmark': f'{cluster_avg:.0f}개'
                })
        
        # 3. 높은 폐업 위험도
        if franchise['risk_score'] > 70:
            factors.append({
                'factor': '높은 폐업 위험도',
                'severity': 'high',
                'description': f'현재 폐업 위험도가 {franchise["risk_score"]:.0f}%로 매우 높습니다.'
            })
        
        return factors
    
    def _analyze_risk_factors_for_new(self, store_data: Dict, cluster_stats: Dict) -> List[Dict]:
        """신규 점포 위험 요인"""
        factors = []
        
        # 클러스터 평균 폐업률이 높은 경우
        closure_rate = cluster_stats.get('closure_rate', 0)
        if closure_rate > 25:
            factors.append({
                'factor': '높은 클러스터 폐업률',
                'severity': 'high',
                'description': f'이 클러스터의 평균 폐업률이 {closure_rate:.1f}%로 높습니다.'
            })
        elif closure_rate > 15:
            factors.append({
                'factor': '중간 수준 클러스터 폐업률',
                'severity': 'medium',
                'description': f'이 클러스터의 평균 폐업률이 {closure_rate:.1f}%입니다.'
            })
        
        return factors
    
    def _create_model_results(self, franchise: Dict) -> Dict:
        """모델 결과 생성"""
        # CSV에서 모델 결과를 가져오거나 기본값 사용
        return {
            'sales_prediction': franchise.get('sales_prediction', 0) or 0,
            'event_prediction': franchise.get('event_prediction', '정상 운영') or '정상 운영',
            'survival_probability': franchise.get('survival_probability', 100 - franchise.get('risk_score', 50)) or 50,
            'risk_score': franchise.get('risk_score', franchise.get('risk_score', 50)) or 50
        }
    
    def _create_cluster_indicators(self, franchise: Dict, cluster_stats: Dict) -> List[Dict]:
        """클러스터별 주요 지표 생성"""
        indicators = []
        cluster_id = franchise.get('cluster_id', '')
        
        # 클러스터별 주요 지표 정의
        if str(cluster_id) == '0':
            # Cluster 0 지표들 (예시: 10대 남성 비율, 영업일 수, 50대 여성 비율, 업종 내 매출 순위 하락)
            indicators.extend([
                {
                    'name': '10대 남성 비율',
                    'value': franchise.get('teen_male_ratio', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_teen_male_ratio', 0) or 0,
                    'unit': '%',
                    'description': '고객 중 10대 남성의 비율',
                    'isPositive': True
                },
                {
                    'name': '영업일 수',
                    'value': franchise.get('operating_days', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_operating_days', 0) or 0,
                    'unit': '일',
                    'description': '월 평균 영업일 수',
                    'isPositive': True
                },
                {
                    'name': '50대 여성 비율',
                    'value': franchise.get('adult_female_ratio', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_adult_female_ratio', 0) or 0,
                    'unit': '%',
                    'description': '고객 중 50대 여성의 비율',
                    'isPositive': True
                },
                {
                    'name': '업종 내 매출 순위 하락',
                    'value': franchise.get('industry_sales_rank_decline', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_industry_sales_rank_decline', 0) or 0,
                    'unit': '순위',
                    'description': '업종 내 매출 순위 하락 정도',
                    'isPositive': False  # 하락은 나쁨
                }
            ])
        elif str(cluster_id) == '1':
            # Cluster 1 지표들 (예시: 지역 폐업률, 지역 매출 순위 비율, 고객 다양성 범위)
            indicators.extend([
                {
                    'name': '지역 폐업률',
                    'value': franchise.get('district_closure_ratio', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_district_closure_ratio', 0) or 0,
                    'unit': '%',
                    'description': '같은 지역의 평균 폐업률',
                    'isPositive': False
                },
                {
                    'name': '지역 매출 순위 비율',
                    'value': franchise.get('district_sales_rank_ratio', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_district_sales_rank_ratio', 0) or 0,
                    'unit': '배',
                    'description': '지역 내 매출 순위 비율',
                    'isPositive': True
                },
                {
                    'name': '고객 다양성 범위',
                    'value': franchise.get('unique_customers_range_diff', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_unique_customers_range_diff', 0) or 0,
                    'unit': '명',
                    'description': '고유 고객 수의 변화 범위',
                    'isPositive': True
                }
            ])
        elif str(cluster_id) == '2':
            # Cluster 2 지표들 (예시: 특별한 지표들)
            indicators.extend([
                {
                    'name': '매출 성장률',
                    'value': franchise.get('sales_growth_rate', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_sales_growth_rate', 0) or 0,
                    'unit': '%',
                    'description': '월 매출 성장률',
                    'isPositive': True
                },
                {
                    'name': '고객 만족도',
                    'value': franchise.get('customer_satisfaction', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_customer_satisfaction', 0) or 0,
                    'unit': '점',
                    'description': '고객 만족도 점수',
                    'isPositive': True
                }
            ])
        elif str(cluster_id) == '3':
            # Cluster 3 지표들
            indicators.extend([
                {
                    'name': '임대료 효율성',
                    'value': franchise.get('rent_efficiency', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_rent_efficiency', 0) or 0,
                    'unit': '배',
                    'description': '매출 대비 임대료 효율성',
                    'isPositive': True
                },
                {
                    'name': '경쟁 강도',
                    'value': franchise.get('competition_intensity', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_competition_intensity', 0) or 0,
                    'unit': '점',
                    'description': '주변 경쟁 강도',
                    'isPositive': False
                }
            ])
        elif str(cluster_id) == '4':
            # Cluster 4 지표들
            indicators.extend([
                {
                    'name': '브랜드 인지도',
                    'value': franchise.get('brand_awareness', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_brand_awareness', 0) or 0,
                    'unit': '%',
                    'description': '지역 내 브랜드 인지도',
                    'isPositive': True
                },
                {
                    'name': '운영 효율성',
                    'value': franchise.get('operational_efficiency', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_operational_efficiency', 0) or 0,
                    'unit': '점',
                    'description': '운영 효율성 점수',
                    'isPositive': True
                }
            ])
        else:
            # 기본 지표들
            indicators.extend([
                {
                    'name': '월 임대료',
                    'value': franchise.get('monthly_rent', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_rent', 0) or 0,
                    'unit': '만원',
                    'description': '월 임대료',
                    'isPositive': False  # 낮을수록 좋음
                },
                {
                    'name': '경쟁점포 수',
                    'value': franchise.get('nearby_stores', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_nearby_stores', 0) or 0,
                    'unit': '개',
                    'description': '반경 500m 내 경쟁점포 수',
                    'isPositive': False  # 적을수록 좋음
                },
                {
                    'name': '유동인구',
                    'value': franchise.get('foot_traffic', 0) or 0,
                    'clusterAvg': cluster_stats.get('avg_foot_traffic', 0) or 0,
                    'unit': '명',
                    'description': '월 평균 유동인구',
                    'isPositive': True
                }
            ])
        
        return indicators
    
    def _create_sales_decline_data(self, franchise: Dict) -> List[Dict]:
        """매출 급감 예상 그래프 데이터 생성"""
        # CSV에서 그래프 데이터를 가져오거나 시뮬레이션
        months = ['1월', '2월', '3월', '4월', '5월', '6월']
        current_sales = franchise.get('current_sales', 1000) or 1000
        decline_rate = franchise.get('sales_decline_rate', 0.05) or 0.05
        
        data = []
        for i, month in enumerate(months):
            predicted_sales = current_sales * (1 - decline_rate * i)
            data.append({
                'month': month,
                'predictedSales': predicted_sales,
                'currentSales': current_sales if i == 0 else None
            })
        
        return data
    
    def _get_default_cluster_stats(self) -> Dict:
        """기본 클러스터 통계"""
        return {
            'cluster_id': 'UNKNOWN',
            'cluster_name': '미분류',
            'total_stores': 0,
            'closure_rate': 20.0,
            'avg_foot_traffic': 100000,
            'avg_rent': 300,
            'avg_nearby_stores': 30
        }


# 싱글톤 인스턴스
analyzer = Analyzer()