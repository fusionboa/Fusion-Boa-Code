#!/usr/bin/env python3
"""
FusionBoa Language - Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="fusionboa-lang",
    version="0.9.2",
    author="FusionBoa Team",
    description="FusionBoa v0.9.2 — 902 English-like keywords. Write once, compile to Python, JavaScript, Go, Rust, C++, and 18 more targets. 90+ features: multiple dispatch, generators, UFCS, macros, operator overloading, channels, memory tracking, meta-factories.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fusionboa/Fusion-Boa-Code",
    packages=find_packages(),
    include_package_data=True,
    py_modules=["fusionboa"],
    entry_points={
        "console_scripts": [
            "fusionboa=fusionboa:main",
        ],
    },
    python_requires=">=3.8",
    install_requires=[
        # FusionBoa has zero external Python dependencies.
        # All imports use only the Python standard library.
        # This list is maintained here for future extensibility.
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: Other/Proprietary License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Code Generators",
    ],
    keywords="compiler codegen polyglot programming-language transpiler english-like multi-target natural-language metaprogramming concurrency",
)
