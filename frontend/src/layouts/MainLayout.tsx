import React, { useEffect, useState } from 'react';
import { useAuth } from '../hooks/useAuth';
import Link from 'next/link';
import { useRouter } from 'next/router';
import { User, Heart, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { cn } from '@/lib/utils';
import { apiClient } from '@/lib/api-client';

export default function MainLayout({ children }: { children: React.ReactNode }) {
  const { isAuthenticated } = useAuth(true);
  const router = useRouter();
  const [userName, setUserName] = useState<string | null>(null);

  useEffect(() => {
    if (!isAuthenticated) return;
    apiClient
      .getUserCredentials()
      .then((user) => setUserName(`${user.name} ${user.surname}`))
      .catch(() => {
        localStorage.removeItem('token');
        router.replace('/login');
      });
  }, [isAuthenticated, router]);

  const handleLogout = async () => {
    try {
      await apiClient.logout();
    } finally {
      localStorage.removeItem('token');
      router.push('/login');
    }
  };

  const navItems = [
    { label: 'Ищу проект', href: '/' },
    { label: 'Ищу инвестора', href: '/investors' },
  ];

  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60 sticky top-0 z-50">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2 font-bold text-xl text-primary">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center text-primary-foreground">
                P
              </div>
              <span>Pitchy</span>
            </Link>

            <nav className="hidden md:flex items-center bg-muted/50 p-1 rounded-lg">
              {navItems.map((item) => {
                const isActive = router.pathname === item.href;
                return (
                  <Link
                    key={item.href}
                    href={item.href}
                    className={cn(
                      "px-4 py-1.5 text-sm font-medium rounded-md transition-all",
                      isActive 
                        ? "bg-background text-foreground shadow-sm"
                        : "text-muted-foreground hover:text-foreground"
                    )}
                  >
                    {item.label}
                  </Link>
                );
              })}
            </nav>
          </div>

          <div className="flex items-center gap-2">
            {userName && (
              <span className="hidden sm:inline text-sm text-muted-foreground mr-2">
                Привет, {userName}
              </span>
            )}
            <Link href="/favorites">
                <Button variant="ghost" size="icon" className="text-foreground hover:text-primary cursor-pointer">
                    <Heart className="w-5 h-5" />
                </Button>
              </Link>

             <Link href="/profile">
                <Button variant="ghost" size="icon" className="text-foreground hover:text-primary cursor-pointer">
                    <User className="w-5 h-5" />
                </Button>
            </Link>

            <Button
              variant="ghost"
              size="icon"
              className="text-foreground hover:text-primary cursor-pointer"
              onClick={handleLogout}
            >
              <LogOut className="w-5 h-5" />
            </Button>
          </div>
        </div>
      </header>
      <main className="flex-grow container mx-auto p-4 md:p-6">{children}</main>
    </div>
  );
}
