'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useSession } from 'next-auth/react';
import AuthButton from './AuthButton';

export default function Header() {
  const pathname = usePathname();
  const { status } = useSession();

  const navLinks = [
    { name: 'Home', path: '/' },
    { name: 'Events', path: '/events' },
    { name: 'Calendar', path: '/calendar' },
    { name: 'About', path: '/about' },
    ...(status !== 'authenticated' ? [{ name: 'Login', path: '/login' }] : []),
  ];

  return (
    <header className="bg-gradient-to-r from-blue-900 to-blue-800 shadow-md">
      <div className="container mx-auto px-4">
        <div className="flex flex-col items-center justify-between space-y-4 py-4 md:flex-row md:space-y-0">
          <Link href="/" className="flex items-center">
            <h1 className="text-xl font-bold text-white md:text-2xl">
              Alleluia Folk Group
            </h1>
          </Link>
          
          <div className="flex flex-wrap items-center justify-center gap-4 md:gap-6">
            <nav className="flex flex-wrap gap-4 md:gap-6">
              {navLinks.map((link) => (
                <Link
                  key={link.name}
                  href={link.path}
                  className={`text-sm font-medium transition-colors duration-200 md:text-base ${
                    pathname === link.path
                      ? 'text-amber-400'
                      : 'text-blue-100 hover:text-amber-400'
                  }`}
                >
                  {link.name}
                </Link>
              ))}
            </nav>
            <AuthButton />
          </div>
        </div>
      </div>
    </header>
  );
}
