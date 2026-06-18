// src/app/dashboard/page.tsx
'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAppStore, CreditPassport as CreditPassportType } from '@/lib/store';
import { getCreditPassport } from '@/lib/api';
import CreditPassport from '@/components/CreditPassport';
import ComplianceStatus from '@/components/ComplianceStatus';
import ReconciliationTable from '@/components/ReconciliationTable';
import { Button } from '@/components/ui/Button';
import { Spinner } from '@/components/ui/Spinner';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Sparkles, MessageCircle, FileText, ArrowRight, CheckCircle2 } from 'lucide-react';

export default function DashboardPage() {
  const router = useRouter();
  const { businessId, creditPassport, setCreditPassport } = useAppStore();
  const [activeTab, setActiveTab] = useState<'overview' | 'compliance' | 'invoices' | 'transactions'>('overview');
  const [loading, setLoading] = useState(false);
  const [showULIModal, setShowULIModal] = useState(false);
  const [connectingLenders, setConnectingLenders] = useState(false);
  const [connectionSuccess, setConnectionSuccess] = useState(false);

  // Fallback structures if database fields are empty during direct navigation checks
  const [invoices, setInvoices] = useState<any[]>([]);
  const [transactions, setTransactions] = useState<any[]>([]);

  useEffect(() => {
    // If user lands directly on dashboard without starting upload, redirect to upload demo
    if (!businessId) {
      router.push('/upload?demo=true');
      return;
    }

    setLoading(true);
    getCreditPassport(businessId)
      .then((data) => {
        setCreditPassport(data);
        
        // Fetch raw lists for child tabs from endpoints or mock
        // Since we are showing invoices and transactions, retrieve from business context
        const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';
        
        fetch(`${API_BASE_URL}/api/reconciliation/${businessId}`)
          .then(res => res.json())
          .then(invs => setInvoices(invs))
          .catch(() => {
            // High quality fallback mocks matching seed data for Ravi Kumar
            setInvoices([
              { id: '1', invoice_number: 'RKT/2026/001', invoice_date: '2026-01-05', vendor_or_customer: 'Mehta Fabrics', amount: 185000, gst_amount: 33300, gst_rate: 18, reconciled: true },
              { id: '2', invoice_number: 'RKT/2026/002', invoice_date: '2026-01-10', vendor_or_customer: 'Yarn Supplier Ahmedabad', amount: 120000, gst_amount: 21600, reconciled: true },
              { id: '22', invoice_number: 'RKT/2026/022', invoice_date: '2026-03-20', vendor_or_customer: 'Patel Garments', amount: 95000, gst_amount: 17100, reconciled: false },
              { id: '23', invoice_number: 'RKT/2026/023', invoice_date: '2026-03-22', vendor_or_customer: 'Raj Fabrics', amount: 45000, gst_amount: 8100, reconciled: false },
              { id: '24', invoice_number: 'RKT/2026/024', invoice_date: '2026-03-24', vendor_or_customer: 'Karan Suits', amount: 65000, gst_amount: 11700, reconciled: false },
            ]);
          });

        fetch(`${API_BASE_URL}/api/compliance/${businessId}`)
          .then(res => res.json())
          .catch(() => {});
      })
      .catch((e) => {
        console.error(e);
      })
      .finally(() => setLoading(false));
  }, [businessId]);

  const triggerULIConnect = () => {
    setShowULIModal(true);
    setConnectingLenders(true);
    setConnectionSuccess(false);

    // Simulate connecting to ULI network
    setTimeout(() => {
      setConnectingLenders(false);
      setConnectionSuccess(true);
    }, 2500);
  };

  if (loading || !creditPassport) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[50vh] space-y-4">
        <Spinner className="h-10 w-10" />
        <p className="text-sm text-slate-500 font-mono">Retrieving credit registry passport...</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start animate-fadeIn relative">
      
      {/* Tab Navigation & Business Overview Sidebar */}
      <div className="lg:col-span-4 space-y-6 lg:sticky lg:top-24">
        <Card>
          <CardContent className="p-6 space-y-6">
            <div className="flex items-center gap-3">
              <div className="h-12 w-12 rounded-xl bg-gradient-to-tr from-emerald-500 to-emerald-950 flex items-center justify-center text-lg font-bold text-slate-100 border border-emerald-500/20">
                RK
              </div>
              <div>
                <h3 className="font-bold text-[#F1F5F9] text-base">Ravi Kumar Textiles</h3>
                <span className="text-xs text-[#94A3B8] font-mono">GSTIN: {creditPassport.compliance_flags[0]?.gstin || '27AABCU9603R1ZM'}</span>
              </div>
            </div>

            <div className="border-t border-[#334155] pt-6 flex flex-col gap-2">
              <button
                onClick={() => setActiveTab('overview')}
                className={`w-full text-left px-4 py-2.5 rounded-lg text-sm transition-colors font-semibold flex items-center justify-between ${
                  activeTab === 'overview' ? 'bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E]' : 'text-[#94A3B8] hover:text-[#F1F5F9] hover:bg-slate-800/40'
                }`}
              >
                <span>Overview & Score</span>
                <Sparkles size={14} />
              </button>

              <button
                onClick={() => setActiveTab('compliance')}
                className={`w-full text-left px-4 py-2.5 rounded-lg text-sm transition-colors font-semibold flex items-center justify-between ${
                  activeTab === 'compliance' ? 'bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E]' : 'text-[#94A3B8] hover:text-[#F1F5F9] hover:bg-slate-800/40'
                }`}
              >
                <span>Compliance Flags</span>
                <span className="bg-amber-950/60 border border-amber-500/20 text-[#F59E0B] px-2 py-0.5 rounded text-xs">
                  {creditPassport.compliance_flags.length}
                </span>
              </button>

              <button
                onClick={() => setActiveTab('invoices')}
                className={`w-full text-left px-4 py-2.5 rounded-lg text-sm transition-colors font-semibold flex items-center justify-between ${
                  activeTab === 'invoices' ? 'bg-[#22C55E]/10 border border-[#22C55E]/20 text-[#22C55E]' : 'text-[#94A3B8] hover:text-[#F1F5F9] hover:bg-slate-800/40'
                }`}
              >
                <span>Invoice Matching</span>
                <span className="bg-slate-800 border border-[#334155] text-slate-300 px-2 py-0.5 rounded text-xs">
                  24 total
                </span>
              </button>
            </div>

            <div className="border-t border-[#334155] pt-6 flex flex-col gap-3">
              <Button onClick={() => router.push('/chat')} className="w-full justify-center">
                <MessageCircle size={16} className="mr-2" />
                Ask Advisor
              </Button>

              <Button onClick={triggerULIConnect} variant="secondary" className="w-full justify-center bg-emerald-950/20 border border-emerald-500/20 text-[#22C55E] hover:bg-[#22C55E] hover:text-slate-900">
                Apply for Credit via ULI
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Main content Tab panel layout */}
      <div className="lg:col-span-8 space-y-6">
        {activeTab === 'overview' && (
          <div className="space-y-6 animate-fadeIn">
            {/* KPI metrics cards grid */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <Card>
                <CardContent className="p-4 flex flex-col space-y-1">
                  <span className="text-xs text-[#94A3B8] font-medium">Filing Rate</span>
                  <span className="text-xl font-extrabold text-[#F1F5F9]">92%</span>
                  <span className="text-[10px] text-[#22C55E] font-medium">&uarr; Stable</span>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4 flex flex-col space-y-1">
                  <span className="text-xs text-[#94A3B8] font-medium">Reconciled</span>
                  <span className="text-xl font-extrabold text-[#F1F5F9]">87.5%</span>
                  <span className="text-[10px] text-slate-500">21 / 24 match</span>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4 flex flex-col space-y-1">
                  <span className="text-xs text-[#94A3B8] font-medium">Flags</span>
                  <span className="text-xl font-extrabold text-[#F59E0B]">2 Warning</span>
                  <span className="text-[10px] text-slate-500">0 Critical</span>
                </CardContent>
              </Card>

              <Card>
                <CardContent className="p-4 flex flex-col space-y-1">
                  <span className="text-xs text-[#94A3B8] font-medium">Monthly Rev</span>
                  <span className="text-xl font-extrabold text-[#F1F5F9]">₹18.4L</span>
                  <span className="text-[10px] text-[#22C55E] font-medium">&uarr; +4.2%</span>
                </CardContent>
              </Card>
            </div>

            <CreditPassport
              score={creditPassport.score}
              grade={creditPassport.grade}
              factorBreakdown={creditPassport.factor_breakdown}
              explanation={creditPassport.explanation}
              topStrength={creditPassport.top_strength}
              topAction={creditPassport.top_action}
            />
          </div>
        )}

        {activeTab === 'compliance' && (
          <div className="space-y-4 animate-fadeIn">
            <h2 className="text-xl font-bold text-[#F1F5F9]">Compliance Flags & Audits</h2>
            <ComplianceStatus flags={creditPassport.compliance_flags} />
          </div>
        )}

        {activeTab === 'invoices' && (
          <div className="space-y-4 animate-fadeIn">
            <h2 className="text-xl font-bold text-[#F1F5F9]">Invoice reconciliation ledger</h2>
            <ReconciliationTable invoices={invoices} />
          </div>
        )}
      </div>

      {/* ULI Connect simulation modal */}
      {showULIModal && (
        <div className="fixed inset-0 bg-slate-950/80 backdrop-blur-sm z-50 flex items-center justify-center p-4">
          <Card className="max-w-md w-full border-[#334155] shadow-2xl animate-scaleIn">
            <CardHeader>
              <CardTitle>Unified Lending Interface (ULI) Connection</CardTitle>
            </CardHeader>
            <CardContent className="p-6 space-y-6 text-center">
              {connectingLenders ? (
                <div className="flex flex-col items-center space-y-4">
                  <Spinner className="h-12 w-12 text-[#22C55E]" />
                  <p className="text-sm text-[#94A3B8] font-mono">
                    Searching participating NBFCs & public sector banks...
                  </p>
                </div>
              ) : (
                <div className="space-y-4">
                  <div className="flex justify-center">
                    <CheckCircle2 className="text-[#22C55E]" size={48} />
                  </div>
                  <h3 className="text-lg font-bold text-[#F1F5F9]">Direct Lending Match Found</h3>
                  <p className="text-xs text-[#94A3B8] leading-relaxed">
                    Based on your 71/100 Credit Readiness Passport, SBI, HDFC and Union Bank of India have matched your textile wholesale profile for loans up to ₹15,00,000.
                  </p>
                  <div className="pt-4 flex gap-2">
                    <Button onClick={() => setShowULIModal(false)} variant="secondary" className="flex-1 text-xs justify-center">
                      Close
                    </Button>
                    <Button onClick={() => { setShowULIModal(false); router.push('/chat'); }} className="flex-1 text-xs justify-center font-bold">
                      Chat with Advisor
                    </Button>
                  </div>
                </div>
              )}
            </CardContent>
          </Card>
        </div>
      )}
    </div>
  );
}
// Define inline scale animation if needed
const scaleInStyle = `
  @keyframes scaleIn {
    from { transform: scale(0.95); opacity: 0; }
    to { transform: scale(1); opacity: 1; }
  }
  .animate-scaleIn {
    animation: scaleIn 0.2s ease-out forwards;
  }
`;
if (typeof document !== 'undefined') {
  const style = document.createElement('style');
  style.appendChild(document.createTextNode(scaleInStyle));
  document.head.appendChild(style);
}
