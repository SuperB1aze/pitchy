import React from 'react';
import { Formik, Form, Field, ErrorMessage } from 'formik';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import { PasswordInput } from '@/components/ui/password-input';
import { Label } from '@/components/ui/label';
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from '@/components/ui/card';
import Link from 'next/link';
import { Input } from '@/components/ui/input';

const loginSchema = z.object({
  email: z.string().email('Некорректный email'),
  password: z.string().min(6, 'Пароль должен быть не менее 6 символов'),
});

type LoginValues = z.infer<typeof loginSchema>;

export default function LoginTemplate() {
  const initialValues: LoginValues = { email: '', password: '' };

  const validate = (values: LoginValues) => {
    const result = loginSchema.safeParse(values);
    if (result.success) return {};
    
    const errors: Record<string, string> = {};
    result.error.issues.forEach((issue) => {
      if (issue.path[0]) errors[issue.path[0] as string] = issue.message;
    });
    return errors;
  };

  return (
    <div className="flex items-center justify-center min-h-[calc(100vh-120px)] p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>Вход</CardTitle>
          <CardDescription>Введите свои данные для входа в аккаунт</CardDescription>
        </CardHeader>
        <Formik
          initialValues={initialValues}
          validate={validate}
          onSubmit={(values) => {
            console.log('Login values:', values);
            alert('Вход выполнен (см. консоль)');
          }}
        >
          {({ isSubmitting }) => (
            <Form>
              <CardContent className="space-y-4">
                <div className="space-y-2">
                  <Label htmlFor="email">Email</Label>
                  <Field name="email" as={Input} type="email" placeholder="name@example.com" />
                  <ErrorMessage name="email" component="div" className="text-sm text-red-500" />
                </div>
                  <div className="space-y-2">
                    <Label htmlFor="password">Пароль</Label>
                    <Field name="password" as={PasswordInput} />
                    <ErrorMessage name="password" component="div" className="text-sm text-red-500" />
                  </div>              </CardContent>
              <CardFooter className="flex flex-col space-y-4">
                <Button type="submit" className="w-full" disabled={isSubmitting}>
                  Войти
                </Button>
                <div className="text-sm text-center">
                  Нет аккаунта?{' '}
                  <Link href="/register" className="text-blue-600 hover:underline">
                    Зарегистрироваться
                  </Link>
                </div>
              </CardFooter>
            </Form>
          )}
        </Formik>
      </Card>
    </div>
  );
}
