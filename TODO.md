# TODO

- [ ] Packaging (including console scripts)
- [ ] Deployment to PyPi
- [ ] CSV import/export
- [ ] Multiple connections (aiosqlite, sqlalchemy_aio)
- [ ] DB migration scripts
- [ ] Schema versioning
- [ ] Full text retrieval
- [ ] Websocket connection status on all pages.
- [ ] Icon
- [ ] Electron app?
- [ ] Windows/Mac instructions
- [ ] Command line help
- [ ] Web help
- [ ] Reconnection for websocket
- [ ] Increase container width restriction.

## Collector

- [ ] Newspaper titles (including limiting search)
- [ ] Update article info after correction on Trove
- [x] Add article correction count
- [ ] Add whether you have corrected the article
- [x] Add article word count
- [x] Illustrated flag
- [ ] Web interface for collector

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
- [ ] Finished message

## Articles

- [ ] Re-evaluation (undo)
- [ ] Web interface for DB modification
- [x] Show people
- [ ] Modify people
- [x] Show matched queries
- [ ] Notes for articles
- [ ] Off-site article link
- [ ] Full details sidebar

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

## Merge tool

- [ ] Merge tool for relevant articles

## Web App

The web application is a thought experiment at this time. It should be hosted
somewhere and allow users to load and save databases on their local disk. All
functionality should be client-side (in the browser) so that all information is
private.

Technologies of interest:

- http://aaronpowell.github.io/db.js/
- https://github.com/kripken/sql.js
- https://pouchdb.com/
- https://developer.mozilla.org/en-US/docs/Web/API/File/Using_files_from_web_applications

- [ ] Create web application version
  - [ ] Load/save to local disk
  - [ ] Use IndexedDB for in-session functionality?
  - [ ] Should match functionality of trvcoll/trveval etc above
  - [ ] Databases should be shareable between python and web versions
