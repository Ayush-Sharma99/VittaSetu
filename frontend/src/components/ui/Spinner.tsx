// src/components/ui/Spinner.tsx
import * as React from "react";

export const Spinner = ({ className = '' }: { className?: string }) => {
  return (
    <div
      className={`animate-spin rounded-full border-2 border-t-transparent border-[#22C55E] h-5 w-5 ${className}`}
    />
  );
};
Spinner.displayName = "Spinner";
