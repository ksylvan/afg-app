---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments: ['_bmad-output/analysis/brainstorming-session-2025-12-25.md']
workflowType: 'product-brief'
lastStep: 5
project_name: 'afg-website'
user_name: 'Kayvan'
date: '2025-12-25'
---

# Product Brief: afg-website

**Date:** 2025-12-25
**Author:** Kayvan

---

## Executive Summary

AFG Website is a modern, mobile-first music ministry coordination platform that replaces a 25-year-old Perl/CGI system with Next.js and React. The platform enables 60+ Alleluia Folk Group members at Holy Family Parish to manage event commitments in seconds from any device, while empowering designated super-users (like ministry coordinator Joan) to oversee scheduling, assist members, and generate reports without technical intervention from the developer.

**Core Value Delivered:**

- **For Members:** One-tap commitment tracking with instant feedback, eliminating password reset friction through magic link authentication
- **For Coordinators:** Real-time visibility into who's committed, who's declined, and who hasn't responded for each Mass and practice session
- **For Administrator (Kayvan):** Zero-maintenance modern architecture deployed on Vercel with seamless data migration preserving all historical commitments

**Key Innovation:** Distributed support model where super-users handle password resets, commitment management, and user administration - scaling ministry coordination beyond a single developer.

---

## Core Vision

### Problem Statement

The Alleluia Folk Group at Holy Family Parish relies on a legacy Perl/CGI application built in the late 1990s to coordinate music ministry commitments across 60+ members for weekly Masses and practice sessions. The aging system creates friction at every level:

- **For Members (ages 60-80):** Password resets require emailing/calling Kayvan for manual intervention via command-line tools (6-12 times/year). The non-responsive HTML interface is difficult to use on mobile devices where most members access the system.

- **For Ministry Coordinator (Joan):** No ability to help members directly - all support requests flow through Kayvan. Viewing commitment reports requires desktop access to the legacy interface.

- **For Developer (Kayvan):** Every password reset requires SSH access to hosting control panel and manual `persondb.pl` commands (5-10 minutes each). The file-based database (persons.db, events.db) and obsolete DES password hashing create security risks and maintenance burden.

### Problem Impact

**Current Pain Points:**

- Members forget passwords every few months → manual reset cycle → 60-120 minutes/year in support time
- Mobile-hostile interface forces members to use desktop computers to make commitments
- Joan cannot assist members directly, creating bottleneck dependency on single developer
- Legacy Perl/CGI stack makes adding features or fixing bugs time-consuming and risky
- Non-responsive design fails to meet modern user expectations for ministry tools

**Cost of Inaction:**

- Continued support burden prevents feature development and system improvements
- Member frustration may lead to disengagement from ministry coordination
- Technical debt accumulates, making future migration even more complex
- Security risk from obsolete DES password hashing (crackable in seconds)

### Why Existing Solutions Fall Short

**Commercial Ministry Tools** (Planning Center, MSP, SignUpGenius):

- These generic solutions don't fit AFG's specific workflow and community culture
- Migration would abandon 25 years of historical data and require complete user retraining
- Monthly costs add up for a volunteer ministry with limited budget
- Over-engineered features create unnecessary complexity for simple commitment tracking

**Current Legacy System:**

- Built for 1990s desktop web browsing, incompatible with mobile-first user expectations
- Single-point-of-failure support model (only Kayvan can reset passwords)
- File-based database limits scalability and reporting capabilities
- Obsolete technology stack makes maintenance and feature development prohibitively expensive

### Proposed Solution

A modern, mobile-first web application built with Next.js 16+ and React that preserves AFG's proven commitment workflow while delivering zero-friction user experience and distributed support capabilities.

**Core Features:**

**For All Members:**

- Magic link authentication eliminates password reset support burden
- One-tap commitment UI: Green checkmark (Yes) or red X (No) with instant reactive feedback
- Dashboard shows upcoming commitments and events needing responses at a glance
- Mobile-optimized responsive design works seamlessly on phones, tablets, and desktops
- 30-day "remember me" sessions minimize login frequency

**For Super-Users (Joan + Delegates):**

- Event-by-event commitment reports showing: who's committed (Yes), who declined (No), who hasn't responded
- Make commitments on behalf of any user (batched email notifications prevent inbox spam)
- Password reset to temporary value with forced reset on next login
- Email change management with confirmation workflow
- User activation/deactivation and new user creation
- Mobile-accessible admin interface for on-the-go coordination

