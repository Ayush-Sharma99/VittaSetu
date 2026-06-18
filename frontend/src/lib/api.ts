// src/lib/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export async function resetDemo() {
  const res = await fetch(`${API_BASE_URL}/api/demo/reset`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to reset demo');
  return res.json();
}

export async function uploadDocument(file: File, docType: string, businessId: string) {
  const formData = new FormData();
  formData.append('file', file);
  formData.append('doc_type', docType);
  formData.append('business_id', businessId);

  const res = await fetch(`${API_BASE_URL}/api/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) throw new Error('Document upload failed');
  return res.json();
}

export async function triggerPipeline(businessId: string) {
  const res = await fetch(`${API_BASE_URL}/api/process?business_id=${businessId}`, {
    method: 'POST',
  });
  if (!res.ok) throw new Error('Failed to start pipeline processing');
  return res.json();
}

export async function getCreditPassport(businessId: string) {
  const res = await fetch(`${API_BASE_URL}/api/score/${businessId}`);
  if (!res.ok) throw new Error('Failed to fetch credit score details');
  return res.json();
}

export async function sendChatMessage(businessId: string, message: string) {
  const res = await fetch(`${API_BASE_URL}/api/chat`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ business_id: businessId, message }),
  });
  if (!res.ok) throw new Error('Chat request failed');
  return res.json();
}

export function getStatusEventSource(jobId: string): EventSource {
  return new EventSource(`${API_BASE_URL}/api/status/${jobId}`);
}
