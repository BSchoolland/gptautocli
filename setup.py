from setuptools import setup, find_packages

with open("VERSION") as f:
    version = f.read().strip()

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()



setup(
    name="gptautocli", 
    version=version,
    author="Benjamin Schoolland",
    author_email="bschoolland@gmail.com",
    description="Provides a conversational interface to the terminal, allowing you to run commands and perform tasks using natural language.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/BSchoolland/gptautocli",
    packages=find_packages(), 
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'gptautocli = gptautocli.main:main',
        ],
    },
    python_requires=">=3.6",
    install_requires=install_requires,
)
