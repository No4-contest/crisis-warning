import pandas as pd
import pickle
import os
from pathlib import Path
from typing import Dict, List, Optional


class DataLoader:
    """CSV 파일 로드 및 전처리"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.models_dir = Path(__file__).parent.parent.parent / "models"
        
        # 데이터 캐시
        self._store_features = None
        self._store_diagnosis_results = None
        self._cluster_metadata = None
        self._feature_dictionary = None
        self._risk_checklist_rules = None
        self._store_monthly_timeseries = None
        self._sales_predict = None
    
    def load_store_features(self) -> pd.DataFrame:
        """점포 특성 데이터 로드"""
        if self._store_features is None:
            csv_path = self.data_dir / "1002_store_features.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"1002_store_features.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._store_features = pd.read_csv(csv_path)
            self._store_features.columns = self._store_features.columns.str.strip()
            print(f"✅ 점포 특성 데이터 로드 완료: {len(self._store_features)}개")
        
        return self._store_features
    
    def load_store_diagnosis_results(self) -> pd.DataFrame:
        """점포 진단 결과 데이터 로드"""
        if self._store_diagnosis_results is None:
            csv_path = self.data_dir / "store_diagnosis_results.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"store_diagnosis_results.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._store_diagnosis_results = pd.read_csv(csv_path)
            self._store_diagnosis_results.columns = self._store_diagnosis_results.columns.str.strip()
            print(f"✅ 점포 진단 결과 데이터 로드 완료: {len(self._store_diagnosis_results)}개")
        
        return self._store_diagnosis_results
    
    def load_cluster_metadata(self) -> pd.DataFrame:
        """클러스터 메타데이터 로드"""
        if self._cluster_metadata is None:
            csv_path = self.data_dir / "cluster_metadata.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"cluster_metadata.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._cluster_metadata = pd.read_csv(csv_path)
            self._cluster_metadata.columns = self._cluster_metadata.columns.str.strip()
            print(f"✅ 클러스터 메타데이터 로드 완료: {len(self._cluster_metadata)}개")
        
        return self._cluster_metadata
    
    def load_feature_dictionary(self) -> pd.DataFrame:
        """특성 사전 데이터 로드"""
        if self._feature_dictionary is None:
            csv_path = self.data_dir / "feature_dictionary.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"feature_dictionary.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._feature_dictionary = pd.read_csv(csv_path)
            self._feature_dictionary.columns = self._feature_dictionary.columns.str.strip()
            print(f"✅ 특성 사전 데이터 로드 완료: {len(self._feature_dictionary)}개")
        
        return self._feature_dictionary
    
    def load_risk_checklist_rules(self) -> pd.DataFrame:
        """위험 체크리스트 룰 데이터 로드"""
        if self._risk_checklist_rules is None:
            csv_path = self.data_dir / "risk_checklist_rules.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"risk_checklist_rules.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._risk_checklist_rules = pd.read_csv(csv_path)
            self._risk_checklist_rules.columns = self._risk_checklist_rules.columns.str.strip()
            print(f"✅ 위험 체크리스트 룰 데이터 로드 완료: {len(self._risk_checklist_rules)}개")
        
        return self._risk_checklist_rules
    
    def load_store_monthly_timeseries(self) -> pd.DataFrame:
        """점포 월별 시계열 데이터 로드"""
        if self._store_monthly_timeseries is None:
            csv_path = self.data_dir / "store_monthly_timeseries.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"store_monthly_timeseries.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._store_monthly_timeseries = pd.read_csv(csv_path)
            self._store_monthly_timeseries.columns = self._store_monthly_timeseries.columns.str.strip()
            print(f"✅ 점포 월별 시계열 데이터 로드 완료: {len(self._store_monthly_timeseries)}개")
        
        return self._store_monthly_timeseries
    
    def load_sales_predict(self) -> pd.DataFrame:
        """매출 예측 데이터 로드"""
        if self._sales_predict is None:
            csv_path = self.data_dir / "sales_predict_result.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"sales_predict_result.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._sales_predict = pd.read_csv(csv_path)
            self._sales_predict.columns = self._sales_predict.columns.str.strip()
            print(f"✅ 매출 예측 데이터 로드 완료: {len(self._sales_predict)}개")
        
        return self._sales_predict
    
    def get_store_by_id(self, store_id: str) -> Optional[Dict]:
        """ID로 점포 조회"""
        df = self.load_store_features()
        result = df[df['store_id'] == store_id]
        
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_store_location_info(self, store_id: str) -> Optional[Dict]:
        """점포 위치 정보 조회 (1002_store_features.csv에서)"""
        store_data = self.get_store_by_id(store_id)
        if not store_data:
            return None
        
        # 필요한 위치 정보만 추출
        return {
            'business_district': store_data.get('business_district', ''),
            'region': store_data.get('region_3depth_name', ''),
            'store_name': store_data.get('store_name', '')
        }
    
    def get_store_diagnosis_results(self, store_id: str) -> Optional[Dict]:
        """점포 진단 결과 조회"""
        df = self.load_store_diagnosis_results()
        # store_id로 store_index를 찾아야 함
        store_features = self.load_store_features()
        store_row = store_features[store_features['store_id'] == store_id]
        if store_row.empty:
            return None
        
        store_index = store_row.index[0]  # pandas 인덱스 사용
        result = df[df['store_index'] == store_index]
        
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_cluster_metadata(self, cluster_id: str) -> Optional[Dict]:
        """클러스터 메타데이터 조회"""
        df = self.load_cluster_metadata()
        # cluster_id를 정수로 변환해서 비교
        cluster_id_int = int(cluster_id)
        result = df[df['cluster_id'] == cluster_id_int]
        
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_feature_korean_name(self, feature: str) -> str:
        """특성의 한국어 이름 조회"""
        df = self.load_feature_dictionary()
        result = df[df['feature'] == feature]
        
        if result.empty:
            return feature  # 한국어 이름이 없으면 원래 이름 반환
        
        return result.iloc[0]['feature_korean']
    
    def get_rules_for_cluster(self, cluster_id: str) -> List[Dict]:
        """특정 클러스터의 룰 목록 조회"""
        df = self.load_risk_checklist_rules()
        # cluster_id를 정수로 변환해서 비교
        cluster_id_int = int(cluster_id)
        print(f"🔍 디버깅 get_rules_for_cluster: cluster_id = {cluster_id}, cluster_id_int = {cluster_id_int}")
        print(f"🔍 디버깅 get_rules_for_cluster: df['cluster_id'].unique() = {df['cluster_id'].unique()}")
        print(f"🔍 디버깅 get_rules_for_cluster: df['cluster_id'].dtype = {df['cluster_id'].dtype}")
        result = df[df['cluster_id'] == cluster_id_int]
        print(f"🔍 디버깅 get_rules_for_cluster: result 길이 = {len(result)}")
        
        if result.empty:
            return []
        
        return result.to_dict('records')
    
    def get_store_monthly_timeseries(self, store_id: str) -> Optional[Dict]:
        """점포 월별 시계열 데이터 조회"""
        df = self.load_store_monthly_timeseries()
        # store_id로 직접 조회 (업데이트된 CSV 구조)
        result = df[df['store_id'] == store_id]
        
        if result.empty:
            return None
        
        # 시계열 데이터를 월별로 정리
        timeseries_data = {}
        for _, row in result.iterrows():
            date_str = row['date']
            month = date_str[:7]  # YYYY-MM 형식
            timeseries_data[month] = {
                'sales': row['sales']  # sales는 등급 (1-6)
            }
        
        return timeseries_data
    
    def get_sales_predictions(self, store_id: str) -> List[Dict]:
        """점포의 매출 예측 데이터 조회 (모든 horizon 포함)"""
        df = self.load_sales_predict()
        result = df[df['store_id'] == store_id]
        
        if result.empty:
            return []
        
        # horizon별로 정렬 (1, 2, 3개월)
        result = result.sort_values('horizon')
        
        return result.to_dict('records')
    
    def calculate_rule_violations(self, store_id: str) -> List[Dict]:
        """점포의 룰 위반 계산"""
        store_data = self.get_store_by_id(store_id)
        if not store_data:
            return []
        
        cluster_id = store_data.get('static_cluster', '0')
        rules = self.get_rules_for_cluster(cluster_id)
        violations = []
        
        for rule in rules:
            feature = rule['feature']
            threshold = rule['threshold']
            direction = rule['direction']
            risk_level = rule['risk_level']
            rule_text = rule['rule_text']
            feature_korean = rule['feature_korean']
            
            # 점포의 해당 특성 값 조회
            if feature in store_data:
                current_value = store_data[feature]
                
                # 룰 위반 여부 판정
                is_violated = False
                if direction == '<=' and current_value <= threshold:
                    is_violated = True
                elif direction == '>=' and current_value >= threshold:
                    is_violated = True
                
                if is_violated:
                    violations.append({
                        'ruleText': rule_text,
                        'riskLevel': risk_level,
                        'featureKorean': feature_korean,
                        'currentValue': current_value,
                        'threshold': threshold,
                        'direction': direction
                    })
        
        return violations


# 싱글톤 인스턴스
data_loader = DataLoader()