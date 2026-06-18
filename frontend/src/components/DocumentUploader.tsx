// src/components/DocumentUploader.tsx
'use client';
import { useState, useRef } from 'react';
import { Badge } from '@/components/ui/Badge';
import { Card, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { FileUp, CheckCircle, Upload } from 'lucide-react';

interface DocumentUploaderProps {
  label: string;
  docType: string;
  onSelectFile: (file: File | null) => void;
}

export default function DocumentUploader({ label, docType, onSelectFile }: DocumentUploaderProps) {
  const [dragActive, setDragActive] = useState(false);
  const [fileDetails, setFileDetails] = useState<{ name: string; size: string } | null>(null);
  
  const inputRef = useRef<HTMLInputElement>(null);

  const handleDrag = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    if (e.type === "dragenter" || e.type === "dragover") {
      setDragActive(true);
    } else if (e.type === "dragleave") {
      setDragActive(false);
    }
  };

  const processFile = (file: File) => {
    if (file.size > 10 * 1024 * 1024) {
      alert("File size limit is 10MB");
      return;
    }
    setFileDetails({
      name: file.name,
      size: (file.size / (1024 * 1024)).toFixed(2) + " MB"
    });
    onSelectFile(file);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      processFile(e.dataTransfer.files[0]);
    }
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    e.preventDefault();
    if (e.target.files && e.target.files[0]) {
      processFile(e.target.files[0]);
    }
  };

  return (
    <Card
      className={`border-2 border-dashed transition-colors relative cursor-pointer ${
        dragActive ? 'border-[#22C55E] bg-[#22C55E]/5' : 'border-[#334155] hover:border-[#3b82f6]'
      }`}
      onDragEnter={handleDrag}
      onDragOver={handleDrag}
      onDragLeave={handleDrag}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,image/*"
        onChange={handleChange}
        className="hidden"
      />
      
      <CardContent className="p-6 flex flex-col items-center text-center space-y-4">
        {fileDetails ? (
          <div className="flex flex-col items-center space-y-2 animate-fadeIn">
            <CheckCircle className="text-[#22C55E]" size={36} />
            <div className="text-sm font-semibold text-[#F1F5F9] truncate max-w-[200px]">
              {fileDetails.name}
            </div>
            <div className="text-xs text-[#94A3B8]">{fileDetails.size}</div>
            <Badge variant="success">Ready</Badge>
          </div>
        ) : (
          <div className="flex flex-col items-center space-y-2">
            <Upload className="text-[#94A3B8]" size={36} />
            <div className="text-sm font-semibold text-[#F1F5F9]">{label}</div>
            <div className="text-xs text-[#64748B]">PDF / Image formats up to 10MB</div>
            <Button variant="secondary" size="sm" className="mt-2 pointer-events-none">
              Browse File
            </Button>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
