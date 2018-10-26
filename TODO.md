# TODO

## Version 0.1.3

- [ ] Packaging (including console scripts)
- [ ] Deployment to PyPi
- [ ] Command line help
- [ ] Web help
- [x] Icon

### Assessment

- [x] Allow assessment based on date
- [x] Finished message

### Articles

- [x] Off-site article link
- [ ] Remove sidebar stuff

### Export tools

- [x] CSV export

### Import tools

- [x] CSV import



## Version 0.1.4

- [ ] Websocket connection status on all pages (include tooltip).
- [ ] Reconnection for websocket
- [ ] GitHub pages

### Collector

- [ ] Add whether you have corrected the article
- [ ] Web interface for collector

### Assessment

- [ ] Tidy article_id in form (e.g. hidden)
- [ ] Allow single article assessment
- [ ] Previously associated people are not shown on the assessment page

### Articles

- [ ] Re-evaluation (undo)
- [ ] Modify people
- [ ] Notes for articles

### People

- [ ] Add/delete/modify people in page
  - [ ] Add person
  - [ ] Delete person

### Queries

- [ ] Add/delete/modify states in page

### Export tools

- [ ] Export only relevant

### Import tools

- [ ] Import person from XLSX converts "" to NaN

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

- [ ] Web interface for DB modification
- [ ] Full details sidebar


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
