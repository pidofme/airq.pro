from setuptools import setup, find_packages

setup(
    name='airq',
    version="0.1.0",
    description="Check air quality like a pro",

    url='https://github.com/pidofme/airq.pro',

    author='Mingyang Li',
    author_email='pidofme@gmail.com',

    license='MIT',

    packages=find_packages(),
    test_suite="test_airq",
    include_package_data=True,
    exclude_package_data={
        '': ['venv/*']
    },
    install_requires=[
        'flask',
        'geoip2',
        'geopy',
        'requests'
    ]
)
