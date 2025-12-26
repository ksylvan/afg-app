# Phase 08: Mobile Polish and Accessibility

This phase optimizes the entire application for mobile use by elderly users, focusing on large touch targets, high contrast, and screen reader accessibility.

## Tasks

- [ ] Update src/app/globals.css to add responsive media query for mobile devices (max-width: 768px) with larger base font size (18px minimum)
- [ ] Update Header.tsx to create mobile hamburger menu that collapses navigation into dropdown on small screens
- [ ] Create src/components/MobileMenu.tsx component with slide-out panel and close button for mobile navigation
- [ ] Update all buttons across the application to have minimum 44px height for WCAG touch target compliance
- [ ] Update EventCard.tsx to use larger text sizes (20px for title, 18px for date/time) on mobile devices
- [ ] Update CommitmentButtons.tsx to stack Yes/No buttons vertically on mobile with 60px height each
- [ ] Increase line-height and letter-spacing across all text elements for better readability
- [ ] Add aria-label attributes to all interactive elements (buttons, links, form inputs)
- [ ] Add focus-visible styles to all buttons and links for keyboard navigation visibility
- [ ] Update form inputs to have minimum 20px font size to prevent iOS zoom on focus
- [ ] Add loading states to all API calls with clear visual feedback (spinner or "Saving..." text)
- [ ] Test mobile responsiveness by using browser dev tools to simulate iPhone and iPad viewports, verifying all elements are tappable and readable
