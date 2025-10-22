import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from app.services.data_loader import data_loader


class Analyzer:
    """가맹점 데이터 분석"""
    
    def generate_franchise_report(self, store_id: str) -> Dict:
        """가맹점 리포트 생성"""
        # 1. 점포 정보 가져오기
        store_data = data_loader.get_store_by_id(store_id) 
        # print(f"🔍 디버깅: store_data = {store_data}")
        if not store_data:
            print(f"❌ 오류: store_id {store_id}를 찾을 수 없습니다.")
            raise ValueError(f"점포 ID {store_id}를 찾을 수 없습니다.")
    
        
        # 2. 위치 정보 가져오기
        print(f"🔍 디버깅: 위치 정보 조회 시작")
        location_info = data_loader.get_store_location_info(store_id)
        print(f"🔍 디버깅: location_info = {location_info}")
        
        # 3. 진단 결과 가져오기
        print(f"🔍 디버깅: 진단 결과 조회 시작")
        diagnosis_results = data_loader.get_store_diagnosis_results(store_id)
        print(f"🔍 디버깅: diagnosis_results = {diagnosis_results}")
        
        # 4. 클러스터 메타데이터 가져오기
        cluster_id = str(store_data.get('static_cluster', '0'))
        print(f"🔍 디버깅: cluster_id = {cluster_id}")
        cluster_metadata = data_loader.get_cluster_metadata(cluster_id)
        print(f"🔍 디버깅: cluster_metadata = {cluster_metadata}")
        
        # 5. 월별 시계열 데이터 가져오기
        print(f"🔍 디버깅: 시계열 데이터 조회 시작")
        timeseries_data = data_loader.get_store_monthly_timeseries(store_id)
        print(f"🔍 디버깅: timeseries_data = {timeseries_data}")
        
        # 6. 룰 위반 계산
        print(f"🔍 디버깅: 룰 위반 계산 시작")
        rule_violations = data_loader.calculate_rule_violations(store_id)
        print(f"🔍 디버깅: rule_violations = {rule_violations}")
        
        # 7. 모델 결과 생성
        print(f"🔍 디버깅: 모델 결과 생성 시작")
        model_results = self._create_model_results(store_data, diagnosis_results)
        print(f"🔍 디버깅: model_results = {model_results}")
        
        # 8. 클러스터별 주요 지표 생성
        print(f"🔍 디버깅: 클러스터 지표 생성 시작")
        print(f"🔍 디버깅: cluster_id = {cluster_id}")
        print(f"🔍 디버깅: cluster_metadata = {cluster_metadata}")
        cluster_indicators = self._create_cluster_indicators(store_data, cluster_metadata)
        print(f"🔍 디버깅: cluster_indicators = {cluster_indicators}")
        print(f"🔍 디버깅: cluster_indicators 길이 = {len(cluster_indicators)}")
        
        # 9. 매출 예측 데이터 가져오기
        print(f"🔍 디버깅: 매출 예측 조회 시작")
        sales_predictions = data_loader.get_sales_predictions(store_id)
        print(f"🔍 디버깅: sales_predictions = {sales_predictions}")
        
        # 10. 트렌드 데이터 생성 (실제 6개월 + 예측 3개월 + 클러스터 순위)
        print(f"🔍 디버깅: 통합 트렌드 데이터 생성 시작")
        trend_data = self._create_enhanced_trend_data(store_data, timeseries_data, sales_predictions)
        print(f"🔍 디버깅: trend_data = {trend_data}")
        
        # 11. 통계 정보 생성
        print(f"🔍 디버깅: 통계 정보 생성 시작")
        statistics = self._create_statistics(store_data, cluster_metadata)
        print(f"🔍 디버깅: statistics = {statistics}")
        
        return {
            'store_data': store_data,
            'location_info': location_info,
            'diagnosis_results': diagnosis_results,
            'cluster_metadata': cluster_metadata,
            'timeseries_data': timeseries_data,
            'rule_violations': rule_violations,
            'model_results': model_results,
            'cluster_indicators': cluster_indicators,
            'trend_data': trend_data,
            'sales_predictions': sales_predictions,
            'statistics': statistics
        }
    
    def _create_model_results(self, store_data: Dict, diagnosis_results: Dict) -> Dict:
        """모델 결과 생성"""
        if diagnosis_results and isinstance(diagnosis_results, dict):
            # inf, -inf 값을 안전한 값으로 변환
            def safe_float(value, default=0):
                if value is None or value != value or value == float('inf') or value == float('-inf'):
                    return default
                return float(value)
            
            risk_score = safe_float(diagnosis_results.get('total_risk_score', 50), 50)
            
            # 생존 가능성 계산: 100 - risk_score (0-100 범위로 제한)
            if risk_score == 50:  # 기본값인 경우
                survival_probability = 50.0
            else:
                survival_probability = max(0, min(100, 100 - risk_score))
            
            return {
                'sales_prediction': safe_float(diagnosis_results.get('sales_prediction', 0), 0),
                'event_prediction': diagnosis_results.get('event_prediction', '정상 운영') or '정상 운영',
                'survival_probability': survival_probability,
                'risk_score': risk_score
            }
        else:
            # 기본값 사용
            return {
                'sales_prediction': 0,
                'event_prediction': '정상 운영',
                'survival_probability': 50,
                'risk_score': 50
            }
    
    def _create_trend_data(self, timeseries_data: Dict) -> List[Dict]:
        """트렌드 데이터 생성 (기본)"""
        if not timeseries_data:
            return []
        
        trend_data = []
        # 월별 매출 데이터 처리
        for month, data in timeseries_data.items():
            trend_data.append({
                'month': month,
                'value': data.get('sales', 0),
                'type': 'sales'
            })
        
        # 월별로 정렬
        trend_data.sort(key=lambda x: x['month'])
        
        return trend_data
    
    def _create_enhanced_trend_data(self, store_data: Dict, timeseries_data: Dict, sales_predictions: List[Dict]) -> List[Dict]:
        """통합 트렌드 데이터 생성 (실제 등급 + 예측 등급 + 클러스터 순위)"""
        trend_data = []
        
        # 1. 실제 월별 등급 데이터 (최근 6개월)
        if timeseries_data:
            sorted_months = sorted(timeseries_data.keys(), reverse=True)[:6]  # 최근 6개월
            sorted_months.reverse()  # 오래된 순으로 정렬
            
            for month in sorted_months:
                data = timeseries_data[month]
                sales_grade = data.get('sales', 0)
                # 등급을 순위 비율로 변환 (1=상위, 6=하위)
                cluster_rank_ratio = (7 - sales_grade) / 6.0 if sales_grade else 0.5
                
                trend_data.append({
                    'month': month,
                    'salesGrade': sales_grade,  # 실제 등급 (1-6)
                    'type': 'actual',
                    'clusterRank': cluster_rank_ratio  # 0-1 (1=상위)
                })
        
        # 2. 예측 3개월 데이터 (sales_predictions에서)
        if sales_predictions and len(sales_predictions) > 0:
            for pred in sales_predictions:
                # yhatGrade를 순위 비율로 변환 (1=상위, 6=하위)
                cluster_rank_ratio = (7 - pred['yhat_grade']) / 6.0
                
                trend_data.append({
                    'month': pred['target_month'],
                    'salesGrade': pred['yhat_grade'],  # 예측 등급 (1-6)
                    'type': 'forecast',
                    'clusterRank': cluster_rank_ratio,  # 0-1 사이 값 (1=상위)
                    'pLow56': pred['p_low56'],
                    'riskWorsen': pred['risk_worsen_ge2']
                })
        
        # 월별로 정렬
        trend_data.sort(key=lambda x: x['month'])
        
        return trend_data
    
    def _create_statistics(self, store_data: Dict, cluster_metadata: Dict) -> Dict:
        """통계 정보 생성"""
        return {
            'clusterClosureRate': cluster_metadata.get('closure_rate', 0) if cluster_metadata and isinstance(cluster_metadata, dict) else 0,
            'industryAvgClosureRate': 15.0,  # 기본값
            'nearbyStores': store_data.get('nearby_stores', 0) or 0,
            'avgMonthlyFootTraffic': store_data.get('foot_traffic', 0) or 0,
            'rentIncreaseRate': store_data.get('rent_increase_rate', 0) or 0
        }
    
    def _create_cluster_indicators(self, store_data: Dict, cluster_metadata: Dict) -> List[Dict]:
        """클러스터별 주요 지표 생성"""
        indicators = []
        cluster_id = str(store_data.get('static_cluster', '0'))
        
        # cluster_metadata가 None이거나 dict가 아닌 경우 기본값 사용
        if not cluster_metadata or not isinstance(cluster_metadata, dict):
            cluster_metadata = {}
        
        # risk_checklist_rules에서 해당 클러스터의 규칙들을 가져와서 지표 생성
        print(f"🔍 디버깅 BEFORE get_rules_for_cluster: cluster_id = {cluster_id}, type = {type(cluster_id)}")
        rules = data_loader.get_rules_for_cluster(cluster_id)
        print(f"🔍 디버깅 AFTER get_rules_for_cluster: rules 길이 = {len(rules) if rules else 0}")
        print(f"🔍 디버깅 AFTER get_rules_for_cluster: rules = {rules[:2] if rules else []}")  # 처음 2개만 출력
        
        for rule in rules[:5]:  # 상위 5개 규칙만 사용
            feature = rule['feature']
            threshold = rule['threshold']
            feature_korean = rule['feature_korean']
            risk_level = rule['risk_level']
            direction = rule['direction']
            
            # 점포의 해당 feature 값 가져오기
            store_value = store_data.get(feature, 0) or 0
            
            # 클러스터 평균은 임계값을 사용 (실제 평균 데이터가 없으므로)
            cluster_avg = threshold
            
            # 방향에 따라 isPositive 결정
            is_positive = direction == '>='  # >= 이면 높을수록 좋음, <= 이면 낮을수록 좋음
            
            # 단위 결정
            unit = '%' if 'ratio' in feature else '회' if 'count' in feature else '점'
            
            indicators.append({
                'name': feature_korean,
                'value': store_value,
                'clusterAvg': cluster_avg,
                'unit': unit,
                'description': f'{feature_korean} ({risk_level})',
                'isPositive': is_positive,
                'riskLevel': risk_level
            })
        
        return indicators


# 싱글톤 인스턴스
analyzer = Analyzer()
