"""setup.py: Based on github.com/pypa/sampleproject"""
from os import path
from setuptools import setup, find_packages


here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='sumerian-ner',
    version='0.1.1',
    description='Sumerian Named Entity Recognition',
    long_description=long_description,
    url='https://github.com/wwunlp/sner',
    author='Matt Adler, Andy Brown, Mike Canoy, Ian Fisk, Luke Terry',
    author_email='glitscm@wwu.edu, browna52@wwu.edu, canoym@wwu.edu, ' \
                 'fiski@wwu.edu, terryl@wwu.edu',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Text Processing :: Linguistic',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='sumerian named entity recognition',
    packages=find_packages(exclude=['docs', 'tests']),
    install_requires=[
        'editdistance==0.3.1',
        'matplotlib==1.5.3',
        'numpy==1.12.0',
        'pandas==0.19.2',
        'pytest==3.0.5',
        'scikit-learn==0.18.1'
    ],
    extras_require={
        'dev': ['pylint', 'sphinx'],
        'test': ['pytest'],
    },
    entry_points={
        'console_scripts': [
            'sner=sner.__main__:main',
        ],
    },
)
