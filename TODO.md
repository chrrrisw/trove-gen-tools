# TODO

- [ ] Packaging (including console scripts)
- [ ] Deplyment to PyPi
- [ ] CSV import/export
- [ ] Multiple connections (aiosqlite, sqlalchemy_aio)
- [ ] DB migration scripts
- [ ] Schema versioning
- [ ] Merge tool for relevant articles
- [ ] Full text retrieval

## Collector

- [x] Remove assessment from collector
- [ ] Newspaper titles (including limiting search)
- [x] State (including limiting search)
- [x] Use query and years tables for re-run (allow modification on cli)
- [ ] Update article info after correction on Trove

## Assessment

- [x] Allow specification of highlights from file
- [x] Use highlights table for highlights
- [ ] Tidy article_id in form (e.g. hidden)
- [x] Catch form re-submission
- [x] Add people to articles
- [x] Link people table to articles
- [x] Stop people enter from submitting form
- [ ] Allow single article assessment
- [x] Allow assessment based on date

## Articles

- [ ] Re-evaluation (undo)
- [ ] Web interface for DB modification
- [ ] Show/modify people
- [ ] Notes for articles

## People

- [ ] Add/delete/modify people in page
  - [x] Date of birth
  - [x] Date of death
  - [x] Name
  - [ ] Add
  - [ ] Delete

## Queries

- [x] Add query table to DB
- [x] Add highlights table to DB
- [x] Add years table to DB
- [x] Show these in page
- [ ] Add/delete/modify these in page

## Export tools

- [ ] Export only relevant