// src/app/layout.tsx
import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "@/styles/globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-sans" });

export const metadata: Metadata = {
  title: "VittaSetu AI - Your ledger is your loan application.",
  description: "AI-powered credit readiness passport and compliance advisor for Indian MSMEs.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark bg-[#0F172A]">
      <body className={`${inter.variable} font-sans text-[#F1F5F9] bg-[#0F172A] min-h-screen flex flex-col`}>
        <header className="border-b border-[#334155] py-4 bg-slate-900/50 backdrop-blur-md sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 flex items-center justify-between">
            <div className="flex items-center gap-2">
              <img src="/logo.png" alt="VittaSetu" className="h-10 w-auto" />
            </div>
            
            <div className="text-xs text-slate-500 font-mono hidden md:inline">
              MSME Credit Passport Protocol v1.0
            </div>
          </div>
        </header>

        <main className="flex-1 max-w-7xl w-full mx-auto px-4 pt-2 pb-8">
          {children}
        </main>

        <footer className="border-t border-[#334155] py-6 text-center text-xs text-[#64748B]">
          <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-4">
            <div>&copy; 2026 VittaSetu AI. All rights reserved.</div>
            <div className="flex gap-4">
              <span>63M MSMEs</span>
              <span>&middot;</span>
              <span>₹30L Cr Credit Gap</span>
              <span>&middot;</span>
              <span>Powered by Gemini AI</span>
            </div>
          </div>
        </footer>
      </body>
    </html>
  );
}
