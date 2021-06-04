#!/usr/bin/env python
# -*- coding: utf-8 -*-

import setuptools
import versioneer


with open('README.md', 'r') as fh:
    long_description = fh.read()


setuptools.setup(
    name='cf-index-meta',
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    author='Lars Bärring, Klaus Zimmermann',
    author_email='lars.barring@smhi.se, klaus.zimmermann@smhi.se',
    description='Climate index metadata',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/clix-meta/clix-meta',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'License :: OSI Approved :: MIT License',
        'Environment :: Console',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Science/Research',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: GIS',
    ],
    packages=setuptools.find_packages(),
    package_data={
        'ci_meta.exporter': ['templates/*.yml'],
    },
    python_requires='>=3.8',
    install_requires=[
        'PyYAML',
        'regex',
        'sentry-sdk',
        'pyexcel',
        'pyexcel-xls',
        'jinja2',
    ],
    entry_points={
        'console_scripts': [
            'ci-meta-exporter=ci_meta.exporter:main',
        ],
    },
    project_urls={
        'Bug Reports':
        'https://github.com/clix-meta/clix-meta/issues',
        'Source': 'https://github.com/clix-meta/clix-meta',
    },
)
