from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("requirements.txt") as f:
    required = f.read().splitlines()

setup(
    name="mermaidian",
    version="0.1.2",
    description="""Mermaidian is a simple Python interface for using Mermaid.js diagramming capabilities from Python. It can be used from stand-alone Python and also from IPython based notebooks. The core Mermaid.js syntax for writing diagram code is preserved so that the user can always refer to Mermaid.js documentation. However, the creation of the frontmatter for configuration and custom theme is made easier by using a dict instead of YAML encoding.""",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Munawar Saudagar",
    packages=find_packages(include=["mermaidian"]),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=required,
    license="MIT",
    url="https://github.com/msaudagar/mermaidian",
    python_requires=">=3.9",
)