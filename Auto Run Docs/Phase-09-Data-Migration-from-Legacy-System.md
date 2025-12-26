# Phase 09: Data Migration from Legacy System

This phase migrates all existing data (60+ users, 65+ events, historical commitments) from the Perl/CGI flat-file database to the new Vercel Postgres database.

## Tasks

- [ ] Examine docs/reference/old_cgi_site/commitment/save/ directory to understand existing database format
- [ ] Read docs/reference/old_cgi_site/commitment/modules/Person.pm to understand user data structure
- [ ] Read docs/reference/old_cgi_site/commitment/modules/Event.pm to understand event data structure
- [ ] Create src/migration/parseLegacyData.ts utility function to read .db files and parse flat-file format
- [ ] Create src/migration/migrateUsers.ts script that reads persons.db and converts to user records in PostgreSQL
- [ ] Create src/migration/migrateEvents.ts script that reads events.db and converts to event records with proper date formatting
- [ ] Create src/migration/migrateCommitments.ts script that reads commitment data and links users to events with status
- [ ] Create src/migration/runMigration.ts main script that executes all migration scripts in order
- [ ] Add npm script to package.json: "db:migrate": "tsx src/migration/runMigration.ts" for running migrations
- [ ] Test migration by running npm run db:migrate on staging environment and verifying data counts match original (users ~60+, events ~65+)
- [ ] Create verification script src/migration/verifyMigration.ts that compares counts between old and new systems
- [ ] Run npm run db:migrate to complete migration and verify all records are transferred correctly
