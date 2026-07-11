import AuthLayout from '@/layouts/AuthLayout';
import MainLayout from '@/layouts/MainLayout';
import RegisterTemplate from '@/templates/RegisterTemplate';

export default function RegisterPage() {
  return (
    <AuthLayout>
      <RegisterTemplate />
    </AuthLayout>
  );
}
