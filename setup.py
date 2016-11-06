import os.path
from setuptools import setup, find_packages
from pip.req import parse_requirements

here = os.path.abspath(os.path.dirname(__file__))

requirements_path = os.path.join(here, 'requirements.txt')
install_requirements = parse_requirements(requirements_path, session=False)
requirements = [str(ir.req) for ir in install_requirements]

setup(
    name='sner',
    version='0.1.0',
    description='Sumerian Named Entity Recognition',
    author='Andy Brown, Mike Canoy, Ian Fisk, Matt Glitsch, Luke Terry',
    author_email='browna52@wwu.edu, canoym@wwu.edu, fiski@wwu.edu, glitscm@wwu.edu, terryl@wwu.edu',
    url='https://gitlab.cs.wwu.edu/canoym/sumerian',
    packages=find_packages(),
    install_requires=requirements,
    classifiers=[
        'Environment :: Console',
        'Natural Language :: English',
    ],
    py_modules=['sner', 'editdistance'],
    entry_points={
        'console_scripts': [
            'sner=sner:main',
        ]
    },
)
