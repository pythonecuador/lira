import setuptools

from lira import __version__

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="lira",
    version=__version__,
    author="Python Ecuador",
    author_email="ecuadorpython@gmail.com",
    description="Tutorial interactivo de Python en tu terminal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    include_package_data=True,
    package_data={"lira": ["*.rst"]},
    install_requires=[
        "docutils==0.16",
        "PyYAML==5.3.1",
        "prompt-toolkit==3.0.7",
        "Pygments==2.7.2",
    ],
    entry_points={
        "console_scripts": [
            "lira=lira.__main__:main",
        ],
    },
    extras_require={"docs": ["sphinx==3.2.1"], "es": []},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    project_urls={
        "Homepage": "https://github.com/pythonecuador/pylearn/",
        "Source Code": "https://github.com/pythonecuador/pylearn/",
        "Issue Tracker": "https://github.com/pythonecuador/pylearn/issues",
    },
)
