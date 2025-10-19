import os
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()


class LLMService:
    """LLM 기반 전략 제안"""
    
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY") or os.getenv("ANTHROPIC_API_KEY")
        self.provider = "openai" if os.getenv("OPENAI_API_KEY") else "anthropic"
        
        if not self.api_key:
            print("⚠️  LLM API 키가 설정되지 않았습니다. 기본 전략을 사용합니다.")
    
    def generate_strategy(self, analysis_data: Dict) -> Dict:
        """분석 데이터 기반 전략 생성"""
        
        if not self.api_key:
            # API 키가 없으면 기본 전략 반환
            return self._get_default_strategy(analysis_data)
        
        # 프롬프트 생성
        prompt = self._create_prompt(analysis_data)
        
        try:
            if self.provider == "openai":
                return self._call_openai(prompt)
            else:
                return self._call_anthropic(prompt)
        except Exception as e:
            print(f"❌ LLM 호출 실패: {e}")
            return self._get_default_strategy(analysis_data)
    
    def _create_prompt(self, data: Dict) -> str:
        """프롬프트 생성"""
        franchise = data['franchise']
        cluster_stats = data['cluster_stats']
        model_results = data.get('model_results', {})
        cluster_indicators = data.get('cluster_indicators', [])
        
        prompt = f"""
다음 가맹점의 폐업 위험을 분석하고 생존 전략을 제안해주세요.

## 가맹점 정보
- 상권: {franchise['trading_area']}
- 업종: {franchise['industry']}
- 클러스터: {cluster_stats.get('cluster_name', 'N/A')}
- 폐업 위험도: {franchise['risk_score']:.1f}점
- 클러스터 평균 폐업률: {cluster_stats.get('closure_rate', 0):.1f}%

## 모델 예측 결과
- 매출 예측: {model_results.get('sales_prediction', 0):.0f}만원
- 생존 가능성: {model_results.get('survival_probability', 0):.1f}%
- 이벤트 예측: {model_results.get('event_prediction', 'N/A')}

## 주요 지표 분석
"""
        if cluster_indicators:
            for indicator in cluster_indicators[:5]:  # 상위 5개 지표만 사용
                prompt += f"- {indicator['name']}: {indicator['value']:.1f}{indicator['unit']} (클러스터 평균: {indicator['clusterAvg']:.1f}{indicator['unit']})\n"
        else:
            prompt += "- 지표 데이터가 없습니다.\n"
        
        prompt += """

## 요청사항
1. 이 가맹점의 전반적인 상황을 1-2문장으로 요약해주세요.
2. 구체적이고 실행 가능한 생존 전략 4가지를 제안해주세요.
3. 각 전략은 이모지와 함께 "**제목**: 설명" 형식으로 작성해주세요.

## 응답 형식
summary: (전체 요약)
strategies:
- 🎯 **전략1 제목**: 상세 설명
- 📱 **전략2 제목**: 상세 설명
- 💰 **전략3 제목**: 상세 설명
- 📊 **전략4 제목**: 상세 설명
"""
        return prompt
    
    def _call_openai(self, prompt: str) -> Dict:
        """OpenAI API 호출"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "당신은 가맹점 경영 컨설턴트입니다."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            return self._parse_llm_response(content)
            
        except Exception as e:
            print(f"OpenAI 호출 실패: {e}")
            raise
    
    def _call_anthropic(self, prompt: str) -> Dict:
        """Anthropic API 호출"""
        try:
            import anthropic
            
            client = anthropic.Anthropic(api_key=self.api_key)
            
            message = client.messages.create(
                model="claude-3-sonnet-20240229",
                max_tokens=1000,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            content = message.content[0].text
            return self._parse_llm_response(content)
            
        except Exception as e:
            print(f"Anthropic 호출 실패: {e}")
            raise
    
    def _parse_llm_response(self, content: str) -> Dict:
        """LLM 응답 파싱"""
        lines = content.strip().split('\n')
        
        summary = ""
        strategies = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            if line.startswith("summary:"):
                current_section = "summary"
                summary = line.replace("summary:", "").strip()
            elif line.startswith("strategies:"):
                current_section = "strategies"
            elif line.startswith("-") or line.startswith("•"):
                if current_section == "strategies":
                    strategies.append(line.lstrip("-•").strip())
            elif current_section == "summary" and not summary:
                summary = line
        
        # 기본값 설정
        if not summary:
            summary = "분석 결과를 기반으로 전략을 제안합니다."
        
        if not strategies:
            strategies = [
                "🎯 **차별화 전략**: 경쟁사 대비 독특한 가치를 제공하세요.",
                "📱 **디지털 마케팅**: 온라인 채널을 통한 고객 유입을 늘리세요.",
                "💰 **비용 최적화**: 불필요한 지출을 줄이고 효율성을 높이세요.",
                "📊 **데이터 분석**: 고객 데이터를 활용한 의사결정을 하세요."
            ]
        
        return {
            'summary': summary,
            'strategies': strategies
        }
    
    def _get_default_strategy(self, data: Dict) -> Dict:
        """기본 전략 (API 키 없을 때)"""
        franchise = data['franchise']
        risk_level = franchise['risk_score']
        
        if risk_level >= 70:
            summary = "이 가맹점은 **고위험군**에 속합니다. 즉각적인 개선 조치가 필요합니다."
            strategies = [
                "🎯 **긴급 차별화 전략**: 경쟁사와 명확히 구분되는 독특한 메뉴나 서비스를 즉시 도입하세요.",
                "📱 **디지털 마케팅 강화**: SNS, 배달앱을 통한 온라인 고객 유입을 최우선으로 확대하세요.",
                "💰 **비용 구조 재검토**: 임대료 재협상, 재고 최적화 등으로 고정비용을 즉시 낮추세요.",
                "📊 **고객 데이터 분석**: 단골 고객의 특성을 파악하고 집중 공략하여 재방문율을 높이세요."
            ]
        elif risk_level >= 40:
            summary = "이 가맹점은 **중위험군**에 속합니다. 예방적 조치로 위험을 낮출 수 있습니다."
            strategies = [
                "🎯 **차별화 포인트 발굴**: 주변 경쟁점포와 차별화할 수 있는 요소를 찾아 강화하세요.",
                "📱 **온라인 마케팅 확대**: 지역 커뮤니티와 SNS를 활용한 브랜드 인지도를 높이세요.",
                "💰 **수익성 개선**: 인기 메뉴 중심으로 운영 효율화를 진행하세요.",
                "📊 **고객 만족도 관리**: 리뷰 관리와 피드백 수집으로 서비스 품질을 개선하세요."
            ]
        else:
            summary = "이 가맹점은 **저위험군**에 속합니다. 현재 상태를 유지하고 성장을 준비하세요."
            strategies = [
                "🎯 **브랜드 강화**: 현재의 강점을 더욱 발전시켜 지역 대표 브랜드로 성장하세요.",
                "📱 **고객 충성도 프로그램**: 멤버십, 포인트 제도로 단골 고객을 늘리세요.",
                "💰 **추가 수익원 발굴**: 신메뉴 개발, 제휴 마케팅 등으로 매출을 확대하세요.",
                "📊 **데이터 기반 의사결정**: 판매 데이터 분석으로 전략적 운영을 강화하세요."
            ]
        
        return {
            'summary': summary,
            'strategies': strategies
        }


# 싱글톤 인스턴스
llm_service = LLMService()