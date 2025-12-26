# Phase 03: Database Schema and Setup

This phase establishes the database infrastructure using Vercel Postgres, creating all necessary tables for users, events, and commitments with proper relationships and constraints.

## Tasks

- [ ] Install @vercel/postgres package using npm install @vercel/postgres
- [ ] Update .env.local to include POSTGRES_URL, POSTGRES_PRISMA_URL, POSTGRES_URL_NON_POOLING placeholder values with Vercel Postgres connection string format
- [ ] Create src/db/schema.ts file with SQL schema definitions: users table (id, name, email, phone, is_admin, created_at), events table (id, title, description, event_date, location, created_at), commitments table (id, user_id, event_id, status, created_at, updated_at)
- [ ] Create src/db/seed.sql file with INSERT statements for initial admin user (Joan) with is_admin=true and sample event data for upcoming ministry events
- [ ] Create src/lib/db.ts utility file with database connection helper using sql from @vercel/postgres
- [ ] Create src/db/migrate.ts file that executes schema.sql and seed.sql files to initialize database
- [ ] Add npm script to package.json: "db:setup": "tsx src/db/migrate.ts" for database initialization
- [ ] Install tsx package using npm install -D tsx for TypeScript execution
- [ ] Run npm run db:setup to create database tables and seed initial data
- [ ] Create src/lib/types.ts file with TypeScript interfaces matching database schema (User, Event, Commitment types)
- [ ] Verify database tables exist by checking .env.local and confirming connection works (add temporary console log verification in migrate.ts)
