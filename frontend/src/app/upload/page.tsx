// src/app/upload/page.tsx
'use client';
import { useState, useEffect, Suspense } from 'react';
import { useRouter, useSearchParams } from 'next/navigation';
import { useAppStore } from '@/lib/store';
import { resetDemo, uploadDocument, triggerPipeline } from '@/lib/api';
import DocumentUploader from '@/components/DocumentUploader';
import { Button } from '@/components/ui/Button';
import { Card, CardContent } from '@/components/ui/Card';
import { AlertCircle, HelpCircle } from 'lucide-react';

function UploadPageContent() {
  const router = useRouter();
  const searchParams = useSearchParams();
  const isDemo = searchParams.get('demo') === 'true';

  const { setBusinessId, setJobId, setDemoMode, businessId } = useAppStore();
  
  const [bankFile, setBankFile] = useState<File | null>(null);
  const [invoiceFile, setInvoiceFile] = useState<File | null>(null);
  const [gstFile, setGstFile] = useState<File | null>(null);
  
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isDemo) {
      setDemoMode(true);
      // Auto-trigger db reset for Ravi Kumar Tiles
      setLoading(true);
      resetDemo()
        .then((data) => {
          setBusinessId(data.business_id);
        })
        .catch((e) => console.error(e))
        .finally(() => setLoading(false));
    }
  }, [isDemo]);

  const handleStartAnalysis = async () => {
    if (!businessId) return;
    setLoading(true);

    try {
      if (isDemo) {
        // In demo mode, documents are already registered by reset endpoint
        const startResult = await triggerPipeline(businessId);
        setJobId(startResult.job_id);
        router.push(`/processing?jobId=${startResult.job_id}`);
      } else {
        // Upload user files
        if (bankFile) await uploadDocument(bankFile, 'bank_statement', businessId);
        if (invoiceFile) await uploadDocument(invoiceFile, 'invoice', businessId);
        if (gstFile) await uploadDocument(gstFile, 'gst_return', businessId);

        const startResult = await triggerPipeline(businessId);
        setJobId(startResult.job_id);
        router.push(`/processing?jobId=${startResult.job_id}`);
      }
    } catch (e) {
      alert("Failed to initialize document analysis.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-2xl mx-auto space-y-8 animate-fadeIn">
      <div className="space-y-2 text-center">
        <span className="text-xs text-[#22C55E] uppercase font-mono tracking-wider font-bold">
          Step 1 of 3
        </span>
        <h1 className="text-3xl font-bold text-[#F1F5F9]">Upload Documents</h1>
        <p className="text-sm text-[#94A3B8]">
          Upload ledgers, invoices, and filing reports to construct your credit-readiness passport.
        </p>
      </div>

      {isDemo && (
        <Card className="border-emerald-500/20 bg-emerald-950/10">
          <CardContent className="p-4 flex items-start gap-3 text-xs sm:text-sm text-[#22C55E]">
            <AlertCircle className="shrink-0 mt-0.5" size={18} />
            <div>
              <span className="font-bold">Demo mode active</span> &mdash; using Ravi Kumar's sample documents (1 Bank Statement, 2 Invoices, 1 GST Return). Click 'Start Analysis' to proceed.
            </div>
          </CardContent>
        </Card>
      )}

      {/* Grid of upload zones */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <DocumentUploader
          label="Bank Statement"
          docType="bank_statement"
          onSelectFile={setBankFile}
        />
        <DocumentUploader
          label="Invoices (PDF/IMG)"
          docType="invoice"
          onSelectFile={setInvoiceFile}
        />
        <DocumentUploader
          label="GST Return"
          docType="gst_return"
          onSelectFile={setGstFile}
        />
      </div>

      <div className="flex justify-end pt-4">
        <Button
          onClick={handleStartAnalysis}
          disabled={loading || (!isDemo && !bankFile && !invoiceFile && !gstFile)}
          size="lg"
          className="w-full sm:w-auto font-bold tracking-wide"
        >
          {loading ? "Initializing..." : "Start Analysis →"}
        </Button>
      </div>
    </div>
  );
}

export default function UploadPage() {
  return (
    <Suspense fallback={<div className="text-center py-12 text-slate-400">Loading document uploader...</div>}>
      <UploadPageContent />
    </Suspense>
  );
}
