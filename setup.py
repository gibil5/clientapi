import setuptools

#__version__ = open("clientapi/.version").read()
__version__ = '0.1.2'

with open("README.md") as f:
    long_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setuptools.setup(
    name="clientapi",
    version=__version__,
    author="ITE Team",
    author_email="ite.engineering@electric.ai",
    description="Library to provide a opinionated implementation for building REST API clients",
    url="https://github.com/ElectricAI/clientapi",
    packages=setuptools.find_packages(exclude=("tests", "tests.*")),
    install_requires=requirements,
    include_package_data=True,
    classifiers=[],
)
