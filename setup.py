"""
A Python3 program that extracts some statistics regarding field coverage from a Solr index.
"""

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(name='solr-fstats',
      version='0.0.1',
      description='a Python3 program that extracts some statistics regarding field coverage from a Solr index',
      url='https://github.com/slub/solr-fstats',
      author='Bo Ferri',
      author_email='zazi@smiy.org',
      license="Apache 2.0",
      packages=[
          'solr_fstats',
      ],
      package_dir={'solr_fstats': 'solr_fstats'},
      install_requires=[
          'argparse>=1.4.0',
          'requests>=2.18.4',
          'sortedcontainers>=2.0.4'
      ],
      entry_points={
          "console_scripts": ["solr-fstats=solr_fstats.solr_fstats:run"]
      }
      )
