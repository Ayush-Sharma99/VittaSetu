// src/components/ReconciliationTable.tsx
'use client';
import { Badge } from '@/components/ui/Badge';
import { AlertCircle, CheckCircle, HelpCircle } from 'lucide-react';

export interface InvoiceItem {
  id: string;
  invoice_number: string;
  invoice_date: string;
  vendor_or_customer: string;
  amount: number;
  gst_amount: number;
  gst_rate: number;
  hsn_code?: string;
  reconciled: boolean;
}

export default function ReconciliationTable({ invoices }: { invoices: InvoiceItem[] }) {
  return (
    <div className="bg-[#1E293B] border border-[#334155] rounded-xl overflow-hidden shadow-lg">
      <div className="overflow-x-auto">
        <table className="w-full text-left border-collapse">
          <thead>
            <tr className="border-b border-[#334155] bg-slate-900/50 text-[#94A3B8] text-xs font-semibold uppercase tracking-wider">
              <th className="p-4">Invoice No.</th>
              <th className="p-4">Date</th>
              <th className="p-4">Customer/Vendor</th>
              <th className="p-4 text-right">Taxable Amt</th>
              <th className="p-4 text-right">GST Amt</th>
              <th className="p-4">HSN</th>
              <th className="p-4 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-[#334155] text-sm text-[#F1F5F9]">
            {invoices.length === 0 ? (
              <tr>
                <td colSpan={7} className="p-8 text-center text-slate-500 italic">
                  No invoices found.
                </td>
              </tr>
            ) : (
              invoices.map((inv) => (
                <tr key={inv.id} className="hover:bg-slate-800/20 transition-colors">
                  <td className="p-4 font-mono font-semibold">{inv.invoice_number}</td>
                  <td className="p-4 text-xs text-[#94A3B8]">{inv.invoice_date}</td>
                  <td className="p-4">{inv.vendor_or_customer}</td>
                  <td className="p-4 text-right font-mono">₹{inv.amount.toLocaleString('en-IN')}</td>
                  <td className="p-4 text-right font-mono text-[#94A3B8]">
                    ₹{inv.gst_amount.toLocaleString('en-IN')}
                  </td>
                  <td className="p-4 font-mono text-xs text-[#94A3B8]">{inv.hsn_code || '-'}</td>
                  <td className="p-4 text-center">
                    {inv.reconciled ? (
                      <div className="inline-flex items-center gap-1 text-[#22C55E] bg-emerald-950/40 border border-emerald-500/20 px-2 py-0.5 rounded-full text-xs font-medium">
                        <CheckCircle size={12} />
                        <span>Matched</span>
                      </div>
                    ) : (
                      <div
                        className="inline-flex items-center gap-1 text-[#F59E0B] bg-amber-950/40 border border-amber-500/20 px-2 py-0.5 rounded-full text-xs font-medium cursor-help"
                        title="Action needed: No matching payment found in bank statement."
                      >
                        <AlertCircle size={12} />
                        <span>Action Needed</span>
                      </div>
                    )}
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
