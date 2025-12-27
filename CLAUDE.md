# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

AFG Website is a modern Next.js application replacing a 25-year-old Perl/CGI system for the Alleluia Folk Group at Holy Family Parish. It enables 60+ members to manage music ministry event commitments through a mobile-first interface with magic link authentication.

**Current Phase:** Phase 02 - Magic Link Authentication (in progress)
**Target Users:** Ministry members (ages 60-80), ministry coordinator (Joan), system administrator (Kayvan)
**Success Goal:** Zero password reset support requests; members commit to events in <30 seconds from any device

## Development Commands

```bash
# Development server (http://localhost:3000)
npm run dev

# Production build
npm run build

# Run production server locally
npm start

# Lint code
npm run lint
```

## Architecture

### Authentication Flow

This application uses **NextAuth v5 (beta)** with a credentials-based provider (magic links planned but not yet implemented).

**Key files:**

- [src/lib/auth.ts](src/lib/auth.ts) - Core NextAuth configuration with JWT sessions (30-day expiration)
- [src/app/api/auth/[...nextauth]/route.ts](src/app/api/auth/[...nextauth]/route.ts) - NextAuth API handlers
- [src/proxy.ts](src/proxy.ts) - Middleware for route protection (redirects logged-in users from /login)
- [src/components/Providers.tsx](src/components/Providers.tsx) - SessionProvider wrapper for client components

**Current authentication flow:**

1. User enters email on [/login](src/app/login/page.tsx) page
2. `signIn('credentials', { email })` called via next-auth/react
3. NextAuth validates email and creates JWT token
4. Session stored for 30 days; user redirected to homepage

**Note:** The UI displays "magic link sent" messaging but currently uses credential-based auth. True email-based magic links are planned for future implementation.

### Directory Structure

```text
/src
  /app                          # Next.js App Router
    /api/auth/[...nextauth]     # Authentication endpoints
    /login                      # Login page
    layout.tsx                  # Root layout with header/footer
    page.tsx                    # Homepage/dashboard
  /components                   # React components
    AuthButton.tsx              # Sign in/out button
    Header.tsx                  # Navigation with conditional Login link
    Footer.tsx                  # Site footer
    Providers.tsx               # SessionProvider wrapper
  /lib
    auth.ts                     # NextAuth configuration
    constants.ts                # Site constants (colors, nav links)
  proxy.ts                       # Authentication middleware
```

### Data Models (Planned - Not Yet Implemented)

The application will integrate Vercel Postgres in Phase 03:

**Users Table:**

- 60+ members with login credentials, contact info, admin flags
- Fields: email, password_hash, full_name, phone, address, birthday, is_admin

**Events Table:**

- 65+ events (Masses, practices, special celebrations)
- Fields: description, location, event_time, arrive_by, timezone (Pacific Time)

**Commitments Join Table:**

- Links users to events with status (Yes/No/Pending)
- Fields: user_id, event_id, commitment_status

**Legacy Data Migration:**

- Source: 25-year-old Perl/CGI system with file-based database (persons.db, events.db)
- Location: [docs/reference/old_cgi_site](docs/reference/old_cgi_site)
- Sync command (from docs/reference): `scp 'danheller.com:public_html/afg/commitment/save/*' ./old_cgi_site/commitment/save/`

### TypeScript Path Aliases

The project uses `@/*` as an alias for `./src/*` (configured in [tsconfig.json](tsconfig.json)).

**Example:**

```typescript
import { auth } from "@/lib/auth"
import { SITE_CONFIG } from "@/lib/constants"
```

### Styling

- **Framework:** Tailwind CSS v4
- **Color Scheme:** Blue (#1e3a8a, #1e40af) and Amber (#d97706, #f59e0b) - defined in [src/lib/constants.ts](src/lib/constants.ts)
- **Fonts:** Geist (from next/font)
- **Responsive Breakpoint:** `md:` at 768px for mobile-first design

## Key Product Requirements

### Success Metrics (from Product Brief)

**Launch Phase (Month 1):**

- 90%+ member adoption (54+ of 60 members)
- 0 password reset requests to developer
- 70%+ mobile usage rate
- Average commitment entry time <30 seconds

**Operational Phase (Month 3):**

- Super-user (Joan) handles 100% of password resets and user management
- 95%+ magic link authentication rate
- System operates as "invisible infrastructure"

### User Personas

**Pat (Member - 68 years old):**

- Wants frictionless mobile experience
- Forgets passwords frequently (currently requires developer intervention)
- Needs to see upcoming events and make Yes/No commitments quickly

**Joan (Coordinator - 62 years old):**

- Needs event-by-event commitment reports (who's committed/declined/pending)
- Must make commitments on behalf of members who contact her
- Requires ability to reset passwords without developer help
- Wants mobile-accessible admin interface

**Kayvan (Developer):**

- Goal: Zero support burden after Month 1
- Currently spends 60-120 minutes/year on password resets via SSH/CLI
- Needs Joan empowered to handle all routine admin tasks

### MVP Scope (Current Phase 02 → Future Phases)

**Completed:**

- ✅ Project setup with Next.js 16 + React 19 + TypeScript
- ✅ Tailwind CSS v4 styling and responsive design
- ✅ Homepage with hero, mission statement, feature cards
- ✅ NextAuth v5 integration with credentials provider
- ✅ Route protection middleware

**In Progress (Phase 02):**

- 🔄 Magic link authentication implementation
- 🔄 Email delivery service integration

**Planned (Phase 03+):**

- Database schema setup (Vercel Postgres)
- Data migration from legacy Perl/CGI system
- Event management (view/create/edit events)
- Commitment tracking (one-tap Yes/No for members)
- Super-user admin interface (Joan's tools)
- Address directory (member contact info)
- Public calendar (viewable by anyone)

**Out of Scope for MVP:**

- Email notifications (batched confirmations, event reminders)
- Photo gallery migration
- Advanced reporting (PDF/CSV export, analytics)
- Recurring commitment preferences

## Important Constraints

### Security

- Current credentials provider is placeholder; production requires proper email-based magic links
- Session tokens expire after 30 days (JWT strategy)
- Password hashing must avoid obsolete DES from legacy system

### Performance

- Target: <30 second commitment entry time
- Mobile-first: 70%+ of usage expected from mobile devices
- Responsive design required for ages 60-80 user base

### Deployment

- Vercel hosting (zero cost within free tier)
- Vercel Postgres - 0.5GB free tier (planned)
- Vercel Blob Storage - 1GB free tier (planned for photos)

## Documentation

**Product Context:**

- [Product Brief](docs/about/product-brief-afg-website-2025-12-25.md) - Full feature specifications and user personas
- [Brainstorming Session](docs/about/brainstorming-session-2025-12-25.md) - Design discussions
- [Legacy System Reference](docs/reference/index.md) - Data sync instructions from old Perl/CGI site

**Key Reference Documents:**

- Product brief contains detailed user journeys, success metrics, and MVP scope
- Legacy data files in docs/reference/old_cgi_site/ preserve 25 years of commitment history
