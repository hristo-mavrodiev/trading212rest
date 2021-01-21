"""
Yahoo Finance stock statistics dowloader.
https://github.com/pypa/sampleproject/blob/master/setup.py
"""

from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="trading212rest",
    version="0.0.1",
    author="Hristo Mavrodiev",
    author_email="h.mavrodiev@abv.bg",
    description="Non official API for Trading212",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/hristo-mavrodiev/trading212rest",
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'requests >= 2.21.0',
        'urllib3 == 1.25.9',
        'selenium == 3.141.0'],
    project_urls={
        'Bug Reports': 'https://github.com/hristo-mavrodiev/trading212rest/issues',
        'Source': 'https://github.com/hristo-mavrodiev/trading212rest',
    },
)