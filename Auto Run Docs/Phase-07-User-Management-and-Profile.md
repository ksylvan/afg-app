# Phase 07: User Management and Profile

This phase adds user profile functionality allowing authenticated members to view and update their contact information, and provides admin tools for managing the ministry member list.

## Tasks

- [ ] Create src/app/profile/page.tsx page displaying user's name, email, and phone number
- [ ] Create src/components/ProfileForm.tsx form with editable fields for name, email, and phone number
- [ ] Create src/app/api/users/[id]/route.ts PUT endpoint accepting { name, email, phone } to update user profile
- [ ] Update src/lib/db.ts to add getUserById(userId), updateUserProfile(userId, data), and getAllUsers() functions
- [ ] Update ProfileForm.tsx to fetch current user data on mount and handle form submission to update profile
- [ ] Add "Profile" link to Header.tsx navigation that only shows when user is authenticated
- [ ] Create src/app/admin/users/page.tsx page listing all ministry members with name, email, phone, and join date
- [ ] Add "Add Member" button to src/app/admin/users/page.tsx that opens CreateEventForm-like modal for new users
- [ ] Create src/app/api/users/route.ts POST endpoint accepting { name, email, phone, is_admin } to create new user
- [ ] Add email validation to ProfileForm.tsx and user creation forms using simple regex pattern
- [ ] Style profile page with clear section headers, large form inputs, and save button
- [ ] Test profile updates by modifying name and phone, then verify changes persist and display on page refresh
