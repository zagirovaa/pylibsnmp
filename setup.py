from setuptools import setup

setup(
    name="pylibsnmp",
    version="0.3.2",
    description="Library for working with network devices via snmp.",
    long_description="",
    author="Abdul Zagirov",
    author_email="zagirovaa@netcon.pro",
    license="GNU GPLv3",
    packages=["pylibsnmp"],
    zip_safe=False,
    install_requires=[
        "easysnmp",
    ]
)
