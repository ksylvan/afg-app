# AFG Website

Modern, mobile-first music ministry coordination platform for the Alleluia Folk Group at Holy Family Parish.

## Overview

AFG Website replaces a 25-year-old Perl/CGI system with a Next.js application that enables 60+ members to manage event commitments in seconds from any device. The platform features magic link authentication, one-tap commitment tracking, and super-user tools for ministry coordinators.

**Current Phase:** Phase 02 - Magic Link Authentication (in progress)

## Quick Start

### Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) to view the application.

### Build & Production

```bash
# Production build
npm run build

# Run production server locally
npm start

# Lint code
npm run lint
```

## Technology Stack

- **Framework:** Next.js 16.1.1 with App Router
- **UI Library:** React 19.2.3
- **Styling:** Tailwind CSS v4
- **Authentication:** NextAuth v5 (beta)
- **Language:** TypeScript 5
- **Deployment:** Vercel (free tier)
- **Database:** Vercel Postgres - planned for Phase 03
- **Storage:** Vercel Blob Storage - planned for media/photos

## Project Structure

```text
/src
  /app                          # Next.js App Router
    /api/auth/[...nextauth]     # Authentication endpoints
    /login                      # Login page
    layout.tsx                  # Root layout
    page.tsx                    # Homepage
  /components                   # React components
  /lib                          # Utilities and config
    auth.ts                     # NextAuth configuration
    constants.ts                # Site constants
  proxy.ts                       # Authentication middleware
```

## Key Features

### Current (Phase 02)

- ✅ Mobile-responsive design with AFG branding (blue/amber color scheme)
- ✅ NextAuth v5 integration with JWT sessions (30-day expiration)
- ✅ Route protection middleware
- 🔄 Magic link authentication (in progress)

### Planned (Phase 03+)

- Database schema and data migration from legacy Perl/CGI system
- Event management (view/create/edit Masses, practices, special events)
- One-tap commitment tracking (Yes/No for each event)
- Super-user admin interface for ministry coordinators
- Member directory with contact information
- Public event calendar

## Target Users

- **Members (60+):** Ages 60-80; need frictionless mobile experience for event commitments
- **Coordinator (Joan):** Ministry leader requiring event reports and super-user admin capabilities
- **Developer (Kayvan):** System administrator seeking zero-maintenance architecture

## Success Metrics

**Launch Goals (Month 1):**

- 90%+ member adoption (54+ of 60 members)
- 0 password reset requests to developer
- 70%+ mobile usage rate
- <30 seconds average commitment entry time

**Operational Goals (Month 3):**

- Super-user handles 100% of password resets and user management
- 95%+ magic link authentication rate
- System operates as "invisible infrastructure"

## Documentation

- **[CLAUDE.md](CLAUDE.md)** - Developer guide for working with this codebase
- **[Product Brief](docs/about/product-brief-afg-website-2025-12-25.md)** - Full feature specifications and user personas
- **[Legacy System Reference](docs/reference/index.md)** - Data migration instructions

## Environment Variables

Create a `.env.local` file with:

```bash
NEXTAUTH_URL=http://localhost:3000
NEXTAUTH_SECRET=your-secret-key-here
```

Generate a secret with: `openssl rand -base64 32`

## Development Notes

- TypeScript path alias: `@/*` → `./src/*`
- Session strategy: JWT with 30-day expiration
- Mobile breakpoint: `md:` at 768px
- Color scheme: Blue (#1e3a8a, #1e40af) and Amber (#d97706, #f59e0b)

## Contact

**Ministry Contact:** <info@alleluiafolkgroup.org>
**Organization:** Holy Family Parish
**Developer:** Kayvan Sylvan
