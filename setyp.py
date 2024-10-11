from setuptools import setup, find_packages

setup(
    name="pykarutils",
    version="0.1.8",
    author="Andrei Karpatiuk",
    author_email="karpatiuk@gmail.com",
    description="A small utility package for Python",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/karpatiuk/pykarutils",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "requests",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)