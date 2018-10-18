# TODO

## Version 0.1.3

- [ ] Packaging (including console scripts)
- [ ] Deployment to PyPi
- [ ] CSV import/export
- [ ] Command line help
- [ ] Web help

### Assessment

- [x] Allow assessment based on date
- [ ] Finished message

## Version 0.1.4

- [ ] Icon
- [ ] Websocket connection status on all pages.
- [ ] Reconnection for websocket

### Assessment

- [ ] Tidy article_id in form (e.g. hidden)
- [ ] Allow single article assessment
- [ ] Previously associated people are not shown on the assessment page

### Collector

- [ ] Add whether you have corrected the article
- [ ] Web interface for collector

### People

- [ ] Add/delete/modify people in page
  - [ ] Add person
  - [ ] Delete person

### Merge tool

- [ ] Merge tool for relevant articles

## Later versions

- [ ] Multiple connections (aiosqlite, sqlalchemy_aio)
- [ ] DB migration scripts
- [ ] Schema versioning
- [ ] Full text retrieval
- [ ] Electron app?
- [ ] Windows/Mac instructions
- [ ] Increase container width restriction.
- [ ] Semantic theme for wider screens
- [ ] Allow deletion of associated people (assessment and article page)











### Articles

- [ ] Re-evaluation (undo)
- [ ] Web interface for DB modification
- [ ] Modify people
- [ ] Notes for articles
- [ ] Off-site article link
- [ ] Full details sidebar

### Queries

- [ ] Show states in page
- [ ] Add/delete/modify tables in page

### Export tools

- [ ] Export only relevant
- [ ] CSV export
- [ ] CSV import

### Import tools

- [ ] Import person from XLSX converts "" to NaN

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
