import AuthLayout from '@/layouts/AuthLayout';
import MainLayout from '@/layouts/MainLayout';
import LoginTemplate from '@/templates/LoginTemplate';

export default function LoginPage() {
  return (
    <AuthLayout>
      <LoginTemplate />
    </AuthLayout>
  );
}
