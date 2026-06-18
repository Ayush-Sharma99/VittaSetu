// src/app/chat/page.tsx
'use client';
import ChatInterface from '@/components/ChatInterface';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { useAppStore } from '@/lib/store';

export default function ChatPage() {
  const router = useRouter();
  const creditPassport = useAppStore((state) => state.creditPassport);

  return (
    <div className="space-y-6 max-w-4xl mx-auto animate-fadeIn">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-3xl font-bold text-[#F1F5F9]">AI Credit Advisor</h1>
          <p className="text-sm text-[#94A3B8]">
            Conversational assistant helping you decode compliance regulations, audit history, and scores.
          </p>
        </div>
        
        <Button variant="secondary" onClick={() => router.push('/dashboard')} size="sm" className="self-start">
          <ArrowLeft size={16} className="mr-2" />
          Back to Dashboard
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 items-stretch">
        <div className="md:col-span-1 bg-[#1E293B] border border-[#334155] rounded-xl p-5 flex flex-col justify-between">
          <div className="space-y-4">
            <h3 className="text-xs font-mono uppercase tracking-wider text-slate-400 font-bold">Passport Status</h3>
            {creditPassport ? (
              <div className="space-y-2">
                <div className="text-3xl font-extrabold text-[#F1F5F9]">{creditPassport.score}</div>
                <div className="text-xs text-[#22C55E] bg-emerald-950/40 border border-emerald-500/20 px-2 py-0.5 rounded font-mono inline-block">
                  Grade: {creditPassport.grade}
                </div>
              </div>
            ) : (
              <div className="text-sm text-slate-500 italic">No score computed yet.</div>
            )}
            
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Ask about your late GSTR-3B filings, how to reconcile outstanding invoices, or how to reach an A+ credit grade.
            </p>
          </div>

          <div className="border-t border-[#334155] pt-4 mt-6">
            <Button onClick={() => window.open('https://www.indiastack.org/uli.html', '_blank')} className="w-full text-xs font-semibold justify-center">
              Learn about ULI
              <ArrowRight size={12} className="ml-1" />
            </Button>
          </div>
        </div>

        <div className="md:col-span-3">
          <ChatInterface />
        </div>
      </div>
    </div>
  );
}
