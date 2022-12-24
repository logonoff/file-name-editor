import setuptools


def readme() -> str:
    """returns readme"""
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


long_description = readme()


setuptools.setup(
    name='vs-rename',
    version='0.1.1',
    scripts=['vs_filenames.py'],
    author="logonoff",
    author_email="hello@logonoff.co",
    description="quick script that helps you mass-edit file names with vscode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/logonoff/vs-rename",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
         "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
         "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'ren-vs = vs_filenames:entry',
        ],
    },
)
