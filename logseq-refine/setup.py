from setuptools import setup, find_packages

setup(
    name="logseq-graph-refiner",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "click",
        "rich",
        "pathspec",
    ],
    entry_points={
        "console_scripts": [
            "logseq-refine=refine_graph.cli:main",
        ],
    },
)
