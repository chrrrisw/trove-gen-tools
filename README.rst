===============
trove-gen-tools
===============

Some tools to help with searching NLA Trove newspapers for genealogy purposes.

The basic work flow is:

- run the collector to search for people mentioned in newpaper articles
- assess those articles for relevance and assign people to them
- some time passes
- run the collector and assessment tools again to pick up any new articles added to trove

Requires Python 3 with ``aiohttp``, ``jinja2``, ``requests``, and ``sqlalchemy``.

Mostly alpha, but useable.

trvartdb
========

The Trove Newspaper Article database package. This is a utility package and has no command line tools.

trvcoll
=======

Collects articles returned from a list of search terms.

Create a file that contains your search terms (one per line). It should look something like this:

.. code-block:: text

    "william willoughby"~1
    "wm willoughby"~1
    willoughby+blacksmith

Let's call this one ``willoughbys.txt``

Request an API key by following the instructions `here<http://help.nla.gov.au/trove/building-with-trove/api>`_.

Once you have your API key, you can run the collector like so:

.. code-block:: shell

    trvcoll --start 1860 --end 1865 -q willoughbys.txt --state sa your-api-key willoughbys.db

This will create a sqlite3 database named ``willoughbys.db`` and populate it with every article from South Australian newspapers that contain any of the search terms in ``willoughbys.txt`` between the years ``1860`` and ``1865``.

The database can then be used by the evaluation tool described below.

Help is available by typing ``trvcoll -h``

trveval
=======

Allows you to evaluate the collected articles for relevance.

Given the database ``willoughbys.db`` this tool will start a web server that allows you to step through every article and assess them for relevance to your research:

.. code-block:: shell

    trveval willoughbys.db
    ======== Running on http://127.0.0.1:5000 ========
    (Press CTRL+C to quit)

If you then bring up the given URL ``http://127.0.0.1:5000`` in your browser you should see the first article in the Trove newspaper interface with some extra controls at the top of the page.

These controls are:

- ``Skip`` (go to the next article without making any changes to the database)
- ``Relevant`` (mark this article as assessed and relevant to your research)
- ``Not Relevant`` (mark this article as assessed and not relevant to your research)
- ``People`` (link this article to one or more people that you are researching)
- Some buttons to navigate to other pages to manage the database.

The ``People`` dropdown allows you to add new people, as well as search for existing people in the database. When you first start the assessment cycle, there won't be any people in the database. Separate entries in this dropdown by pressing the ``enter`` key.

The other pages are minimally functional at this time.

Development install
===================

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

Linux
-----

Once I have this up on pypi:

.. code-block:: shell

	pip install trove-gen-tools

Windows
-------

Help needed.

Mac
---

Help needed.
