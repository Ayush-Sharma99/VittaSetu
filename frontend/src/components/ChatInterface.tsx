// src/components/ChatInterface.tsx
'use client';
import { useState, useRef, useEffect } from 'react';
import { useAppStore } from '@/lib/store';
import { sendChatMessage } from '@/lib/api';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Send, Bot, User, Sparkles } from 'lucide-react';

interface Message {
  sender: 'user' | 'ai' | 'system';
  text: string;
  tools?: string[];
}

export default function ChatInterface() {
  const businessId = useAppStore((state) => state.businessId);
  const [messages, setMessages] = useState<Message[]>([
    { sender: 'system', text: 'Connected to your financial data.' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [lang, setLang] = useState<'EN' | 'HI'>('EN');

  const bottomRef = useRef<HTMLDivElement>(null);

  const starterPrompts = [
    "Why is my score lower this month?",
    "What compliance issues should I fix first?",
    "How do I reconcile my pending invoices?",
    "When is my next GST filing deadline?"
  ];

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (textToSend: string) => {
    if (!textToSend.trim() || !businessId) return;
    
    // Add user message
    setMessages(prev => [...prev, { sender: 'user', text: textToSend }]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await sendChatMessage(businessId, textToSend);
      setMessages(prev => [...prev, {
        sender: 'ai',
        text: response.reply,
        tools: response.tool_calls_made
      }]);
    } catch (e) {
      setMessages(prev => [...prev, { sender: 'system', text: 'Failed to retrieve response from AI advisor.' }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="flex flex-col h-[550px] border-[#334155]">
      <CardHeader className="flex flex-row items-center justify-between py-4">
        <div className="flex items-center gap-2">
          <Bot className="text-[#22C55E]" size={20} />
          <CardTitle className="text-sm sm:text-base">VittaSetu AI · Financial Advisor</CardTitle>
        </div>
        
        {/* Language selector toggle */}
        <button
          onClick={() => setLang(prev => prev === 'EN' ? 'HI' : 'EN')}
          className="text-xs font-mono px-2.5 py-1 rounded bg-slate-800 border border-[#334155] text-[#94A3B8] hover:text-[#F1F5F9] transition-colors"
        >
          LANG: {lang}
        </button>
      </CardHeader>

      {/* Messages layout pane */}
      <CardContent className="flex-1 overflow-y-auto p-4 space-y-4 max-h-[400px]">
        {messages.map((msg, idx) => (
          <div
            key={idx}
            className={`flex items-start gap-2.5 ${
              msg.sender === 'user' ? 'justify-end' : msg.sender === 'system' ? 'justify-center' : 'justify-start'
            }`}
          >
            {msg.sender === 'ai' && (
              <div className="h-8 w-8 rounded-full bg-emerald-950 flex items-center justify-center border border-emerald-500/30">
                <Bot size={15} className="text-[#22C55E]" />
              </div>
            )}

            <div
              className={`p-3.5 rounded-2xl max-w-[80%] text-sm leading-relaxed ${
                msg.sender === 'user'
                  ? 'bg-[#1E3A8A] text-[#F1F5F9] rounded-tr-none'
                  : msg.sender === 'system'
                  ? 'text-[#64748B] italic text-xs'
                  : 'bg-emerald-950/40 border border-emerald-500/20 text-[#F1F5F9] rounded-tl-none'
              }`}
            >
              {msg.text}
              
              {/* Tool Calls Trace overlay */}
              {msg.tools && msg.tools.length > 0 && (
                <div className="mt-2.5 pt-2 border-t border-emerald-500/10 flex flex-wrap gap-1.5 items-center">
                  <span className="text-[10px] text-slate-400 font-mono flex items-center gap-1">
                    <Sparkles size={10} />
                    called:
                  </span>
                  {msg.tools.map(tool => (
                    <span key={tool} className="text-[9px] font-mono bg-emerald-900/60 border border-emerald-500/20 px-1.5 py-0.5 rounded text-slate-300">
                      {tool}()
                    </span>
                  ))}
                </div>
              )}
            </div>

            {msg.sender === 'user' && (
              <div className="h-8 w-8 rounded-full bg-blue-950 flex items-center justify-center border border-blue-500/30">
                <User size={15} className="text-[#3B82F6]" />
              </div>
            )}
          </div>
        ))}
        
        {isLoading && (
          <div className="flex items-start gap-2.5">
            <div className="h-8 w-8 rounded-full bg-emerald-950 flex items-center justify-center border border-emerald-500/30">
              <Bot size={15} className="text-[#22C55E]" />
            </div>
            <div className="bg-emerald-950/40 border border-emerald-500/20 p-3.5 rounded-2xl rounded-tl-none flex items-center gap-1">
              <div className="h-2 w-2 bg-[#22C55E] rounded-full animate-bounce" style={{ animationDelay: '0ms' }} />
              <div className="h-2 w-2 bg-[#22C55E] rounded-full animate-bounce" style={{ animationDelay: '150ms' }} />
              <div className="h-2 w-2 bg-[#22C55E] rounded-full animate-bounce" style={{ animationDelay: '300ms' }} />
            </div>
          </div>
        )}
        <div ref={bottomRef} />
      </CardContent>

      {/* Suggested Starter prompts chips (only displayed on load) */}
      {messages.length === 1 && (
        <div className="px-4 py-2 border-t border-[#334155] bg-slate-900/20 flex flex-wrap gap-2">
          {starterPrompts.map(prompt => (
            <button
              key={prompt}
              onClick={() => handleSend(prompt)}
              className="text-xs text-left bg-slate-800 border border-[#334155] px-3 py-1.5 rounded-lg text-[#94A3B8] hover:text-[#F1F5F9] hover:bg-slate-700/60 transition-colors"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input area footer */}
      <div className="p-3 bg-slate-900/80 border-t border-[#334155] flex items-center gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === 'Enter' && handleSend(input)}
          placeholder={lang === 'EN' ? "Ask VittaSetu AI about your financials..." : "वित्तीय सलाह के लिए पूछें..."}
          className="flex-1 bg-slate-800 border border-[#334155] rounded-lg px-4 py-2 text-sm text-[#F1F5F9] placeholder-slate-500 focus:outline-none focus:border-[#22C55E] transition-colors"
          disabled={isLoading}
        />
        <Button onClick={() => handleSend(input)} disabled={isLoading} className="p-2 h-9 w-9 rounded-lg">
          <Send size={15} />
        </Button>
      </div>
    </Card>
  );
}
