import React from 'react';
import { useAuth } from '../hooks/useAuth';

export default function AuthLayout({ children }: { children: React.ReactNode }) {
  useAuth(false);

  return (
    <div className="min-h-screen flex flex-col">
      <main className="flex-grow p-4">{children}</main>
    </div>
  );
}
