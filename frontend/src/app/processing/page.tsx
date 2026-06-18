// src/app/processing/page.tsx
'use client';
import { useEffect, useState, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAppStore, AgentStep } from '@/lib/store';
import { getStatusEventSource } from '@/lib/api';
import AgentTracePanel from '@/components/AgentTracePanel';
import { Badge } from '@/components/ui/Badge';
import { CheckCircle2 } from 'lucide-react';

function ProcessingPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const jobId = searchParams.get('jobId');

  const { addAgentStep, clearAgentSteps } = useAppStore();
  const [currentAgent, setCurrentAgent] = useState('Extraction');
  const [percentComplete, setPercentComplete] = useState(0);
  const [completed, setCompleted] = useState(false);

  useEffect(() => {
    if (!jobId) return;

    clearAgentSteps();
    const eventSource = getStatusEventSource(jobId);

    eventSource.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === 'complete') {
          setCompleted(true);
          setPercentComplete(100);
          eventSource.close();
          // Short delay for wow factor and redirection
          setTimeout(() => {
            router.push(data.redirect);
          }, 1500);
          return;
        }

        // Add agent reasoning trace step to console log
        const step: AgentStep = {
          agent: data.agent,
          step: data.step,
          status: data.status,
          message: data.message,
          reasoning: data.reasoning,
          duration: data.duration
        };
        addAgentStep(step);

        // Map status steps to completion circle percentages
        setCurrentAgent(data.agent);
        if (data.agent === 'extraction' && data.status === 'done') setPercentComplete(25);
        if (data.agent === 'compliance' && data.status === 'done') setPercentComplete(50);
        if (data.agent === 'reconciliation' && data.status === 'done') setPercentComplete(75);
        if (data.agent === 'scoring' && data.status === 'done') setPercentComplete(100);
      } catch (e) {
        console.error("Error parsing status SSE message", e);
      }
    };

    eventSource.onerror = (err) => {
      console.error("SSE connection failure", err);
      eventSource.close();
    };

    return () => eventSource.close();
  }, [jobId]);

  return (
    <div className="grid grid-cols-1 lg:grid-cols-10 gap-8 items-stretch min-h-[60vh] animate-fadeIn">
      {/* Left panel: 40% Agent activity console */}
      <div className="lg:col-span-4 h-full">
        <AgentTracePanel />
      </div>

      {/* Right panel: 60% Visual animations progress ring */}
      <div className="lg:col-span-6 bg-[#1E293B] border border-[#334155] rounded-xl p-8 flex flex-col items-center justify-center text-center space-y-8 shadow-2xl relative overflow-hidden">
        
        {/* Animated document funnel background effect */}
        <div className="absolute top-0 inset-x-0 h-1 bg-gradient-to-r from-emerald-500 to-blue-500 animate-pulse" />

        <div className="space-y-2">
          <span className="text-xs text-[#22C55E] uppercase font-mono tracking-wider font-bold">
            Step 2 of 3
          </span>
          <h2 className="text-2xl font-bold text-[#F1F5F9]">Processing Financials</h2>
          <p className="text-sm text-[#94A3B8] max-w-md">
            Our multi-agent pipeline is extracting details, running audits and reconciling invoices.
          </p>
        </div>

        {/* Circular Progress Gauge */}
        <div className="relative h-48 w-48 flex items-center justify-center">
          <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke="#1e293b"
              strokeWidth="6"
              fill="transparent"
              className="stroke-slate-800"
            />
            <circle
              cx="50"
              cy="50"
              r="40"
              stroke={completed ? "#22C55E" : "#3B82F6"}
              strokeWidth="6"
              fill="transparent"
              strokeDasharray={251.2}
              strokeDashoffset={251.2 - (251.2 * percentComplete) / 100}
              className="transition-all duration-700 ease-out"
            />
          </svg>
          <div className="absolute flex flex-col items-center">
            {completed ? (
              <CheckCircle2 size={40} className="text-[#22C55E] animate-bounce" />
            ) : (
              <>
                <span className="text-3xl font-extrabold text-[#F1F5F9]">{percentComplete}%</span>
                <span className="text-[10px] text-slate-500 uppercase font-mono tracking-wider mt-1">
                  {currentAgent}
                </span>
              </>
            )}
          </div>
        </div>

        {/* 4 Agent Status Chips indicator lights */}
        <div className="flex flex-wrap justify-center gap-3">
          <span className={`px-3 py-1.5 rounded-full text-xs font-mono border ${
            percentComplete >= 25 ? 'bg-emerald-950/40 border-emerald-500/20 text-[#22C55E]' : 'bg-slate-800/40 border-slate-700 text-slate-500'
          }`}>
            Extraction
          </span>
          <span className={`px-3 py-1.5 rounded-full text-xs font-mono border ${
            percentComplete >= 50 ? 'bg-emerald-950/40 border-emerald-500/20 text-[#22C55E]' : 'bg-slate-800/40 border-slate-700 text-slate-500'
          }`}>
            Compliance
          </span>
          <span className={`px-3 py-1.5 rounded-full text-xs font-mono border ${
            percentComplete >= 75 ? 'bg-emerald-950/40 border-emerald-500/20 text-[#22C55E]' : 'bg-slate-800/40 border-slate-700 text-slate-500'
          }`}>
            Reconciliation
          </span>
          <span className={`px-3 py-1.5 rounded-full text-xs font-mono border ${
            percentComplete >= 100 ? 'bg-emerald-950/40 border-emerald-500/20 text-[#22C55E]' : 'bg-slate-800/40 border-slate-700 text-slate-500'
          }`}>
            Scoring
          </span>
        </div>
      </div>
    </div>
  );
}

export default function ProcessingPage() {
  return (
    <Suspense fallback={<div className="text-center py-12 text-slate-400">Loading analysis pipeline...</div>}>
      <ProcessingPageContent />
    </Suspense>
  );
}
