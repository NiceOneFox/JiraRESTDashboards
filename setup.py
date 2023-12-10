# setup.py
from setuptools import setup, find_packages

setup(
    name='JiraDashboardsRest',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
    "requests",
    "matplotlib",
    "datetime"
    ],
    entry_points={
        'console_scripts': [
            'your_script = your_package.main_module:main',
        ],
    },
    author='Evgeniy',
    author_email='test@example.com',
    description='REST',
    url='https://github.com/NiceOne_Fox/JiraRESTDashboards',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
