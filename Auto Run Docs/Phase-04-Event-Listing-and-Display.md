# Phase 04: Event Listing and Display

This phase creates the public-facing event listing page that displays all ministry events in a clear, chronological format accessible to all ministry members.

## Tasks

- [ ] Create src/app/events/page.tsx page that fetches all events from database ordered by event_date ascending
- [ ] Create src/components/EventCard.tsx component displaying event title, formatted date (Month Day, Year), time, location, and optional description
- [ ] Create src/lib/utils.ts with formatDate and formatTime helper functions for consistent date/time display
- [ ] Update src/app/events/page.tsx to render events as a vertical list of EventCard components
- [ ] Add "Events" link to Header.tsx navigation menu
- [ ] Style EventCard.tsx with clean, readable design using AFG brand colors, large text suitable for elderly users, and sufficient padding
- [ ] Create src/app/events/layout.tsx with page title "Ministry Events" and meta description
- [ ] Update EventCard.tsx to show "No events scheduled" message when events array is empty
- [ ] Add CSS class for event cards with hover effect and subtle border using AFG gold color
- [ ] Test by running npm run dev and navigating to /events route to verify events display correctly with proper formatting
