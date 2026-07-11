import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { FileUpload } from '@/components/FileUpload';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';

const CATEGORIES = [
  { value: 'web', label: 'Веб-разработка' },
  { value: 'mobile', label: 'Мобильные приложения' },
  { value: 'design', label: 'Дизайн' },
  { value: 'it', label: 'IT-инфраструктура' },
  { value: 'ecology', label: 'Экология' },
  { value: 'fintech', label: 'Финтех' },
];

export function ProjectForm() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Информация о проекте</CardTitle>
        <CardDescription>Заполните данные, чтобы привлечь инвестиции</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex flex-col md:flex-row gap-6">
          <FileUpload 
            type="avatar" 
            label="Обложка проекта" 
            accept="image/*" 
            className="shrink-0"
          />
          
          <div className="flex-grow space-y-4">
            <div className="space-y-2">
              <Label htmlFor="project-name">Название проекта</Label>
              <Input id="project-name" placeholder="Например: EcoSphere AI" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="project-desc">Описание проекта</Label>
              <Textarea id="project-desc" placeholder="Расскажите о вашей идее..." className="min-h-[100px]" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="target-amount">Цель сбора (₽)</Label>
            <Input 
              id="target-amount" 
              type="number" 
              min="0" 
              onKeyDown={(e) => {
                if (e.key === '-' || e.key === 'e') e.preventDefault();
              }}
              placeholder="1 000 000" 
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="project-category">Категория</Label>
            <Select>
              <SelectTrigger id="project-category" className='bg-card'>
                <SelectValue placeholder="Выберите категорию" />
              </SelectTrigger>
              <SelectContent>
                {CATEGORIES.map((cat) => (
                  <SelectItem key={cat.value} value={cat.value}>
                    {cat.label}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        <div className="space-y-2">
          <Label>Дополнительные материалы (презентации, фото, документы)</Label>
          <FileUpload multiple accept=".pdf,.doc,.docx,.jpg,.png" />
        </div>

        <Button variant="default" className="w-full md:w-auto">Обновить данные проекта</Button>
      </CardContent>
    </Card>
  );
}


