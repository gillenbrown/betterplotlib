from setuptools import setup, find_packages

setup(
	name="betterplotlib",

	version="1.5.0",

	description="Some wrappers for matplotlib to make plotting easier and nicer.",
	long_description="This module contains wrapper functions for matplotlib. A lot of the matplotlib plots are ugly and not easy to make, so I wrote some functions that do a lot of the stuff that should be easy, as well as wrappers for common plots that make them look nicer. ",

	url="http://betterplotlib.readthedocs.io/en/master/",

	author="Gillen Brown",
	author_email="gillenbrown@gmail.com",

	license="MIT",

	keywords="plotting matplotlib",

	include_package_data=True,

	install_requires=["matplotlib",
					  "numpy",
					  "palettable",
					  "pytest>=3.3",
					  "imageio",
					  "scipy",
					  "numpy",
					  "cycler",
					  "astropy"
					  ]

	)
