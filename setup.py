__author__ = "YANG Zhenfei"
__copyright__ = "Copyright (C) 2018 Ghislain Bourgeois"
__license__ = "GNU GPLv2"

import setuptools
from setuptools import find_packages


setuptools.setup(
    name="monthly_expenses",
    version="0.5",
    packages=find_packages(),
    package_data={'monthly_expenses.templates': ['*.html']},
    setup_requires=['pytest-runner'],
    install_requires=['beancount>=2.1.2', 'tabulate', 'pandas', 'fava'],
    tests_require=['pytest', 'testfixtures'],

    test_suite="tests",

    author="YANG Zhenfei",
    author_email="yangzhenfei0@gmail.com",
    description="Beancount monthly expenses report",
    license="GPLv2",
    keywords="beancount monthly expenses report",
    url="https://github.com/dvorak0/fava-monthly-expenses/",
    include_package_data=True,

    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "Topic :: Office/Business :: Financial",
        "Topic :: Office/Business :: Financial :: Accounting",
        "Topic :: Office/Business :: Financial :: Investment",
        ),
    )
