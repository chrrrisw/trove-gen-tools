

===============
trove-gen-tools
===============

Some tools to help with searching NLA Trove newspapers for genealogy purposes.

Can be used to keep a track of searches on any subject.

The basic work flow is:

- run the collector to search for people (subjects) mentioned in newpaper articles
- assess those articles for relevance and assign people (subjects) to them
- some time passes
- run the collector and assessment tools again to pick up any new articles added to Trove

Requires:

- Python > 3.5.3
- aiohttp
- jinja2
- numpy
- pandas
- requests
- sqlalchemy
- xlrd
- xlsxwriter

Mostly beta, but useable.

Getting a Trove API key
=======================

The collection tool uses the Trove API, which requires each user to have an API key.

You can request an API key by following the instructions `here
<http://help.nla.gov.au/trove/building-with-trove/api>`_.

trvartdb
========

The Trove Newspaper Article database package.

Contains some command line tools for importing and exporting the database.

trv2xl
------

Converts the database to an Excel (.xlxs) file.

.. code-block:: shell

    trv2xl my_database.db my_database.xlsx

xl2trv
------

Converts an Excel (.xlsx) file to a database.

.. code-block:: shell

    xl2trv my_database.xlsx my_new_database.db

This tool reconstructs a database from the sheets in the Excel workbook. As such,
the sheet names should match the tables required by the database. Modifications
to the spreadsheet should be picked up, but any additional columns will not be.

This will not (currently) overwrite an existing database.

trv2csv
-------

Converts the database to a group of CSV files.

.. code-block:: shell

    trv2csv my_database.db my_database

will produce a number of CSV files with names starting with ``my_database``. One
database table per file.

csv2trv
-------

Converts a group of CSV files to a database.

.. code-block:: shell

    csv2trv my_database my_new_database.db

will reconstruct a database from the group of CSV files with names starting
with ``my_database``. As such, the csv names should match the tables required
by the database. Modifications to the CSV files should be picked up,
but any additional columns will not be.

This will not (currently) overwrite an existing database.

trvcoll
=======

Collects articles returned from a list of search terms.

When creating a new database, a text file containing search queries is required 
on the command line (using the ``-q`` option). If you run ``trvcoll`` again on 
a pre-existing database the previous search queries will be read from the 
database and used again. You can add new search queries to a pre-existing 
database by specifying the ``-q`` option again.

Similarly, when creating a new database, a range of years must be specified on 
the command line (using the ``--start`` and ``--end`` options). If you 
run ``trvcoll`` again on a pre-existing database the previous year range will 
be read from the database and used again. You can add new year ranges to a 
pre-existing database by specifying the ``--start`` and ``--end`` options again.

The ``--states`` and ``--titles`` options (defaults to all states and titles) 
are also stored and reused on re-query (as above).

Create a file that contains your search terms (one per line). It should look 
something like this:

.. code-block:: text

    "william willoughby"~1
    "wm willoughby"~1
    willoughby+blacksmith

Let's call this one ``willoughbys.txt``.

The search query format for Trove is detailed `here
<http://help.nla.gov.au/trove/about-trove/searching-guide>`_.

Once you have your API key, you can run the collector like so:

.. code-block:: shell

    trvcoll --start 1860 --end 1865 -q willoughbys.txt --state sa your-api-key willoughbys.db

Obviously, replace ``your-api-key`` in the command above with the one you were 
issued.

This will create a sqlite3 database named ``willoughbys.db`` and populate it 
with every article from South Australian newspapers that contain any of the 
search terms in ``willoughbys.txt`` between the years ``1860`` and ``1865``.

The database can then be used by the evaluation tool described below.

Help is available by typing ``trvcoll -h``

trveval
=======

Allows you to evaluate the collected articles for relevance.

Given a database file name this tool will start a web server that 
allows you to step through every article and assess them for relevance to your
research:

.. code-block:: shell

    trveval willoughbys.db
    ======== Running on http://127.0.0.1:5000 ========
    (Press CTRL+C to quit)

If you then bring up the given URL ``http://127.0.0.1:5000`` in your browser you 
should see the first article in the Trove newspaper interface with some extra 
controls at the top of the page.

These controls are:

- ``Skip`` (go to the next article without making any changes to the database)
- ``Relevant`` (mark this article as assessed and relevant to your research and go to the next article)
- ``Not Relevant`` (mark this article as assessed and not relevant to your research and go to the next article)
- ``People`` (link this article to one or more people that you are researching)
- Some buttons to navigate to other pages to manage the database.

The ``People`` dropdown allows you to add new people, as well as search for 
existing people in the database. When you first start the assessment cycle, 
there won't be any people in the database. Separate the entries in this dropdown 
by pressing the ``enter`` key.

The other pages have brief descriptions of their functionality on each page.

You can stop assessment at any time by killing the process. When you run it again,
only those articles that you have not assessed will be available on the assessment
page.

Al full list of all articles in the database is available on the ``articles``
page, and you can modify the ``chk`` (checked/assessed) and ``rel`` (relevant)
flags here. If you want to go back and re-evaluate an article, this currently
requires you to un-check the ``chk`` tick box and re-start the process. Be aware
that previously associated people (subjects) are currently not shown in the
assessment page - to be fixed in a future release.


Development install
===================

A python ``venv`` is useful to avoid dependency clashes with others, but not necessary.

Linux
-----

.. code-block:: shell

    git clone https://github.com/chrrrisw/trove-gen-tools.git
    cd trove-gen-tools
    pip install -e .

Windows
-------

Help needed.

Mac
---

Help needed.

Full install
============

A python ``venv`` is useful to avoid dependency clashes with others, but not necessary.

Linux
-----

.. code-block:: shell

	pip install trove-gen-tools

Windows
-------

Help needed.

Mac
---

Help needed.
