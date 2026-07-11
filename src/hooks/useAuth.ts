import { useEffect } from 'react';
import { useRouter } from 'next/router';

export const useAuth = (requireAuth: boolean = true) => {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem('token');

    if (requireAuth && !token) {
      // Если нужен токен, но его нет — на логин
      router.replace('/login');
    } else if (!requireAuth && token) {
      // Если мы на странице логина/регистрации, но токен уже есть — на главную
      router.replace('/');
    }
  }, [requireAuth, router]);

  return { isAuthenticated: typeof window !== 'undefined' ? !!localStorage.getItem('token') : false };
};
