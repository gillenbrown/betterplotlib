from setuptools import setup, find_packages

setup(
	name="betterplotlib",

	version="0.2.1",

	description="Some wrappers for matplotlib to make plotting easier and nicer.",
	long_description="This module contains wrapper functions for matplotlib. A lot of the matplotlib plots are ugly and not easy to make, so I wrote some functions that do a lot of the stuff that should be easy, as well as wrappers for common plots that make them look nicer. ",

	url="http://betterplotlib.readthedocs.io/en/latest/",

	author="Gillen Brown",
	author_email="gillenbrown@gmail.com",

	license="MIT",

	keywords="plotting matplotlib",

	packages=find_packages(exclude=["docs"]),

	install_requires=["matplotlib",  "numpy",  "palettable"]

	)
