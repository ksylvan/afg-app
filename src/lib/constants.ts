export const SITE_TITLE = 'Alleluia Folk Group';

export const SITE_CONFIG = {
  title: SITE_TITLE,
  description: 'Serving Holy Family Parish through the gift of music',
  contactEmail: 'info@alleluiafolkgroup.org',
  parish: 'Holy Family Parish',
  minYear: 2025,
} as const;

export const AFG_COLORS = {
  blue900: '#1e3a8a',
  blue800: '#1e40af',
  amber600: '#d97706',
  amber500: '#f59e0b',
  amber400: '#fbbf24',
  amber300: '#fcd34d',
} as const;

export const NAV_LINKS = [
  { name: 'Home', path: '/' },
  { name: 'Events', path: '/events' },
  { name: 'Calendar', path: '/calendar' },
  { name: 'About', path: '/about' },
] as const;
