# coding: utf-8

"""
    Video API

    Official API
"""

from setuptools import setup, find_packages

with open("README.md", "r") as file:
    long_description = file.read()

NAME = "videoguys"
VERSION = "0.0.3"

REQUIRES = [
    "simple_rest_client>=0.5.4"
]

setup(
    name=NAME,
    version=VERSION,
    description="Video API",
    author_email="",
    url="https://github.com/VideoGuys/python-client",
    keywords=["Video API", "Video Guys", "Vevio", "Vidup"],
    install_requires=REQUIRES,
    packages=find_packages(),
    include_package_data=True,
    long_description=long_description,
    long_description_content_type="text/markdown"
)