**For Everyone:**

- Address/contact directory (authenticated users only)
- Public event calendar (viewable by anyone, authenticated or not)
- Seamless data migration preserving all 60+ users, 65+ events, and historical commitments
- Deployed on Vercel with Postgres database (Neon) - zero monthly cost within free tier

**Technical Architecture:**

- Next.js 16+ with React for modern, maintainable codebase
- Vercel Postgres (0.5GB free tier) replacing file-based database
- Vercel Blob Storage (1GB free tier) for photos and media
- Supabase Auth for magic links and self-service password management
- PostgreSQL with proper timezone handling (Pacific Time)

### Key Differentiators

**1. Continuity Over Disruption:**
Unlike commercial tools requiring complete workflow changes, AFG Website preserves the proven commitment model that has served the ministry for 25 years while modernizing the technical foundation.

**2. Distributed Support Model:**
Super-user delegation empowers ministry coordinators (Joan and delegates) to handle password resets, commitment management, and user support - eliminating single-point-of-failure dependency on developer.

**3. Zero-Friction Mobile Experience:**
One-tap commitments with instant reactive feedback - no page reloads, no "Submit" buttons. Members complete their commitments in seconds from any device.

**4. Seamless Migration:**
Complete preservation of all user data, login credentials (via clean-slate password reset), events, and historical commitments - no data loss, no manual re-entry.

**5. Modern Stack, Zero Cost:**
Next.js/React deployment on Vercel with Postgres (Neon) and Blob Storage stays within free tiers indefinitely - no monthly costs for a volunteer ministry.

**6. Clean, Minimal, Modern Design:**
Visual overhaul from 1990s HTML to contemporary responsive UI with clean typography, intuitive navigation, and mobile-first approach.

---

## Target Users

### Primary Users

#### User Persona: Patricia "Pat" Anderson - Ministry Member

**Background:**
Pat is a 68-year-old alto in the Alleluia Folk Group who has been singing at Holy Family Parish for 15 years. She's retired, tech-savvy enough to use Facebook and online banking on her iPhone, but gets frustrated when websites don't work smoothly on mobile. She attends weekly Thursday evening practice and sings at 2-3 Masses per month.

**Current Experience:**

- Checks the AFG calendar 2-3 times per week, usually on her phone during breaks or while sitting at practice
- Has forgotten her password 3 times in the past year, each time requiring a call to Kayvan for reset
- Finds the current website difficult to navigate on mobile - has to zoom and scroll constantly
- Sometimes forgets to enter her commitments, then feels guilty when Joan asks who's coming

**Goals & Motivations:**

- Stay reliable and committed to the ministry she loves
- Quickly see what's coming up and confirm her availability
- Avoid being "that person" who forgets to respond
- Not bother Kayvan with tech support requests

