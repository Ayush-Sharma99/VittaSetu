// src/components/ui/Card.tsx
import * as React from "react";

export const Card = React.forwardRef<HTMLDivElement, React.HTMLAttributes<HTMLDivElement>>(
  ({ className = '', ...props }, ref) => (
    <div
      ref={ref}
      className={`bg-[#1E293B] border border-[#334155] rounded-xl text-[#F1F5F9] shadow-lg ${className}`}
      {...props}
    />
  )
);
Card.displayName = "Card";

export const CardHeader = ({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={`p-6 pb-4 border-b border-[#334155] ${className}`} {...props} />
);
CardHeader.displayName = "CardHeader";

export const CardTitle = ({ className = '', ...props }: React.HTMLAttributes<HTMLHeadingElement>) => (
  <h3 className={`text-lg font-semibold text-[#F1F5F9] tracking-tight ${className}`} {...props} />
);
CardTitle.displayName = "CardTitle";

export const CardContent = ({ className = '', ...props }: React.HTMLAttributes<HTMLDivElement>) => (
  <div className={`p-6 pt-4 ${className}`} {...props} />
);
CardContent.displayName = "CardContent";
