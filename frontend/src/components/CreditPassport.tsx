// src/components/CreditPassport.tsx
'use client';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';
import { Check, ShieldCheck, Zap } from 'lucide-react';

interface CreditPassportProps {
  score: number;
  grade: string;
  factorBreakdown: {
    filing_compliance: number;
    filing_timeliness: number;
    invoice_reconciliation: number;
    revenue_trend: number;
    cash_flow_consistency: number;
    compliance_health: number;
  };
  explanation: string;
  topStrength: string;
  topAction: string;
}

export default function CreditPassport({
  score,
  grade,
  factorBreakdown,
  explanation,
  topStrength,
  topAction
}: CreditPassportProps) {
  // Determine score color matching parameters (green >= 70, amber 50-69, red < 50)
  const getScoreColorClass = (val: number) => {
    if (val >= 70) return 'text-[#22C55E]';
    if (val >= 50) return 'text-[#F59E0B]';
    return 'text-[#EF4444]';
  };

  const getScoreBgClass = (val: number) => {
    if (val >= 70) return 'border-[#22C55E]/30 bg-[#22C55E]/10';
    if (val >= 50) return 'border-[#F59E0B]/30 bg-[#F59E0B]/10';
    return 'border-[#EF4444]/30 bg-[#EF4444]/10';
  };

  const factorNames = {
    filing_compliance: 'Filing Compliance (20 pts)',
    filing_timeliness: 'Filing Timeliness (15 pts)',
    invoice_reconciliation: 'Invoice Reconciliation (20 pts)',
    revenue_trend: 'Revenue Trend (15 pts)',
    cash_flow_consistency: 'Cash Flow Consistency (15 pts)',
    compliance_health: 'Compliance Health (15 pts)'
  };

  const maxPoints = {
    filing_compliance: 20,
    filing_timeliness: 15,
    invoice_reconciliation: 20,
    revenue_trend: 15,
    cash_flow_consistency: 15,
    compliance_health: 15
  };

  return (
    <div className="space-y-6">
      {/* Visual circular gauge and grade display card */}
      <Card className="overflow-hidden">
        <CardContent className="p-8 flex flex-col md:flex-row items-center justify-between gap-8">
          <div className="flex flex-col items-center space-y-4">
            {/* Simple SVG Circular Score Indicator */}
            <div className="relative h-40 w-40 flex items-center justify-center">
              <svg className="w-full h-full transform -rotate-90" viewBox="0 0 100 100">
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke="#334155"
                  strokeWidth="8"
                  fill="transparent"
                />
                <circle
                  cx="50"
                  cy="50"
                  r="42"
                  stroke={score >= 70 ? "#22C55E" : score >= 50 ? "#F59E0B" : "#EF4444"}
                  strokeWidth="8"
                  fill="transparent"
                  strokeDasharray={263.89}
                  strokeDashoffset={263.89 - (263.89 * score) / 100}
                  className="transition-all duration-1000 ease-out"
                />
              </svg>
              <div className="absolute flex flex-col items-center justify-center">
                <span className="text-4xl font-extrabold text-[#F1F5F9]">{Math.round(score)}</span>
                <span className="text-xs text-[#94A3B8] font-mono">/ 100</span>
              </div>
            </div>
            
            <div className="text-center">
              <div className="flex items-center justify-center gap-2">
                <Badge variant={score >= 70 ? 'success' : score >= 50 ? 'warning' : 'danger'} className="text-sm px-3 py-1 font-bold">
                  Grade: {grade}
                </Badge>
              </div>
            </div>
          </div>

          <div className="flex-1 space-y-4">
            <h2 className="text-2xl font-bold tracking-tight text-[#F1F5F9]">Credit-Readiness Score</h2>
            <div className={`p-4 rounded-xl border ${getScoreBgClass(score)}`}>
              <p className="text-sm leading-relaxed text-[#F1F5F9]">
                {explanation}
              </p>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div className="bg-slate-800/50 p-3 rounded-lg border border-[#334155] flex items-start gap-2.5">
                <ShieldCheck className="text-[#22C55E] shrink-0 mt-0.5" size={18} />
                <div>
                  <span className="text-xs text-[#94A3B8] block">Top Strength</span>
                  <span className="text-sm font-semibold text-[#F1F5F9]">{topStrength}</span>
                </div>
              </div>

              <div className="bg-slate-800/50 p-3 rounded-lg border border-[#334155] flex items-start gap-2.5">
                <Zap className="text-[#F59E0B] shrink-0 mt-0.5" size={18} />
                <div>
                  <span className="text-xs text-[#94A3B8] block">Top Action Needed</span>
                  <span className="text-sm font-semibold text-[#F1F5F9]">{topAction}</span>
                </div>
              </div>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Credit Score Factor Breakdown Horizontal Bar Chart */}
      <Card>
        <CardHeader>
          <CardTitle>Credit Factor Breakdown</CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          {Object.entries(factorBreakdown).map(([factor, points]) => {
            const maxVal = maxPoints[factor as keyof typeof maxPoints] || 20;
            const percentage = (points / maxVal) * 100;
            
            return (
              <div key={factor} className="space-y-1">
                <div className="flex justify-between text-xs sm:text-sm font-medium">
                  <span className="text-[#94A3B8]">{factorNames[factor as keyof typeof factorNames]}</span>
                  <span className="text-[#F1F5F9] font-bold">{points} / {maxVal}</span>
                </div>
                <div className="w-full bg-slate-800 rounded-full h-2.5 border border-[#334155] overflow-hidden">
                  <div
                    className="bg-[#22C55E] h-2.5 rounded-full transition-all duration-700"
                    style={{ width: `${percentage}%` }}
                  />
                </div>
              </div>
            );
          })}
        </CardContent>
      </Card>
    </div>
  );
}
