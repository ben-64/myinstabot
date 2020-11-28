from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
    name='myinstabot',
    version='0.64',
    description='Script to post photos on instagram',
    long_description=long_description,
    author='ben64',
    author_email='ben64@time0ut.org',
    scripts=["myinstabot.py"]
)
