# Phase 05: One-Tap Commitment Tracking

This phase implements the core feature: authenticated users can view events and tap Yes/No buttons to record their commitment, optimized for mobile with large touch targets for elderly users.

## Tasks

- [ ] Update src/lib/db.ts to add query functions: getCommitmentsForUser(userId), getCommitmentForUserEvent(userId, eventId), upsertCommitment(userId, eventId, status)
- [ ] Create src/app/api/commitments/route.ts POST endpoint that accepts { userId, eventId, status } and calls upsertCommitment
- [ ] Update EventCard.tsx to accept optional userId prop and show "Sign in to RSVP" message when not authenticated
- [ ] Create src/components/CommitmentButtons.tsx component with two large buttons: "Yes - I'll be there" (green) and "No - Can't make it" (red)
- [ ] Update EventCard.tsx to include CommitmentButtons component below event details when user is authenticated
- [ ] Update CommitmentButtons.tsx to fetch current commitment status on mount and highlight the selected button
- [ ] Add useState and useEffect to CommitmentButtons.tsx to manage loading state and commitment status
- [ ] Add onClick handlers to Yes/No buttons that call /api/commitments endpoint with appropriate status
- [ ] Style CommitmentButtons.tsx with button width at least 140px, height at least 60px, large text (18px minimum) for easy tapping
- [ ] Update src/lib/types.ts to add CommitmentStatus type with "yes", "no", "pending" values
- [ ] Test by logging in as admin user and tapping Yes/No buttons to verify commitment updates correctly and persists
