import pathlib
from setuptools import setup

setup(
    name="pyserved",
    version="2.0.5",
    description="Share files with your friends (on the same network though). Project setup by Choam by Kian Mckenna.",
    long_description_content_type="text/markdown",
    url="https://github.com/SblipDev/pyserved/",
    author="Shaurya Pratap Singh",
    author_email="shaurya.p.singh21@gmail.com",
    license="MIT",
    packages=["pyserved"],
    install_requires=['netifaces', 'rich'],
    include_package_data=True,
    scripts=['pyserved/bin/pdlisten', 'pyserved/bin/pdsnd'],
)
