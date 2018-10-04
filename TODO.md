# TODO

- [ ] Packaging (including console scripts)
- [ ] CSV import/export
- [ ] Multiple connections (aiosqlite, sqlalchemy_aio)
- [ ] DB migration scripts
- [ ] Schema versioning
- [ ] Merge tool for relevant articles
- [ ] Full text retrieval

## Collector

- [x] Remove assessment from collector
- [ ] Newspaper titles (including limiting search)
- [ ] State (including limiting search)
- [x] Use query and years tables for re-run (allow modification on cli)
- [ ] Update article info after correction on Trove

## Assessment

- [x] Allow specification of highlights from file
- [ ] Use highlights table for highlights
- [ ] Tidy article_id in form (e.g. hidden)
- [x] Catch form re-submission
- [x] Add people to articles
- [x] Link people table to articles
- [x] Stop people enter from submitting form

## Articles

- [ ] Re-evaluation (undo)
- [ ] Web interface for DB modification
- [ ] Show/modify people
- [ ] Notes for articles

## People

- [ ] Add/delete/modify people in page

## Queries

- [x] Add query table to DB
- [x] Add highlights table to DB
- [x] Add years table to DB
- [x] Show these in page
- [ ] Add/delete/modify these in page