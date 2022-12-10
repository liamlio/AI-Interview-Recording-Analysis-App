import setuptools

with open("README.md", "r", encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="vindent-utils",
    version="0.0.1",
    author="Liam Croteau",
    author_email="liamcroteau@gmail.com",
    description="A simple audio transcription and analysis pipeline",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/liamlio/AI-Interview-Recording-Analysis-App",
    packages=setuptools.find_packages(exclude=["tests", "tests.*"]),
    install_requires=["torch"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)