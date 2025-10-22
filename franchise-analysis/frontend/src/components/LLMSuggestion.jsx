import React, { useState } from 'react';
import { Sparkles, ChevronDown, ChevronUp, Copy, Check } from 'lucide-react';

const LLMSuggestion = ({ suggestion }) => {
  const [expandedIndex, setExpandedIndex] = useState(null);
  const [copied, setCopied] = useState(false);

  // 전체 텍스트 복사
  const handleCopy = () => {
    const fullText = `${suggestion.summary}\n\n전략:\n${suggestion.strategies.join('\n')}`;
    navigator.clipboard.writeText(fullText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  // 전략 확장/축소
  const toggleStrategy = (index) => {
    setExpandedIndex(expandedIndex === index ? null : index);
  };

  return (
    <div className="bg-gradient-to-r from-indigo-500 to-purple-600 rounded-xl shadow-lg p-6 text-white hover:shadow-2xl transition-all duration-300 hover:-translate-y-1">
      {/* 헤더 */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center gap-2">
          <Sparkles size={28} className="animate-pulse" />
          <h2 className="text-2xl font-bold">AI 생존 전략 제안</h2>
        </div>
        <button
          onClick={handleCopy}
          className="flex items-center gap-2 px-4 py-2 bg-white/20 hover:bg-white/30 rounded-lg transition"
        >
          {copied ? (
            <>
              <Check size={16} />
              <span className="text-sm">복사됨!</span>
            </>
          ) : (
            <>
              <Copy size={16} />
              <span className="text-sm">복사</span>
            </>
          )}
        </button>
      </div>

      {/* 요약 */}
      <div className="bg-white/10 backdrop-blur rounded-lg p-4 mb-4 border border-white/20">
        <p className="text-lg leading-relaxed">{suggestion.summary}</p>
      </div>

      {/* 전략 목록 */}
      <div className="space-y-3">
        <h3 className="text-lg font-semibold mb-2">💡 실행 가능한 전략</h3>
        {suggestion.strategies.map((strategy, idx) => {
          // 전략 파싱 (이모지와 타이틀 분리)
          const emojiMatch = strategy.match(/^([^\s]+)\s/);
          const emoji = emojiMatch ? emojiMatch[1] : '•';
          const content = strategy.replace(/^[^\s]+\s/, '');
          
          // 타이틀과 설명 분리 (**: 기준)
          const parts = content.split(':');
          const title = parts[0].replace(/\*\*/g, '').trim();
          const description = parts.slice(1).join(':').trim();

          return (
            <div
              key={idx}
              className="bg-white/10 backdrop-blur rounded-lg border border-white/20 overflow-hidden transition hover:bg-white/15"
            >
              <button
                onClick={() => toggleStrategy(idx)}
                className="w-full p-4 flex items-start justify-between text-left"
              >
                <div className="flex items-start gap-3 flex-1">
                  <span className="text-2xl">{emoji}</span>
                  <div className="flex-1">
                    <p className="font-bold text-lg">{title}</p>
                    {expandedIndex !== idx && description && (
                      <p className="text-sm text-white/70 mt-1 line-clamp-1">
                        {description}
                      </p>
                    )}
                  </div>
                </div>
                {description && (
                  <div className="ml-2">
                    {expandedIndex === idx ? (
                      <ChevronUp size={20} />
                    ) : (
                      <ChevronDown size={20} />
                    )}
                  </div>
                )}
              </button>

              {/* 확장된 내용 */}
              {expandedIndex === idx && description && (
                <div className="px-4 pb-4 animate-fade-in">
                  <div className="pl-11 pr-8">
                    <p className="text-sm leading-relaxed text-white/90">
                      {description}
                    </p>
                  </div>
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* 하단 안내 */}
      <div className="mt-6 pt-4 border-t border-white/20">
        <p className="text-sm text-white/70 text-center">
          💬 이 제안은 AI가 데이터 분석을 통해 생성한 것입니다. 실제 적용 시 전문가와 상담하세요.
        </p>
      </div>
    </div>
  );
};

export default LLMSuggestion;