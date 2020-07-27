from setuptools import setup, find_packages

version = '0.0.1'

with open('README.rst') as readme:
    long_description = readme.read()

setup(
    name = 'robodkgui',
    version = version,
    description = 'Gui builder for robodk scripts',
    long_description = long_description,
    author = 'Matt Dewar',
    author_email = 'mattpdewar@gmail.com',
    license = 'LICENCE',
    url = 'https://github.com/kobbled/robodk-gui',
    packages=find_packages(),
    platforms='Cross-platform',
    classifiers=[
      'Programming Language :: Python',
      'Programming Language :: Python :: 3'
    ],
)
