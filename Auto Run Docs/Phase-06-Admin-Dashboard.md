# Phase 06: Admin Dashboard

This phase creates a dedicated admin interface for the super-user (Joan) to manage events, view all commitments, and access ministry membership information.

## Tasks

- [ ] Create src/app/admin/page.tsx page that checks user is_admin property and redirects to home if not authorized
- [ ] Create src/lib/auth.ts helper function requireAdmin() that throws error if current user is not admin
- [ ] Update src/middleware.ts to protect /admin routes with admin-only access
- [ ] Create src/app/admin/events/page.tsx page listing all events with "Create Event" button
- [ ] Create src/app/api/events/route.ts GET endpoint returning all events and POST endpoint accepting { title, description, event_date, location } to create new event
- [ ] Create src/components/CreateEventForm.tsx form with fields for title, description, date, time, location and submit button
- [ ] Update src/app/admin/events/page.tsx to render CreateEventForm and list of existing events with delete option
- [ ] Create src/app/api/events/[id]/route.ts DELETE endpoint to remove events by ID
- [ ] Create src/app/admin/commitments/page.tsx page showing all commitments grouped by event with user names and statuses
- [ ] Update src/lib/db.ts to add getAllCommitmentsWithDetails() query returning commitments joined with users and events
- [ ] Add "Admin" link to Header.tsx navigation that only displays when user is_admin is true
- [ ] Style admin pages with clear section headers, card layouts, and action buttons using AFG brand colors
- [ ] Test admin functionality by logging in as Joan (admin user) and creating a new event, then viewing commitments page
