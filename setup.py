from setuptools import setup, find_packages

setup(
    name="trove_gen_tools",
    version="0.1",
    description="Collection of tools for genealogy research on NLA Trove.",
    url="https://github.com/chrrrisw/trove-gen-tools",
    author="Chris Willoughby",
    author_email="",
    license="MIT",
    packages=find_packages("."),
    include_package_data=True,
    install_requires=["aiohttp", "sqlalchemy"],
    entry_points={
        "console_scripts": [
            "trveval=trveval.__main__:main",
            "trvcoll=trvcoll.__main__:main",
        ]
    },
)
