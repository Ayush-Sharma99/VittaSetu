// src/components/ui/Badge.tsx
import * as React from "react";

export interface BadgeProps extends React.HTMLAttributes<HTMLSpanElement> {
  variant?: 'success' | 'warning' | 'danger' | 'info' | 'muted';
}

export const Badge = ({ className = '', variant = 'info', ...props }: BadgeProps) => {
  const baseStyle = "inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold tracking-wide border";
  
  const variants = {
    success: "bg-emerald-950/40 text-[#22C55E] border-emerald-500/30",
    warning: "bg-amber-950/40 text-[#F59E0B] border-amber-500/30",
    danger: "bg-red-950/40 text-[#EF4444] border-red-500/30",
    info: "bg-blue-950/40 text-[#3B82F6] border-blue-500/30",
    muted: "bg-slate-800 text-[#64748B] border-[#334155]"
  };

  return (
    <span
      className={`${baseStyle} ${variants[variant]} ${className}`}
      {...props}
    />
  );
};
Badge.displayName = "Badge";
