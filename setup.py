import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hkscs-unicode-converter",
    version="0.0.1",
    author="Aaron Tan",
    author_email="hi@aaronhktan.com",
    description="Convert HKSCS codepoints to corresponding new codepoints in Unicode 4.1 onwards",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/aaronhktan/hkscs-unicode-converter",
    project_urls={
        "Bug Tracker": "https://github.com/aaronhktan/hkscs-unicode-converter/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    package_data={"": ["*.tsv", "*.json"]},
    python_requires=">=3.7",
)
