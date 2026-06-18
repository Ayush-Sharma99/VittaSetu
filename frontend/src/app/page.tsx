// src/app/page.tsx
'use client';
import { useRouter } from 'next/navigation';
import { Button } from '@/components/ui/Button';
import { Shield, TrendingUp, FileText, ArrowRight, CheckCircle2, Cpu, Sparkles } from 'lucide-react';
import { useAppStore } from '@/lib/store';

export default function Home() {
  const router = useRouter();
  const setDemoMode = useAppStore((state) => state.setDemoMode);

  const startDemo = () => {
    setDemoMode(true);
    router.push('/upload?demo=true');
  };

  return (
    <div className="relative min-h-[80vh] flex flex-col items-center justify-start space-y-8 pt-0 pb-6 animate-fadeIn">
      {/* Decorative gradient background blobs */}
      <div className="absolute top-1/4 left-1/4 -translate-x-1/2 -translate-y-1/2 h-96 w-96 bg-emerald-500/5 rounded-full filter blur-3xl -z-10 animate-pulse" />
      <div className="absolute bottom-1/3 right-1/4 translate-x-1/2 translate-y-1/2 h-[30rem] w-[30rem] bg-cyan-500/5 rounded-full filter blur-3xl -z-10" />

      {/* Grid Hero Section (Side-by-side on large screens, stacked on small) */}
      <div className="w-full max-w-7xl px-4 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center pt-0">
        
        {/* Left Column: Title & Intro */}
        <div className="lg:col-span-5 space-y-5 text-left flex flex-col justify-center">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-xs font-semibold uppercase tracking-wider w-fit">
            <Sparkles size={12} className="animate-spin" style={{ animationDuration: '4s' }} />
            VittaSetu AI Protocol v1.0
          </div>
          
          <div className="flex items-center gap-3 bg-slate-900/60 border border-[#334155]/60 rounded-xl px-4 py-2.5 w-fit shadow-lg shadow-emerald-500/5 backdrop-blur-sm">
            <img src="/logo.png" alt="VittaSetu Logo" className="h-12 w-auto drop-shadow-[0_0_8px_rgba(34,197,94,0.2)] filter brightness-110" />
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold text-[#F1F5F9] leading-tight tracking-tight">
            Your ledger is your <br />
            <span className="bg-gradient-to-r from-emerald-400 via-teal-300 to-amber-300 bg-clip-text text-transparent">
              loan application.
            </span>
          </h1>
          
          <p className="text-sm sm:text-base text-[#94A3B8] font-medium leading-relaxed">
            AI-powered compliance and credit readiness for India's 63 million MSMEs. Convert raw document streams (GST invoices, bank statements, ledgers) into verified, lender-grade credit passports.
          </p>

          <div className="pt-2 flex flex-col sm:flex-row gap-4">
            <Button onClick={startDemo} size="lg" className="group font-semibold tracking-wide shadow-lg bg-gradient-to-r from-emerald-600 to-teal-500 hover:from-emerald-500 hover:to-teal-400 border-0 text-white px-6 py-5 rounded-xl text-sm transition-all duration-300 transform hover:-translate-y-0.5">
              Launch Interactive Demo 
              <ArrowRight className="ml-2 group-hover:translate-x-1 transition-transform" size={16} />
            </Button>
          </div>
        </div>

        {/* Right Column: Simulated Live Credit Passport Mockup */}
        <div className="lg:col-span-7 w-full">
          <div className="bg-[#1E293B]/70 border border-[#334155]/60 rounded-2xl p-5 md:p-6 shadow-2xl relative overflow-hidden backdrop-blur-md">
            {/* Top Window Bar */}
            <div className="absolute top-0 left-0 right-0 h-8 bg-[#0F172A]/80 border-b border-[#334155]/50 flex items-center px-4 justify-between">
              <div className="flex gap-1.5">
                <span className="w-2.5 h-2.5 rounded-full bg-red-500/60 inline-block"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-yellow-500/60 inline-block"></span>
                <span className="w-2.5 h-2.5 rounded-full bg-emerald-500/60 inline-block"></span>
              </div>
              <div className="text-[10px] text-slate-500 font-mono">vittasetu-credit-passport-live.json</div>
              <div className="w-8"></div>
            </div>

            <div className="mt-4 grid grid-cols-1 md:grid-cols-12 gap-6 pt-2">
              {/* Simulated Passport Info */}
              <div className="md:col-span-6 space-y-4">
                <div>
                  <div className="text-slate-400 text-[10px] font-semibold tracking-wider uppercase">MSME Entity</div>
                  <h3 className="text-lg font-bold text-slate-100 flex items-center gap-1.5 mt-0.5">
                    Sharma Enterprises Pvt Ltd
                    <CheckCircle2 className="text-emerald-400 fill-emerald-950/30" size={16} />
                  </h3>
                  <span className="text-[10px] text-emerald-400 font-mono bg-emerald-950/40 border border-emerald-800/30 px-2 py-0.5 rounded mt-1 inline-block">
                    GSTIN: 27AAAAA1111A1Z1
                  </span>
                </div>

                {/* Large Score Indicator */}
                <div className="flex items-center gap-3.5 p-3 rounded-xl bg-slate-900/60 border border-slate-800/80">
                  <div className="relative flex items-center justify-center w-16 h-16 shrink-0">
                    <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                      <circle cx="50" cy="50" r="40" stroke="#1E293B" strokeWidth="10" fill="transparent" />
                      <circle cx="50" cy="50" r="40" stroke="#10B981" strokeWidth="10" fill="transparent" 
                        strokeDasharray="251.2" strokeDashoffset="45.2" strokeLinecap="round" className="drop-shadow-[0_0_6px_rgba(16,185,129,0.4)]" />
                    </svg>
                    <div className="absolute flex flex-col items-center">
                      <span className="text-lg font-black text-slate-100">82</span>
                    </div>
                  </div>
                  <div>
                    <div className="text-xs font-semibold text-slate-300">Credit Score: Strong</div>
                    <p className="text-[11px] text-slate-400 leading-normal mt-0.5">
                      Healthy GST filings compliance, and 98% bank ledger reconciliation match.
                    </p>
                  </div>
                </div>

                {/* Compliance Badges */}
                <div className="space-y-2.5">
                  <div>
                    <div className="flex justify-between items-center text-[11px] mb-1">
                      <span className="text-slate-400 font-medium">Reconciliation Match</span>
                      <span className="text-emerald-400 font-bold">98.4% Passed</span>
                    </div>
                    <div className="w-full bg-slate-900 rounded-full h-1.5">
                      <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-1.5 rounded-full" style={{ width: '98.4%' }}></div>
                    </div>
                  </div>
                  <div>
                    <div className="flex justify-between items-center text-[11px] mb-1">
                      <span className="text-slate-400 font-medium">GST Rule Compliance</span>
                      <span className="text-emerald-400 font-bold">12/12 Checked</span>
                    </div>
                    <div className="w-full bg-slate-900 rounded-full h-1.5">
                      <div className="bg-gradient-to-r from-emerald-500 to-teal-400 h-1.5 rounded-full" style={{ width: '100%' }}></div>
                    </div>
                  </div>
                </div>
              </div>

              {/* The Pipeline explanation */}
              <div className="md:col-span-6 flex flex-col justify-center space-y-3 border-t md:border-t-0 md:border-l border-slate-800/80 pt-4 md:pt-0 md:pl-4">
                <h4 className="text-xs font-bold text-slate-200 flex items-center gap-1.5 mb-1">
                  <Cpu size={14} className="text-teal-400" />
                  Multi-Agent Consensus Pipeline
                </h4>
                
                <div className="space-y-2 text-[11px]">
                  <div className="flex gap-2 items-start">
                    <span className="w-4 h-4 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-[9px] shrink-0 mt-0.5">1</span>
                    <p className="text-slate-300"><strong className="text-slate-100">Extraction:</strong> Pulls data from raw statements & PDFs.</p>
                  </div>
                  <div className="flex gap-2 items-start">
                    <span className="w-4 h-4 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold text-[9px] shrink-0 mt-0.5">2</span>
                    <p className="text-slate-300"><strong className="text-slate-100">GST RAG:</strong> Audits transactions against tax rules.</p>
                  </div>
                  <div className="flex gap-2 items-start">
                    <span className="w-4 h-4 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-[9px] shrink-0 mt-0.5">3</span>
                    <p className="text-slate-300"><strong className="text-slate-100">Reconcile:</strong> Cross-checks ledgers against bank lines.</p>
                  </div>
                  <div className="flex gap-2 items-start">
                    <span className="w-4 h-4 rounded-full bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-[9px] shrink-0 mt-0.5">4</span>
                    <p className="text-slate-300"><strong className="text-slate-100">Scoring:</strong> Packages findings into lender API formats.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Features Grid */}
      <div className="max-w-7xl w-full px-4 space-y-6 pt-4">
        <div className="text-left space-y-1">
          <h2 className="text-2xl font-extrabold text-slate-100">Designed for Bank Readiness</h2>
          <p className="text-xs text-slate-400">VittaSetu automates the friction points of underwriting to secure credit faster.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {/* Card 1 */}
          <div className="bg-[#1E293B]/40 hover:bg-[#1E293B]/60 transition-all duration-300 border border-[#334155]/50 rounded-xl p-5 space-y-3">
            <div className="p-2 bg-emerald-500/10 text-emerald-400 rounded-lg w-fit">
              <FileText size={20} />
            </div>
            <h3 className="text-lg font-bold text-[#F1F5F9]">Multi-Agent Ledger Sync</h3>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Our background workflow orchestrates five distinct AI agents specializing in extraction, validation, matching, rule checking, and scoring.
            </p>
          </div>

          {/* Card 2 */}
          <div className="bg-[#1E293B]/40 hover:bg-[#1E293B]/60 transition-all duration-300 border border-[#334155]/50 rounded-xl p-5 space-y-3">
            <div className="p-2 bg-cyan-500/10 text-cyan-400 rounded-lg w-fit">
              <Shield size={20} />
            </div>
            <h3 className="text-lg font-bold text-[#F1F5F9]">GST Audit & RAG</h3>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Verify legal compliance and tax audit alignment on-the-fly. Checks details against a vector store of GST rules and tax legislation.
            </p>
          </div>

          {/* Card 3 */}
          <div className="bg-[#1E293B]/40 hover:bg-[#1E293B]/60 transition-all duration-300 border border-[#334155]/50 rounded-xl p-5 space-y-3">
            <div className="p-2 bg-amber-500/10 text-amber-400 rounded-lg w-fit">
              <TrendingUp size={20} />
            </div>
            <h3 className="text-lg font-bold text-[#F1F5F9]">Explainable Grading</h3>
            <p className="text-xs text-[#94A3B8] leading-relaxed">
              Get an instantly readable credit grade (0-100) detailing transaction health, audit results, and highlighting reconciliation recommendations.
            </p>
          </div>
        </div>
      </div>

      {/* Trust Banner/Stats */}
      <div className="w-full max-w-7xl px-4 text-center">
        <div className="border-t border-[#334155]/40 pt-8 grid grid-cols-2 md:grid-cols-4 gap-4">
          <div>
            <div className="text-2xl font-black text-emerald-400">63 Million</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold mt-0.5">Indian MSMEs</div>
          </div>
          <div>
            <div className="text-2xl font-black text-teal-400">₹30 Lakh Cr</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold mt-0.5">Credit Gap</div>
          </div>
          <div>
            <div className="text-2xl font-black text-amber-400">5-Agent</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold mt-0.5">Consensus AI</div>
          </div>
          <div>
            <div className="text-2xl font-black text-indigo-400">Real-Time</div>
            <div className="text-[10px] text-slate-500 uppercase font-semibold mt-0.5">GST Audit</div>
          </div>
        </div>
      </div>
    </div>
  );
}
