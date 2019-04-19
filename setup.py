import codecs
import os
import re

from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

# https://packaging.python.org/guides/single-sourcing-package-version/
here = os.path.abspath(os.path.dirname(__file__))
requirements = [
    'bpemb>=0.2.9',
    'networkx>=2.2',
    'nltk>=3.4',
    'numpy>=1.15.4',
    'packaging>=18.0',
    'pandas>=0.23.4',
    'spacy>=2.0.16',
    'textblob>=0.15.2',
    'tqdm>=4.29.1',
    'webargs>=5.1.2',
    'langdetect>=1.0.7',
    'scikit-learn>=0.20.1',
    'waitress>=1.2',
    'sumeval==0.1.7',
]

dev_requirements = [
    'pytest>=4.1',
]


def read(*parts):
    with codecs.open(os.path.join(here, *parts), 'r') as fp:
        return fp.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__: str = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='tesufr',
    version=find_version("tesufr", "__init__.py"),
    description='Multilingual text summarizing framework',
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["natural language processing", "nlp", "summary", "keywords"],
    url='https://github.com/serge-sotnyk/tesufr',
    author='S.Sotnyk',
    install_requires=requirements,
    extras_require={
        'dev': dev_requirements
    },
    packages=['tesufr', 'tesufr.cores', 'tesufr.text_utils', 'tesufr.models', 'tesufr.keysum_evaluator',
              'tesufr.corpora'],
    python_requires='>=3.6'
)
