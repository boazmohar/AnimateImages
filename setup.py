from setuptools import setup, find_packages
from codecs import open
from os import path
here = path.abspath(path.dirname(__file__))


with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

with open(path.join(here, 'requirements.txt'), encoding='utf-8') as f:
    requires = f.read().splitlines()

setup(
    name='animateimages',
    packages=find_packages(exclude=['dist', 'docs', 'test']),
    version='0.1.3',
    description="Animation of matplotlib images",
    long_description=long_description,
    author='Boaz Mohar',
    author_email='boazmohar@gmail.com',
    license='MIT',
    url='https://github.com/boazmohar/animateImages',
    download_url='https://github.com/boazmohar/animateImages/archive/0.1.3.tar.gz',
    keywords=['matplotlib', 'animation', ],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: OSI Approved :: MIT License',
                 'Programming Language :: Python :: 2',
                 'Programming Language :: Python :: 2.7',
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 ],
    install_requires=requires,
)
