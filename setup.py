from setuptools import setup, find_packages

with open("README.md", "r") as readme_file:
    long_description = readme_file.read()

name = "soilgrids"
version = "0.1.0"
dependencies = [

]

setup(
    name="soilgrids",
    version="0.1.0",
    author="Jacob Scott",
    author_email="jscott2718@gmail.com",
    description="Fetch and analyse soil data from the ISRIC Soilgrids API" \
        " https://rest.isric.org/soilgrids/v2.0/docs",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/wurli/soilgrids",
    packages=find_packages(exclude=("tests*",)),
    install_requires=[
        "numpy >= 1.26.0",
        "pandas >= 2.1.0",
        "requests >= 2.31",
        "importlib-metadata; python_version<'3.12'",
    ]
)