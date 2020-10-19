from setuptools import setup, find_packages

setup(
    name="gog-data-processing",
    version="0.1",
    description="Tools for GOG data processing home assignment.",
    author="Marcin Łobaczewski",
    author_email="marcin.lobaczewski@gmail.com",
    packages=find_packages(),
    install_requires=["pandas>=1.1.3"],
)