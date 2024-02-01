from setuptools import setup, find_packages

setup(
    name="Portfolio,
    version="0.1.1",
    author="Lucas Lara",
    author_email="lucaslara.salgado@gmail.com",
    description="Testing packages.",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/lucaslara4/entregable_3",
    license="GPL-3.0-or-later",  # Updated license
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src", exclude=["test"]),
    python_requires=">=3.10",
    install_requires=["numpy"],
)