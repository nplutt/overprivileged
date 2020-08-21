from setuptools import find_packages, setup


setup(
    name="overprivileged",
    version="0.0.1",
    description="CLI for discovering overprivileged AWS IAM roles",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license="MIT",
    url="https://github.com/nplutt/overprivileged",
    project_urls={"Source Code": "https://github.com/nplutt/overprivileged/"},
    keywords="overprivileged aws iam cloudtrail roles python",
    classifiers=[
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    python_requires=">=3.6",
    packages=find_packages(exclude=("tests",)),
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "op = overprivileged.cli:main",
            "overprivileged =  overprivileged.cli:main",
        ],
    },
    install_requires=["boto3", "click"],
    extras_require={
        "test": ["pytest", "pytest-cov"],
        "dev": ["black", "isort", "requests"],
    },
)
