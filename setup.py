from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name="planyo",
    description="Python client for Planyo API",
    license="MIT",
    url="https://github.com/chesstrian/planyo-py",
    long_description=long_description,
    version="0.1.0",
    author="Christian Gutierrez",
    author_email="chesstrian@gmail.com",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=["requests>=2.22.0"]
)
