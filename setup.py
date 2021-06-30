import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="unisender",
    version="0.0.1",
    author="tdeems",
    author_email="tdeems@ya.ru",
    description="unisender lib",
    long_description=long_description,
    url="https://github.com/deems/unisender",
    packages=setuptools.find_packages(),
    install_requires=[
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)