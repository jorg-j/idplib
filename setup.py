import setuptools


with open("README.md", "r")as f:
    full_description = f.read()

try:
    with open("build_number.txt", "r")as f:
        version = f.read()
except:
    version = "0.0.0"


setuptools.setup(
    name="hslib",
    version=version,
    author="Jack Jorgensen",
    author_email="",
    description="Package to support Hyperscience validation process",
    long_description=full_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'fuzzywuzzy==0.18.0',
        'python-Levenshtein==0.25.0'
    ],
    python_requires=">=3.7"
)

# pip install wheel
# python setup.py bdist_wheel