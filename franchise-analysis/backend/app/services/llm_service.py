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
            # API 키가 없으면 데이터 기반 기본 전략 반환
            print("⚠️  LLM API 키 없음 - 데이터 기반 기본 전략 사용")
            return self._get_default_strategy(analysis_data)
        
        # 프롬프트 생성
        prompt = self._create_prompt(analysis_data)
        
        try:
            if self.provider == "openai":
                result = self._call_openai(prompt, analysis_data)
            else:
                result = self._call_anthropic(prompt, analysis_data)
            
            print(f"✅ LLM 전략 생성 성공")
            return result
        except Exception as e:
            print(f"❌ LLM 호출 실패: {e}")
            print(f"🔄 데이터 기반 기본 전략으로 전환")
            return self._get_default_strategy(analysis_data)
    
    def _create_prompt(self, data: Dict) -> str:
        """프롬프트 생성 (실제 데이터 구조 반영)"""
        store_data = data['store_data']
        location_info = data.get('location_info', {})
        cluster_metadata = data.get('cluster_metadata', {})
        diagnosis_results = data.get('diagnosis_results', {})
        model_results = data.get('model_results', {})
        cluster_indicators = data.get('cluster_indicators', [])
        rule_violations = data.get('rule_violations', [])
        trend_data = data.get('trend_data', [])
        
        # 클러스터 요약 정보 추출
        cluster_summary = cluster_metadata.get('summary_text', '') if cluster_metadata else ''
        
        # 최근 매출 등급 추세 분석 (실제 데이터)
        actual_trends = [t for t in trend_data if t['type'] == 'actual']
        forecast_trends = [t for t in trend_data if t['type'] == 'forecast']
        
        trend_description = ""
        if actual_trends:
            recent_grades = [t['salesGrade'] for t in actual_trends[-3:]]  # 최근 3개월
            avg_grade = sum(recent_grades) / len(recent_grades)
            trend_description = f"최근 3개월 평균 매출 등급: {avg_grade:.1f}등급 (1등급이 가장 높음)"
        
        # 예측 트렌드
        forecast_description = ""
        if forecast_trends:
            forecast_grades = [t['salesGrade'] for t in forecast_trends]
            risk_worsen = forecast_trends[-1].get('riskWorsen', 0) * 100
            forecast_description = f"향후 3개월 예측 등급: {forecast_grades[0]}등급, 악화 위험률: {risk_worsen:.1f}%"
        
        prompt = f"""
다음 가맹점의 폐업 위험을 분석하고 생존 전략을 제안해주세요.

## 가맹점 정보
- 점포명: {store_data.get('store_name', 'N/A')}
- 상권: {location_info.get('business_district', 'N/A')} ({location_info.get('region', 'N/A')})
- 클러스터: {cluster_metadata.get('cluster_name', 'N/A') if cluster_metadata else 'N/A'}
- 클러스터 특성: {cluster_summary}

## 위험도 진단
- 위험도 점수: {diagnosis_results.get('total_risk_score', 50):.1f}점 (100점 만점)
- 룰 위반 건수: {diagnosis_results.get('n_violations', 0)}건 (치명적: {diagnosis_results.get('n_critical_violations', 0)}건)

## 매출 트렌드
- {trend_description}
- {forecast_description}

## 위반된 주요 룰 (상위 3개)
    """
        
        if rule_violations:
            for i, violation in enumerate(rule_violations[:3], 1):
                current = violation['currentValue']
                threshold = violation['threshold']
                feature = violation['featureKorean']
                prompt += f"{i}. [{violation['riskLevel']}] {feature}: 현재 {current:.1f}% (기준: {threshold:.1f}%)\n"
        else:
            prompt += "- 위반된 룰이 없습니다.\n"
        
        prompt += "\n## 클러스터 대비 주요 지표\n"
        if cluster_indicators:
            for indicator in cluster_indicators[:5]:
                value = indicator['value']
                avg = indicator['clusterAvg']
                diff = value - avg
                diff_sign = "▲" if diff > 0 else "▼"
                prompt += f"- {indicator['name']}: {value:.1f}{indicator['unit']} (클러스터 평균 대비 {diff_sign}{abs(diff):.1f}{indicator['unit']})\n"
        else:
            prompt += "- 지표 데이터가 없습니다.\n"
        
        prompt += """

## 요청사항
0. 존댓말로 해주세요. 가맹점주에게 제안을 하는 상황입니다.

1. 이 가맹점의 전반적인 상황을 **1-2문장**으로 명확하게 요약하세요.
- 위험도 수준, 주요 문제점, 예측 트렌드를 포함하세요.

2. 생존 전략 4가지를 제안하세요.
- 각 전략은 **점주가 즉시 실행 가능**해야 합니다.
- 모호한 조언(예: "마케팅 강화")은 금지합니다.
- 구체적 실행 방법과 예상 효과를 명시하세요.

4. 각 전략은 아래 형식을 따르세요:
- **전략 제목**: 구체적 실행 방법 서술

5. 답변은 아래 형식으로만 출력하세요.

## 응답 형식
summary: (1-2문장 요약)
strategies:
- 🎯 **전략1 제목**: 상세 설명 (실행 주체, 방법, 예상 효과 포함)
- 📱 **전략2 제목**: 상세 설명
- 💰 **전략3 제목**: 상세 설명
- 📊 **전략4 제목**: 상세 설명
"""
        
        return prompt
    
    def _call_openai(self, prompt: str, analysis_data: Dict = None) -> Dict:
        """OpenAI API 호출"""
        try:
            import openai
            openai.api_key = self.api_key
            
            response = openai.ChatCompletion.create(
                model="gpt-4o-mini",  # 더 빠른 모델 (3-5초 vs 20-30초)
                messages=[
                    {"role": "system", "content": "당신은 프랜차이즈 본사의 데이터 기반 경영 컨설턴트입니다. "
            "가맹점의 데이터를 바탕으로 폐업 위험을 진단하고, 점주가 즉시 실행할 수 있는 생존 전략을 제시합니다. "
            "응답은 반드시 JSON 형식으로 출력해야 합니다. 설명 문장은 포함하지 마세요."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800  # 토큰 감소로 속도 향상
            )
            
            content = response.choices[0].message.content
            print(f"📝 GPT-4 응답:\n{content}\n" + "="*50)
            return self._parse_llm_response(content, analysis_data)
            
        except Exception as e:
            print(f"OpenAI 호출 실패: {e}")
            raise
    
    def _call_anthropic(self, prompt: str, analysis_data: Dict = None) -> Dict:
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
            return self._parse_llm_response(content, analysis_data)
            
        except Exception as e:
            print(f"Anthropic 호출 실패: {e}")
            raise
    
    def _parse_llm_response(self, content: str, analysis_data: Dict = None) -> Dict:
        """LLM 응답 파싱 (개선된 버전)"""
        import re
        
        lines = content.strip().split('\n')
        
        summary = ""
        strategies = []
        current_section = None
        
        for line in lines:
            line = line.strip()
            if not line:
                continue
            
            # summary 찾기 (여러 패턴 지원)
            if line.lower().startswith("summary:") or line.startswith("## 요약") or line.startswith("**요약"):
                current_section = "summary"
                summary = re.sub(r'^(summary:|##\s*요약|\\*\\*요약\\*\\*):?', '', line, flags=re.IGNORECASE).strip()
                continue
            
            # strategies 찾기
            if line.lower().startswith("strategies:") or line.startswith("## 전략") or line.startswith("**전략"):
                current_section = "strategies"
                continue
            
            # 전략 항목 찾기 (-, •, 숫자., 이모지로 시작)
            if current_section == "strategies":
                # 패턴: "- ", "• ", "1. ", "🎯 " 등으로 시작
                if re.match(r'^[-•\d\.\)🎯📱💰📊✅🔼🔻⚠️➡️]\s*', line):
                    strategy = re.sub(r'^[-•\d\.\)🎯📱💰📊✅🔼🔻⚠️➡️]\s*', '', line).strip()
                    if strategy:
                        strategies.append(strategy)
            
            # summary 내용 (summary: 다음 줄)
            elif current_section == "summary" and not summary:
                summary = line
        
        # JSON 형식으로 응답한 경우 처리
        if not summary and not strategies:
            try:
                import json
                # ```json ... ``` 블록 제거
                json_content = content
                if '```json' in content:
                    json_content = content.split('```json')[1].split('```')[0].strip()
                elif '```' in content:
                    json_content = content.split('```')[1].split('```')[0].strip()
                
                # JSON으로 파싱 시도
                data = json.loads(json_content)
                summary = data.get('summary', '')
                
                # strategies가 객체 배열인 경우 처리
                raw_strategies = data.get('strategies', [])
                if isinstance(raw_strategies, list):
                    for strat in raw_strategies:
                        if isinstance(strat, dict):
                            # 객체 형식: {"emoji": "🎯", "title": "...", "description": "..."}
                            emoji = strat.get('emoji', '🎯')
                            title = strat.get('title', '')
                            desc = strat.get('description', '')
                            strategies.append(f"{emoji} **{title}**: {desc}")
                        elif isinstance(strat, str):
                            # 문자열 형식
                            strategies.append(strat)
            except Exception as e:
                print(f"   JSON 파싱 실패: {e}")
                pass
        
        # 파싱 실패 시 데이터 기반 전략 사용
        if not summary or not strategies:
            print(f"⚠️  LLM 응답 파싱 실패 - 데이터 기반 전략으로 전환")
            print(f"   파싱 결과: summary={bool(summary)}, strategies={len(strategies)}개")
            if analysis_data:
                return self._get_default_strategy(analysis_data)
            else:
                # 정말 최후의 수단
                return {
                    'summary': "분석 결과를 기반으로 전략을 제안합니다.",
                    'strategies': [
                        "🎯 **차별화 전략**: 경쟁사 대비 독특한 가치를 제공하세요.",
                        "📱 **디지털 마케팅**: 온라인 채널을 통한 고객 유입을 늘리세요.",
                        "💰 **비용 최적화**: 불필요한 지출을 줄이고 효율성을 높이세요.",
                        "📊 **데이터 분석**: 고객 데이터를 활용한 의사결정을 하세요."
                    ]
                }
        
        print(f"✅ 파싱 성공: summary 길이={len(summary)}, strategies={len(strategies)}개")
        return {
            'summary': summary,
            'strategies': strategies
        }
    
    def _get_default_strategy(self, data: Dict) -> Dict:
        """기본 전략 (API 키 없을 때)"""
        store_data = data['store_data']
        diagnosis_results = data.get('diagnosis_results', {})
        risk_level = diagnosis_results.get('total_risk_score', 50)
        
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