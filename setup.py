import re

from setuptools import setup
import os.path


version = re.search("__version__ = '([^']+)'", open(
        os.path.join(os.path.dirname(__file__), 'multifeedexporter.py')
        ).read().strip()).group(1)

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='scrapy-multifeedexporter',
    version=version,
    py_modules=['multifeedexporter'],
    license=open(os.path.join(here,'LICENSE')).readline().strip(),
    description='Export scraped items of different types to multiple feeds.',
    long_description=README,
    author='Gabriel Birke',
    author_email='gb@birke-software.de',
    url='http://github.com/gbirke/scrapy-multifeedexporter',
    keywords="scrapy crawl scraping",
    platforms = ['Any'],
    install_requires = ['scrapy>=0.23'],
    classifiers = [
        'Development Status :: 4 - Beta',
        'Environment :: No Input/Output (Daemon)',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Scrapy'
        ]
)