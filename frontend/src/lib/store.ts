// src/lib/store.ts
import { create } from 'zustand';

export interface AgentStep {
  agent: string;
  step: number;
  status: 'running' | 'done' | 'error';
  message: string;
  reasoning?: string;
  duration?: string;
}

export interface CreditPassport {
  business_id: string;
  score: number;
  grade: string;
  computed_at: string;
  factor_breakdown: {
    filing_compliance: number;
    filing_timeliness: number;
    invoice_reconciliation: number;
    revenue_trend: number;
    cash_flow_consistency: number;
    compliance_health: number;
  };
  explanation: string;
  top_strength: string;
  top_action: string;
  compliance_flags: Array<{
    flag_type: string;
    severity: 'critical' | 'warning' | 'info';
    description: string;
    rule_reference: string;
    rag_source_chunk: string;
    detected_at: string;
  }>;
}

interface AppState {
  businessId: string | null;
  jobId: string | null;
  agentSteps: AgentStep[];
  creditPassport: CreditPassport | null;
  demoMode: boolean;
  setBusinessId: (id: string | null) => void;
  setJobId: (id: string | null) => void;
  addAgentStep: (step: AgentStep) => void;
  clearAgentSteps: () => void;
  setCreditPassport: (passport: CreditPassport | null) => void;
  setDemoMode: (mode: boolean) => void;
}

export const useAppStore = create<AppState>((set) => ({
  businessId: null,
  jobId: null,
  agentSteps: [],
  creditPassport: null,
  demoMode: false,
  setBusinessId: (id) => set({ businessId: id }),
  setJobId: (id) => set({ jobId: id }),
  addAgentStep: (step) => set((state) => {
    // Avoid duplicate step records if stream duplicates
    const filtered = state.agentSteps.filter(s => !(s.agent === step.agent && s.status === step.status));
    return { agentSteps: [...filtered, step] };
  }),
  clearAgentSteps: () => set({ agentSteps: [] }),
  setCreditPassport: (passport) => set({ creditPassport: passport }),
  setDemoMode: (mode) => set({ demoMode: mode }),
}));
