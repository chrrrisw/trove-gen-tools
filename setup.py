from setuptools import setup, find_packages

# RST formatted text
with open("README.rst", "r") as fh:
    long_description = fh.read()

classifiers = [
    "Development Status :: 4 - Beta",
    "Environment :: Console",
    "Environment :: Web Environment",
    "Framework :: AsyncIO",
    "Intended Audience :: Developers",
    "Intended Audience :: End Users/Desktop",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Topic :: Database :: Front-Ends",
    "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    "Topic :: Sociology :: Genealogy",
]

keywords = ["Trove", "National Library of Australia", "Genealogy"]

setup(
    name="trove_gen_tools",
    version="0.1.2",
    description="Collection of tools for genealogy research on NLA Trove.",
    long_description=long_description,
    keywords=keywords,
    classifiers=classifiers,
    url="https://github.com/chrrrisw/trove-gen-tools",
    author="Chris Willoughby",
    author_email="chrrrisw@gmail.com",
    license="MIT",
    packages=find_packages("."),
    package_data={"trveval": ["static/*.js", "static/*.css", "templates/*.html"]},
    include_package_data=True,
    install_requires=[
        "aiohttp",
        "jinja2",
        "pandas",
        "requests",
        "sqlalchemy",
        "xlrd",
        "xlsxwriter",
    ],
    python_requires=">3.5.3",
    entry_points={
        "console_scripts": [
            "trveval=trveval.__main__:main",
            "trvcoll=trvcoll.__main__:main",
            "trv2xl=trvartdb.articlecsv:export_db_as_xlsx",
            "trv2csv=trvartdb.articlecsv:export_db_as_csv",
        ],
        "gui_scripts": [],
    },
)
