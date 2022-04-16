from pathlib import Path
from setuptools import setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="pyserved",
    version="2.0.8",
    description="Network transfer/hosting utilities by SblipDev.",
    long_description_content_type="text/markdown",
    long_description=long_description,
    url="https://github.com/SblipDev/pyserved/",
    author="Shaurya Pratap Singh",
    author_email="shaurya.p.singh21@gmail.com",
    license="MIT",
    packages=["pyserved"],
    install_requires=["rich"],
    include_package_data=True,
    scripts=["pyserved/bin/pdlisten", "pyserved/bin/pdsnd", "pyserved/bin/pdhost"],
)
