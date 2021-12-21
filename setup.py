import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="DictDots",
    version="0.1.1",
    description="DictDots is a tool to access nested dictionaries without long if-else chains.",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/alexlambson/python-dict-dots/",
    author="Alex Lambson",
    author_email="support@alexlambson.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Utilities",
    ],
    packages=["dictdots"],
    include_package_data=True,
)
