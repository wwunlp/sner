"""setup.py: From github.com/pypa/sampleproject"""
from setuptools import setup, find_packages


with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name='sumerian-ner',
    version='0.1.1',
    description='Sumerian Named Entity Recognition',
    long_description=long_description,
    url='https://github.com/wwunlp/sner',
    author='WWUNLP SNER Team',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'editdistance',
        'matplotlib',
        'numpy',
        'pandas',
        'scikit-learn',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'sner=sner:main',
        ],
    },
    project_urls={
        'Bug Reports': 'https://github.com/wwunlp/sner/issues',
        'Source': 'https://github.com/wwunlp/sner',
    }
)
