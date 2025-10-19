import pandas as pd
import pickle
import os
from pathlib import Path


class DataLoader:
    """CSV 파일 로드 및 전처리"""
    
    def __init__(self):
        self.data_dir = Path(__file__).parent.parent.parent / "data"
        self.models_dir = Path(__file__).parent.parent.parent / "models"
        
        # 데이터 캐시
        self._franchises = None
        self._clusters = None
        self._statistics = None
        self._cluster_model = None
        self._scaler = None
    
    def load_franchises(self) -> pd.DataFrame:
        """가맹점 데이터 로드"""
        if self._franchises is None:
            csv_path = self.data_dir / "franchises.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"franchises.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._franchises = pd.read_csv(csv_path)
            # 컬럼명 정리 (공백 제거)
            self._franchises.columns = self._franchises.columns.str.strip()
            print(f"✅ 가맹점 데이터 로드 완료: {len(self._franchises)}개")
        
        return self._franchises
    
    def load_clusters(self) -> pd.DataFrame:
        """클러스터 통계 데이터 로드"""
        if self._clusters is None:
            csv_path = self.data_dir / "clusters.csv"
            if not csv_path.exists():
                raise FileNotFoundError(f"clusters.csv 파일을 찾을 수 없습니다: {csv_path}")
            
            self._clusters = pd.read_csv(csv_path)
            self._clusters.columns = self._clusters.columns.str.strip()
            print(f"✅ 클러스터 데이터 로드 완료: {len(self._clusters)}개")
        
        return self._clusters
    
    def load_statistics(self) -> pd.DataFrame:
        """변수별 통계 데이터 로드 (선택사항)"""
        if self._statistics is None:
            csv_path = self.data_dir / "statistics.csv"
            if csv_path.exists():
                self._statistics = pd.read_csv(csv_path)
                self._statistics.columns = self._statistics.columns.str.strip()
                print(f"✅ 통계 데이터 로드 완료")
            else:
                print("⚠️  statistics.csv 파일이 없습니다 (선택사항)")
                self._statistics = pd.DataFrame()
        
        return self._statistics
    
    def load_cluster_model(self):
        """학습된 클러스터링 모델 로드"""
        if self._cluster_model is None:
            model_path = self.models_dir / "cluster_model.pkl"
            if not model_path.exists():
                raise FileNotFoundError(f"cluster_model.pkl 파일을 찾을 수 없습니다: {model_path}")
            
            with open(model_path, 'rb') as f:
                self._cluster_model = pickle.load(f)
            print("✅ 클러스터링 모델 로드 완료")
        
        return self._cluster_model
    
    def load_scaler(self):
        """스케일러 로드 (있을 경우)"""
        if self._scaler is None:
            scaler_path = self.models_dir / "scaler.pkl"
            if scaler_path.exists():
                with open(scaler_path, 'rb') as f:
                    self._scaler = pickle.load(f)
                print("✅ 스케일러 로드 완료")
            else:
                print("⚠️  scaler.pkl 파일이 없습니다 (선택사항)")
        
        return self._scaler
    
    def get_franchise_by_id(self, franchise_id: str) -> dict:
        """ID로 가맹점 조회"""
        df = self.load_franchises()
        result = df[df['franchise_id'] == franchise_id]
        
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_cluster_stats(self, cluster_id: str) -> dict:
        """클러스터 통계 조회"""
        df = self.load_clusters()
        result = df[df['cluster_id'] == cluster_id]
        
        if result.empty:
            return None
        
        return result.iloc[0].to_dict()
    
    def get_franchises_by_cluster(self, cluster_id: str) -> pd.DataFrame:
        """특정 클러스터의 모든 가맹점 조회"""
        df = self.load_franchises()
        return df[df['cluster_id'] == cluster_id]
    
    def get_industry_stats(self, industry: str) -> dict:
        """업종별 통계 계산"""
        df = self.load_franchises()
        industry_data = df[df['industry'] == industry]
        
        if industry_data.empty:
            return None
        
        # is_closed 컬럼이 없으므로 risk_score를 기반으로 폐업률 추정
        # risk_score가 70 이상이면 폐업 위험으로 간주
        high_risk_count = len(industry_data[industry_data['risk_score'] >= 70])
        estimated_closure_rate = (high_risk_count / len(industry_data)) * 100
        
        return {
            'total_stores': len(industry_data),
            'closure_rate': estimated_closure_rate,
            'avg_closure_risk': industry_data['risk_score'].mean()
        }


# 싱글톤 인스턴스
data_loader = DataLoader()