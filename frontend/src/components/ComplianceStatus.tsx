// src/components/ComplianceStatus.tsx
'use client';
import { useState } from 'react';
import { Card, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { ChevronDown, ChevronUp, AlertTriangle, AlertCircle, Info } from 'lucide-react';

interface ComplianceFlag {
  flag_type: string;
  severity: 'critical' | 'warning' | 'info';
  description: string;
  rule_reference: string;
  rag_source_chunk: string;
  detected_at: string;
}

export default function ComplianceStatus({ flags }: { flags: ComplianceFlag[] }) {
  const [expandedRow, setExpandedRow] = useState<number | null>(null);
  const [filter, setFilter] = useState<'all' | 'critical' | 'warning' | 'info'>('all');

  const toggleRow = (idx: number) => {
    setExpandedRow(expandedRow === idx ? null : idx);
  };

  const filteredFlags = flags.filter(flag => {
    if (filter === 'all') return true;
    return flag.severity === filter;
  });

  const getSeverityIcon = (sev: string) => {
    switch (sev) {
      case 'critical': return <AlertCircle className="text-[#EF4444]" size={16} />;
      case 'warning': return <AlertTriangle className="text-[#F59E0B]" size={16} />;
      default: return <Info className="text-[#3B82F6]" size={16} />;
    }
  };

  return (
    <div className="space-y-4">
      {/* Filtering triggers */}
      <div className="flex items-center gap-2">
        <span className="text-xs text-[#94A3B8] font-semibold">Filter:</span>
        <button
          onClick={() => setFilter('all')}
          className={`px-3 py-1 rounded-full text-xs transition-colors font-medium border ${
            filter === 'all'
              ? 'bg-[#22C55E]/10 border-[#22C55E]/30 text-[#22C55E]'
              : 'border-[#334155] text-[#94A3B8] hover:text-[#F1F5F9]'
          }`}
        >
          All ({flags.length})
        </button>
        <button
          onClick={() => setFilter('critical')}
          className={`px-3 py-1 rounded-full text-xs transition-colors font-medium border ${
            filter === 'critical'
              ? 'bg-red-950/40 border-red-500/30 text-[#EF4444]'
              : 'border-[#334155] text-[#94A3B8] hover:text-[#F1F5F9]'
          }`}
        >
          Critical ({flags.filter(f => f.severity === 'critical').length})
        </button>
        <button
          onClick={() => setFilter('warning')}
          className={`px-3 py-1 rounded-full text-xs transition-colors font-medium border ${
            filter === 'warning'
              ? 'bg-amber-950/40 border-amber-500/30 text-[#F59E0B]'
              : 'border-[#334155] text-[#94A3B8] hover:text-[#F1F5F9]'
          }`}
        >
          Warning ({flags.filter(f => f.severity === 'warning').length})
        </button>
      </div>

      {/* Flag rows */}
      {filteredFlags.length === 0 ? (
        <Card>
          <CardContent className="p-8 text-center text-slate-500 italic text-sm">
            No compliance flags of this level detected.
          </CardContent>
        </Card>
      ) : (
        <div className="space-y-3">
          {filteredFlags.map((flag, idx) => {
            const isExpanded = expandedRow === idx;
            return (
              <Card key={idx} className="border-[#334155] overflow-hidden">
                <div
                  onClick={() => toggleRow(idx)}
                  className="p-4 flex items-center justify-between gap-4 cursor-pointer hover:bg-slate-800/40 transition-colors select-none"
                >
                  <div className="flex items-center gap-3">
                    {getSeverityIcon(flag.severity)}
                    <div>
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="font-semibold text-sm text-[#F1F5F9] capitalize">
                          {flag.flag_type.replace('_', ' ')}
                        </span>
                        <Badge variant={flag.severity === 'critical' ? 'danger' : flag.severity === 'warning' ? 'warning' : 'info'}>
                          {flag.severity}
                        </Badge>
                      </div>
                      <p className="text-xs text-[#94A3B8] mt-1">{flag.description}</p>
                    </div>
                  </div>

                  <div className="flex items-center gap-3">
                    <span className="text-xs text-[#64748B] hidden sm:inline">{flag.rule_reference}</span>
                    {isExpanded ? <ChevronUp size={16} /> : <ChevronDown size={16} />}
                  </div>
                </div>

                {isExpanded && (
                  <div className="p-4 bg-slate-900 border-t border-[#334155] font-mono text-xs text-[#94A3B8] space-y-2">
                    <div className="text-[#22C55E] font-semibold">Retrieved GST rule text (RAG source):</div>
                    <blockquote className="border-l-2 border-[#22C55E] pl-3 py-1 italic leading-relaxed text-slate-300">
                      "{flag.rag_source_chunk}"
                    </blockquote>
                    <div className="text-[10px] text-slate-500 text-right mt-1">
                      Detected at: {new Date(flag.detected_at).toLocaleString()}
                    </div>
                  </div>
                )}
              </Card>
            );
          })}
        </div>
      )}
    </div>
  );
}
