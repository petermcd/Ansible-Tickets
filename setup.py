from setuptools import find_packages, setup

PACKAGE_NAME = 'Ansible Tickets'
PACKAGE_VERSION = '0.0.6'
DESCRIPTION = 'Creates Jira tickets for Ansible failures.'
with open('README.md', 'r') as fileHandler:
    LONG_DESCRIPTION = fileHandler.read()

TEST_REQUIRES = [
    'flake8',
    'mypy',
    'pytest',
    'twine',
    'wheel',
]


setup(
    name=PACKAGE_NAME,
    version=PACKAGE_VERSION,
    url='',
    download_url='',
    entry_points={
        'console_scripts': ['ansible_tickets=ansible_tickets.cli:init']
    },
    project_urls={},
    author='Peter McDonald',
    author_email='me@petermcdonald.co.uk',
    maintainer='Peter McDonald',
    maintainer_email='me@petermcdonald.co.uk',
    classifiers='',
    license='MIT',
    license_file='LICENSE',
    license_files='LICENSE',
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='',
    keywords='ansible, jira',
    packages=find_packages(),
    package_dir={'ansible_tickets': 'ansible_tickets'},
    platforms='',
    provides='',
    requires='',
    extras_require={'test': TEST_REQUIRES},
    obsoletes='',
)
