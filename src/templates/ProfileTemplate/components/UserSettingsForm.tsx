import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { PasswordInput } from '@/components/ui/password-input';
import { EditMeRequest } from '@/types/api';

export function UserSettingsForm() {
  // В будущем здесь будет начальное состояние из API
  const initialValues: EditMeRequest = {
    name: '',
    surname: '',
    patronymic: null,
  };
  return (
    <Card>
      <CardHeader>
        <CardTitle>Настройки аккаунта</CardTitle>
      </CardHeader>
      <CardContent className="space-y-4">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div className="space-y-2">
            <Label htmlFor="email">Электронная почта</Label>
            <Input id="email" type="email" placeholder="example@mail.com" />
          </div>
          <div className="space-y-2">
            <Label htmlFor="phone">Номер телефона</Label>
            <Input id="phone" type="tel" placeholder="+7 (999) 000-00-00" />
          </div>
        </div>
        <div className="pt-4 border-t space-y-2">
          <h3 className="text-sm font-bold">Смена пароля</h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="space-y-2">
              <Label htmlFor="new-password">Новый пароль</Label>
              <PasswordInput id="new-password" />
            </div>
            <div className="space-y-2">
              <Label htmlFor="confirm-password">Подтвердите пароль</Label>
              <PasswordInput id="confirm-password" />
            </div>
          </div>
        </div>
        <Button className="mt-4">Сохранить изменения</Button>
      </CardContent>
    </Card>
  );
}
