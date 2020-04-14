from setuptools import setup
from js8py.version import strictversion

try:
    from setuptools import find_namespace_packages
except ImportError:
    from setuptools import PEP420PackageFinder
    find_namespace_packages = PEP420PackageFinder.find

setup(
    name="js8py",
    version=str(strictversion),
    packages=find_namespace_packages(include=["js8py"]),
    package_data={"js8py": ["*.pickle"]},
    # use the github page for now
    url="https://github.com/jketterl/js8py",
    author="Jakob Ketterl",
    author_email="jakob.ketterl@gmx.de",
    maintainer="Jakob Ketterl",
    maintainer_email="jakob.ketterl@gmx.de",
    license="GPLv3",
    python_requires=">=3.5",
)
