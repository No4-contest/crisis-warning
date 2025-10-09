import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from app.services.data_loader import data_loader


class Analyzer:
    """가맹점 데이터 분석"""
    
    def analyze_franchise(self, franchise_id: str) -> Dict:
        """기존 가맹점 종합 분석"""
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
        
        # 4. 비교 데이터 생성
        comparison_data = self._create_comparison_data(franchise, cluster_stats)
        
        # 5. 분포 데이터 생성
        distribution_data = self._create_distribution_data(franchise)
        
        # 6. 위험 요인 분석
        risk_factors = self._analyze_risk_factors(franchise, cluster_stats)
        
        return {
            'franchise': franchise,
            'cluster_stats': cluster_stats,
            'industry_stats': industry_stats,
            'comparison_data': comparison_data,
            'distribution_data': distribution_data,
            'risk_factors': risk_factors
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
            'closure_risk': cluster_stats.get('closure_rate', 50.0),
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
                (cluster_franchises['closure_risk'] >= bins[i]) & 
                (cluster_franchises['closure_risk'] < bins[i+1])
            ])
            
            # 우리 점포가 이 구간에 속하는지
            my_store_in_range = 1 if (
                franchise['closure_risk'] >= bins[i] and 
                franchise['closure_risk'] < bins[i+1]
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
                (cluster_franchises['closure_risk'] >= bins[i]) & 
                (cluster_franchises['closure_risk'] < bins[i+1])
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
        if franchise['closure_risk'] > 70:
            factors.append({
                'factor': '높은 폐업 위험도',
                'severity': 'high',
                'description': f'현재 폐업 위험도가 {franchise["closure_risk"]:.0f}%로 매우 높습니다.'
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