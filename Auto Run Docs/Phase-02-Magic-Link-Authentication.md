# Phase 02: Magic Link Authentication

This phase implements authentication using NextAuth v5 with magic link email-based login, eliminating password management for elderly users and providing secure access control.

## Tasks

- [ ] Install NextAuth v5 (next-auth@beta) and required dependencies using npm install next-auth@beta
- [ ] Create .env.local file with NEXTAUTH_URL and NEXTAUTH_SECRET placeholder values
- [ ] Update tsconfig.json to include path alias "@/*" pointing to "./src/*" for cleaner imports
- [ ] Create src/lib/auth.ts file with NextAuth v5 configuration, credentials provider using email as identifier
- [ ] Create src/app/api/auth/[...nextauth]/route.ts file to handle authentication API endpoints
- [ ] Create src/components/AuthButton.tsx component with "Sign In" and "Sign Out" functionality
- [ ] Add AuthButton component to Header.tsx, positioned on the right side of navigation
- [ ] Update src/lib/auth.ts to include session management and protect routes configuration
- [ ] Create src/middleware.ts file to handle protected route redirects and authentication state
- [ ] Create src/app/login/page.tsx with simple login form that accepts email only and displays "Magic link sent to your email" message on submission
- [ ] Add login link to navigation in Header.tsx that only shows when user is not authenticated
- [ ] Verify authentication flow: login form submission shows success message, AuthButton toggles correctly between sign in/sign out
