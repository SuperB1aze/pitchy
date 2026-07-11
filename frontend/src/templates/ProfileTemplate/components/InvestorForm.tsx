import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Textarea } from '@/components/ui/textarea';
import { FileUpload } from '@/components/FileUpload';

export function InvestorForm() {
  return (
    <Card>
      <CardHeader>
        <CardTitle>Профиль инвестора</CardTitle>
        <CardDescription>Настройте свои предпочтения для инвестирования</CardDescription>
      </CardHeader>
      <CardContent className="space-y-6">
        <div className="flex flex-col md:flex-row gap-6">
          <FileUpload 
            type="avatar" 
            label="Фото профиля" 
            accept="image/*" 
            className="shrink-0"
          />
          
          <div className="flex-grow space-y-4">
            <div className="space-y-2">
              <Label htmlFor="investor-name">ФИО или Название компании</Label>
              <Input id="investor-name" placeholder="Иван Иванов" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="interests">Интересы</Label>
              <Textarea id="interests" placeholder="В какие сферы вы готовы инвестировать?" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="min-check">Минимальный чек (₽)</Label>
            <Input id="min-check" type="number" placeholder="50 000" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="max-check">Максимальный чек (₽)</Label>
            <Input id="max-check" type="number" placeholder="10 000 000" />
          </div>
        </div>

        <div className="space-y-2">
          <Label>Документы и подтверждения (сертификаты, портфолио)</Label>
          <FileUpload multiple accept=".pdf,.doc,.docx" />
        </div>

        <Button variant="default" className="w-full md:w-auto">Обновить профиль инвестора</Button>
      </CardContent>
    </Card>
  );
}
