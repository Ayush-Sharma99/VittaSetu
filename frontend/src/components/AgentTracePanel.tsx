// src/components/AgentTracePanel.tsx
'use client';
import { useAppStore } from '@/lib/store';
import { Badge } from '@/components/ui/Badge';
import { Spinner } from '@/components/ui/Spinner';
import { Terminal, CheckCircle2, AlertCircle, Play } from 'lucide-react';

export default function AgentTracePanel() {
  const agentSteps = useAppStore((state) => state.agentSteps);

  const getAgentEmoji = (agent: string) => {
    switch (agent.toLowerCase()) {
      case 'extraction': return '⚡';
      case 'compliance': return '⚖️';
      case 'reconciliation': return '🔍';
      case 'scoring': return '📊';
      default: return '🤖';
    }
  };

  return (
    <div className="bg-slate-900 border border-[#334155] rounded-xl p-6 shadow-2xl h-full flex flex-col font-mono">
      <div className="flex items-center gap-2 mb-6 border-b border-[#334155] pb-4">
        <Terminal className="text-[#22C55E]" size={20} />
        <h2 className="text-[#F1F5F9] font-semibold text-base">AI Agent Activity</h2>
      </div>

      <div className="flex-1 overflow-y-auto space-y-4 pr-2 max-h-[500px]">
        {agentSteps.length === 0 ? (
          <div className="text-slate-500 flex items-center justify-center h-40 italic text-sm">
            Awaiting process initiation...
          </div>
        ) : (
          agentSteps.map((step, idx) => (
            <div
              key={`${step.agent}-${step.status}-${idx}`}
              className="border-l-2 border-slate-700 pl-4 py-1 animate-fadeIn flex flex-col space-y-1.5"
            >
              <div className="flex items-center justify-between text-xs sm:text-sm">
                <div className="flex items-center gap-2">
                  <span className="text-base">{getAgentEmoji(step.agent)}</span>
                  <span className="text-[#22C55E] capitalize font-bold">{step.agent} Agent</span>
                  <span className="text-slate-500">[step {step.step}]</span>
                </div>
                
                {step.status === 'running' ? (
                  <div className="flex items-center gap-1.5 text-sky-400">
                    <Spinner className="h-3 w-3 border-sky-400" />
                    <span>running</span>
                  </div>
                ) : step.status === 'done' ? (
                  <div className="flex items-center gap-1 text-emerald-400 font-bold">
                    <CheckCircle2 size={13} />
                    <span>done</span>
                  </div>
                ) : (
                  <div className="flex items-center gap-1 text-rose-500">
                    <AlertCircle size={13} />
                    <span>error</span>
                  </div>
                )}
              </div>

              <p className="text-[#F1F5F9] text-xs leading-relaxed pl-6">
                {step.message}
              </p>

              {step.duration && step.duration !== '0' && (
                <span className="text-[10px] text-slate-500 pl-6">
                  Duration: {parseFloat(step.duration) / 1000}s
                </span>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}
