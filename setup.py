# Always prefer setuptools over distutils
from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='pdfhandoutcrop',
    version='0.3.2',
    description='A tool to crop pdf handout with multiple pages per sheet',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://cges30901.github.io/pdfhandoutcrop/',
    author='Hsiu-Ming Chang',
    author_email='cges30901@gmail.com',
    license='GPLv3+',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Education',
        'Topic :: Education',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Natural Language :: English',
        'Natural Language :: Chinese (Traditional)',
    ],
    keywords='pdf crop',
    project_urls={
        'Bug Reports': 'https://github.com/cges30901/pdfhandoutcrop/issues',
        'Source': 'https://github.com/cges30901/pdfhandoutcrop/',
    },
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    install_requires=['PyQt5', 'python-poppler-qt5', 'PyPDF2'],
    python_requires='>=3',
    scripts=['scripts/pdfhandoutcrop'],
    package_data={
        'pdfhandoutcrop': ['pdfhandoutcrop.png', 'language/*.ts', 'language/*.qm'],
    },
)
