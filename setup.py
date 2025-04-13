from distutils.core import setup
from setuptools import find_packages

def read(file_path):
	with open(file_path, "r") as in_stream:
		return in_stream.read()

setup(
  name = 'shexer',
  packages = find_packages(exclude=["*.local_code.*"]), # this must be the same as the name above
  version = '2.5.10',
  description = 'Automatic schema extraction for RDF graphs',
  author = 'Daniel Fernandez-Alvarez',
  author_email = 'danifdezalvarez@gmail.com',
  url = 'https://github.com/DaniFdezAlvarez/shexer',
  download_url = 'https://github.com/DaniFdezAlvarez/shexer/archive/2.5.10.tar.gz',
  keywords = ['testing', 'shexer', 'shexerp3', "rdf", "shex", "shacl", "schema"],
  long_description = read('README.md'),
  long_description_content_type='text/markdown',
  classifiers=[
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
		"Programming Language :: Python :: 3.10",
		"Programming Language :: Python :: 3.11",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Information Technology",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ],
  install_requires=[            
          'Flask',
          'Flask-Cors',
		  'rdflib',
		  'SPARQLWrapper',
          'wlighter',
          'plantuml',
          'python-xz'
      ],
)
