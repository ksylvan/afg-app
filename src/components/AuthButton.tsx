'use client';

import { signIn, signOut, useSession } from 'next-auth/react';

export default function AuthButton() {
  const { data: session, status } = useSession();

  if (status === 'loading') {
    return null;
  }

  if (session) {
    return (
      <button
        type="button"
        onClick={() => signOut()}
        className="rounded bg-amber-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-amber-600 md:text-base"
      >
        Sign Out
      </button>
    );
  }

  return (
    <button
      type="button"
      onClick={() => signIn()}
      className="rounded bg-amber-500 px-4 py-2 text-sm font-medium text-white transition-colors hover:bg-amber-600 md:text-base"
    >
      Sign In
    </button>
  );
}