**Success Vision:**
Pat pulls out her phone during practice break, taps the magic link from her email, sees 4 upcoming Masses that need responses, and taps the green checkmark on 3 of them and red X on one (she'll be out of town). Done in 15 seconds. No password to remember, no zooming, no "Submit" button - just instant confirmation that her commitments are recorded.

**"Aha!" Moment:**
"Wait, I'm already done? That was so easy! I don't even need to remember a password!"

---

#### User Persona: Joan Martinez - Ministry Coordinator & Super-User

**Background:**
Joan is a 62-year-old soprano who coordinates AFG scheduling and has been leading the group for 8 years. She's organized, detail-oriented, and deeply invested in making sure every Mass has enough musicians. She's comfortable with technology but values simplicity and speed.

**Current Experience:**

- Checks commitments 2-3 times per week, intensifying as event dates approach
- Gets frequent "I can't log in" calls/emails from members → has to redirect them to Kayvan
- Needs to know by Wednesday who's committed for Sunday Mass so she can follow up with non-responders
- Manually tracks who hasn't responded in a separate spreadsheet
- Sometimes prints commitment reports for planning purposes

**Goals & Motivations:**

- Ensure every Mass has adequate musical coverage
- Help members quickly without tech barriers
- Minimize last-minute scrambling for musicians
- Empower members to self-serve while being available when they need help

**Pain Points:**

- Can't help with password resets (creates bottleneck through Kayvan)
- Can't see at-a-glance who hasn't responded yet
- Desktop-only interface makes it hard to check commitments on her phone
- No ability to enter commitments for members who call/email her directly

**Success Vision:**
Joan opens the AFG website on her phone Wednesday morning and sees the upcoming Sunday 10am Mass. The interface shows: 8 committed (green), 2 declined (red), 4 no response yet (amber). She taps the 4 non-responders and makes commitments on their behalf based on a quick text exchange, then the system sends each person a single email confirmation. Done in 2 minutes.

**Super-User Capabilities She Values Most:**

1. Event-by-event commitment reports with clear visual status (committed/declined/pending)
2. Make commitments on behalf of others (with batched email notifications)
3. Password reset for members who call/email her directly
4. Add events to next year's calendar (annual planning task)
5. Mobile-accessible admin interface

**"Aha!" Moment:**
"I can actually help people myself now! I don't need to tell them to call Kayvan anymore!"

---

### Secondary Users

#### User Persona: Kayvan - Developer & System Administrator

**Background:**
You're the developer who built and maintains the AFG system, balancing ministry support with your professional work. You want the system to "just work" without constant intervention.

**Current Pain Points:**

- 6-12 password reset requests per year (5-10 minutes each via SSH and persondb.pl)
- Annual event calendar creation falls on you
- Any bug fix or feature request requires diving into legacy Perl/CGI code
- Single point of failure for all system administration

**Success Vision ("Zero Maintenance"):**
After launch, the system runs itself. Joan adds events to next year's calendar. Joan resets passwords. Members use magic links and never forget passwords. You receive zero support emails. You can focus on new features when YOU want to, not when support requests force you to.

**Admin Capabilities You Need:**

- View system health/metrics (optional nice-to-have)
- Manage super-user permissions (grant/revoke Joan's access or add new super-users)
- Database backup/export capabilities
- Emergency override access if needed

**"Aha!" Moment:**
"It's been 3 months and I haven't gotten a single support email. Joan is handling everything. This is amazing."

---

### User Journey

**Discovery & Onboarding (Launch Day):**

1. **Email Announcement:** All 60+ members receive clear launch email from Joan/Kayvan explaining the new system, password reset requirement, and magic link authentication
2. **First Login:** Members click magic link in email → automatically logged in → see dashboard with upcoming events
3. **First Commitment:** One-tap green checkmark or red X → instant confirmation → "Wow, that was easy!"
4. **Remember Me:** System remembers them for 30 days → no login required for next 2-3 weeks

**Weekly Practice Integration:**

- Thursday evening practice → Members pull out phones during break
- Check upcoming events → Make commitments in seconds
- Organic peer support: "How do I do this?" → "Just tap the green checkmark!"

**Joan's Weekly Workflow:**

1. **Tuesday/Wednesday:** Check event-by-event reports for Sunday Mass
2. **Identify non-responders:** See amber/pending status at a glance
3. **Follow up:** Text/call non-responders → Make commitments on their behalf
4. **Verify coverage:** Green checkmarks show adequate musicians for each role
5. **Optional print:** Print report if needed for practice or planning

**Long-term Routine:**

- Members check 2-3 times per week, commitments become habitual
- Joan's coordination becomes proactive rather than reactive
- Kayvan receives zero support emails, system fades into reliable infrastructure
- Annual event planning: Joan adds next year's calendar herself

**Value Realization Timeline:**

- **Week 1:** Members discover magic links eliminate password frustration
- **Week 2:** Joan experiences first "I can help you myself" moment with password reset
- **Month 1:** Kayvan realizes he hasn't gotten a support email in weeks
- **Month 3:** System becomes invisible infrastructure - everyone just uses it naturally

---

## Success Metrics

Success for AFG Website is measured across three dimensions: eliminating support burden, enabling coordination effectiveness, and ensuring member engagement. Since this is a volunteer ministry (not a commercial product), success focuses on operational efficiency and user satisfaction rather than revenue metrics.

### User Success Metrics

**Member Adoption & Engagement:**

- **Initial Adoption:** 90%+ of active members (54+ of 60) successfully log in within first week of launch
- **Sustained Usage:** 80%+ of members check commitments 2-3 times per week consistently
- **Commitment Entry Speed:** Average commitment entry time ≤ 30 seconds from login to confirmation
- **Password-Free Experience:** 95%+ of logins via magic links (vs. manual password entry)
- **Mobile Adoption:** 70%+ of sessions from mobile devices (reflecting Thursday practice usage pattern)

**Coordinator Effectiveness:**

- **Joan's Self-Service Success:** 100% of password resets and user management handled without Kayvan involvement
- **Commitment Visibility:** Joan can identify non-responders within 10 seconds of viewing event report
- **Proxy Commitment Speed:** Joan completes commitments for 4 members in < 2 minutes
- **Annual Planning Independence:** Joan adds next year's calendar without technical assistance
- **Mobile Coordination:** 60%+ of Joan's admin tasks performed on mobile device

**Developer Liberation:**

- **Zero Support Burden:** 0 password reset requests to Kayvan after Month 1
- **System Stability:** 99.9%+ uptime (leveraging Vercel's infrastructure reliability)
- **Maintenance Time:** < 1 hour/month on system maintenance (vs. current 2-3 hours/month)
- **Feature Development Freedom:** Ability to add features proactively vs. reactively responding to support requests

### Business Objectives

#### Primary Objective: Eliminate Support Bottleneck

- **Current State:** 6-12 password resets/year × 5-10 minutes each = 60-120 minutes annual support burden
- **Target State:** 0 support requests by Month 3
- **Success Indicator:** 3 consecutive months with zero support emails/calls to Kayvan

#### Secondary Objective: Enable Distributed Ministry Coordination

- **Current State:** All admin tasks (password resets, event creation, user management) require Kayvan intervention
- **Target State:** Joan handles 100% of routine admin tasks independently
- **Success Indicator:** Annual event calendar added by Joan without Kayvan involvement

#### Tertiary Objective: Improve Member Experience

- **Current State:** Mobile-hostile interface, frequent password resets, confusion about commitments
- **Target State:** Mobile-first experience with one-tap commitments and zero password friction
- **Success Indicator:** Zero complaints about password issues or mobile usability in first 3 months

### Key Performance Indicators

**Launch Success (First 30 Days):**

- 90%+ member adoption rate (54+ of 60 members successfully log in)
- 0 password reset requests to Kayvan
- Joan successfully resets 3+ passwords for members independently
- 70%+ mobile usage rate during Thursday practice sessions
- Average commitment entry time < 30 seconds

**Operational Success (3 Months Post-Launch):**

- 100% of password resets handled by Joan (zero to Kayvan)
- 100% of annual event planning handled by Joan
- 80%+ sustained member engagement (check commitments 2-3× weekly)
- 95%+ magic link authentication rate (vs. password-based login)
- < 1 hour/month maintenance time for Kayvan

**Long-Term Success (6-12 Months):**

- System operates as "invisible infrastructure" - no support requests for 6+ consecutive months
- Joan proactively coordinates without technical barriers
- Members habitually check commitments 2-3× weekly without prompting
- Zero migration-related data issues or complaints
- $0/month hosting costs (within Vercel/Supabase free tiers)

**Red Flags (Failure Indicators):**

- > 3 password reset requests to Kayvan in any given month
- < 70% member adoption after 30 days
- Joan requests Kayvan assistance for routine admin tasks
- > 5% of members complain about mobile usability
- Average commitment entry time > 60 seconds

---

## MVP Scope

### Core Features

**Authentication & User Management:**

- Magic link authentication (primary login method)
- Optional password authentication (for convenience)
- 30-day "remember me" session tokens
- Self-service password reset via magic links
- User profile management (email, contact info)

**Commitment Management (Members):**

- Dashboard showing:
  - Upcoming events requiring commitment decisions
  - Events user has committed to (Yes)
  - Events user has declined (No)
- One-tap commitment UI:
  - Green checkmark = Yes (committed)
  - Red X = No (declined)
  - Instant reactive feedback (no "Submit" button)
- Event calendar view (all upcoming events)
- Mobile-optimized responsive design

**Super-User Admin Interface (Joan + Delegates):**

- Event-by-event commitment reports showing:
  - Who's committed (green/Yes)
  - Who's declined (red/No)
  - Who hasn't responded (amber/pending)
- Make commitments on behalf of any user
- Password reset to temporary value (with forced reset on next login)
- Email change management with confirmation workflow
- User activation/deactivation (mark users as inactive/active)
- Add new users to the system
- Mobile-accessible admin interface

**Address Directory:**

- Contact information for all members (authenticated users only)
- Phone numbers, addresses, birthday, notes
- Searchable/filterable member list

**Public Event Calendar:**

- Viewable by anyone (authenticated or not)
- Shows upcoming Masses, practices, and events
- Event details: description, location, event time, "arrive by" time

**Data Migration:**

- Complete migration of all 60+ users with:
  - Login credentials (clean-slate password reset required)
  - Full names, contact info, admin flags
  - All current/future events (65+ events)
  - All historical commitments per person
- Preserve original `login` field for commitment matching
- Convert admin_level (0/1) to boolean
- Force UTF-8 character encoding
- Preserve timezone metadata (Pacific Time)

**Event Management:**

- Display all current and future events (no past events shown)
- Soft delete approach: Mark old events as `archived: true`, filter queries to show only `archived: false` events
  - Future consideration: Re-evaluate if join table becomes unwieldy and hard delete with cleanup becomes necessary
- Event details: description, location, event_time, arrive_by, timezone

**Technical Foundation:**

- Next.js 16+ with React
- Vercel Postgres (Neon) - 0.5GB free tier
- Vercel Blob Storage (1GB free tier) for photos/media
- Supabase Auth for magic links and password management
- PostgreSQL with proper timezone handling (Pacific Time)
- Deployed on Vercel (zero monthly cost within free tiers)

---

### Out of Scope for MVP

**Deferred to Post-MVP (v1.1+):**

**Email Notifications:**

- Batched email confirmations when super-user makes commitments on behalf of users
- Event reminder emails
- New event announcements
- Commitment deadline reminders

**Event Creation/Editing by Super-Users:**

- Joan adding events to next year's calendar
- Modifying existing event details (time, location, description)
- Deleting/canceling events
- Bulk event import for annual planning

**Advanced Reporting:**

- Export commitment reports to PDF/CSV
- Historical participation analytics
- Attendance trends and statistics
- Member engagement metrics dashboard

**Enhanced Member Features:**

- Personal notes on events
- Recurring commitment preferences
- Notification preferences
- Mobile app (PWA only for MVP)

**Advanced Admin Features:**

- Role-based permissions (multiple super-user levels)
- Audit logs for admin actions
- Bulk user operations
- Custom event categories/types

**Photo Gallery:**

- Existing `pix/` directory migration
- Photo upload and management
- Event photo albums

---

### MVP Success Criteria

**Launch Success (First 30 Days):**

- 90%+ member adoption rate (54+ of 60 members successfully log in)
- 0 password reset requests to Kayvan
- Joan successfully resets 3+ passwords independently
- 70%+ mobile usage rate during Thursday practice
- Average commitment entry time < 30 seconds
- Zero migration-related data loss or errors

**Validation Criteria:**

- All 60+ users migrated with correct data
- All 65+ current/future events migrated with commitments intact
- Magic link authentication working reliably (< 30 second delivery)
- Super-user admin functions working without Kayvan assistance
- Mobile UI usable on phones (no zoom/scroll issues)
- Public calendar accessible to non-authenticated visitors

**Go/No-Go Decision Points:**

- If < 70% adoption after 30 days → investigate barriers, provide additional support
- If > 3 password reset requests to Kayvan in Month 1 → magic links aren't working, need adjustment
- If Joan requests Kayvan help for routine admin → super-user interface needs improvement
- If average commitment time > 60 seconds → UI needs simplification

---

### Future Vision

**Version 1.1 (3-6 Months Post-Launch):**

- Email notification system (batched confirmations, event reminders)
- Super-user event creation/editing capabilities
- Joan adds annual calendar without Kayvan involvement
- Export/print functionality for commitment reports

**Version 1.2 (6-12 Months):**

- Photo gallery migration and management
- Advanced reporting and analytics
- Recurring commitment preferences
- Enhanced mobile experience (PWA optimization)

**Version 2.0 (12+ Months):**

- Multi-ministry support (expand beyond AFG to other parish groups)
- Role-based permissions for different coordinator levels
- Integration with parish calendar systems
- API for third-party integrations (e.g., parish management software)

**Long-Term Vision (2-3 Years):**

If wildly successful, AFG Website could become a **parish-wide ministry coordination platform**:

- Support multiple ministries (AFG, Eucharistic Ministers, Lectors, Ushers, etc.)
- Unified calendar across all parish activities
- Cross-ministry scheduling and conflict detection
- Parish-wide communication and announcement system
- White-label offering for other parishes seeking similar solutions

**Key Expansion Opportunities:**

- Other music ministries at different parishes
- Multi-parish diocese-level coordination
- SaaS offering for Catholic parishes nationwide
- Integration with existing parish management systems (ParishSoft, eCatholic)

**Guiding Principle:**

The MVP proves the distributed support model works and eliminates the single-developer bottleneck. Future versions build on this foundation to scale ministry coordination across broader contexts while maintaining the simplicity and mobile-first experience that makes it successful.

---
