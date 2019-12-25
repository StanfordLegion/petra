from setuptools import setup

setup(
    name = "petra",
    version = "alpha",
    description = "A compiler for Petra programs that emits LLVM",
    author = "Andrew Benson",
    author_email = "adbenson@stanford.edu",
    packages = ["petra"],
    install_requires = ["llvmlite"],
)
