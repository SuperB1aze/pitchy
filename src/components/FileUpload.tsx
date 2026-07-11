import { useState, useRef } from 'react';
import { Button } from '@/components/ui/button';
import { Upload, X, FileText, Image as ImageIcon } from 'lucide-react';
import { cn } from '@/lib/utils';

interface FileUploadProps {
  label?: string;
  accept?: string;
  multiple?: boolean;
  maxSize?: number; // в МБ
  type?: 'avatar' | 'file';
  className?: string;
}

export function FileUpload({ 
  label, 
  accept, 
  multiple = false, 
  maxSize = 5, 
  type = 'file', 
  className 
}: FileUploadProps) {
  const [files, setFiles] = useState<File[]>([]);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      const newFiles = Array.from(e.target.files);
      setFiles(prev => multiple ? [...prev, ...newFiles] : newFiles);
    }
  };

  const removeFile = (index: number) => {
    setFiles(prev => prev.filter((_, i) => i !== index));
  };

  return (
    <div className={cn("space-y-2", className)}>
      {label && <label className="text-sm font-medium">{label}</label>}
      
      <div 
        onClick={() => fileInputRef.current?.click()}
        className={cn(
          "border-2 border-dashed rounded-lg p-4 flex flex-col items-center justify-center cursor-pointer transition-colors hover:bg-muted/50",
          type === 'avatar' ? "aspect-square w-32 rounded-full mx-auto" : "w-full min-h-[100px]"
        )}
      >
        <input 
          type="file" 
          ref={fileInputRef} 
          className="hidden" 
          accept={accept} 
          multiple={multiple} 
          onChange={handleFileChange} 
        />
        
        {type === 'avatar' && files.length > 0 ? (
          <img 
            src={URL.createObjectURL(files[0])} 
            className="w-full h-full object-cover rounded-full" 
            alt="Avatar preview" 
          />
        ) : (
          <>
            <Upload className="w-6 h-6 text-muted-foreground mb-2" />
            <span className="text-xs text-muted-foreground text-center">
              {type === 'avatar' ? 'Загрузить фото' : 'Нажмите для загрузки'}
            </span>
          </>
        )}
      </div>

      {files.length > 0 && type === 'file' && (
        <div className="space-y-2">
          {files.map((file, index) => (
            <div key={index} className="flex items-center justify-between p-2 bg-muted rounded-md text-sm">
              <div className="flex items-center gap-2 truncate">
                {file.type.startsWith('image/') ? <ImageIcon className="w-4 h-4" /> : <FileText className="w-4 h-4" />}
                <span className="truncate">{file.name}</span>
              </div>
              <Button 
                variant="ghost" 
                size="icon" 
                className="h-6 w-6" 
                onClick={(e) => { e.stopPropagation(); removeFile(index); }}
              >
                <X className="w-4 h-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
