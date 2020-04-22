#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import setuptools
import versioneer


readme_path = os.path.join(os.path.dirname(__file__), '..', 'README.md')
with open(readme_path, 'r') as fh:
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
    url='https://bitbucket.org/cf-index-meta/cf-index-meta',
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
        'https://bitbucket.org/cf-index-meta/cf-index-meta/issues',
        'Source': 'https://bitbucket.org/cf-index-meta/cf-index-meta',
    },
)
