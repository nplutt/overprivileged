from setuptools import setup


setup(
    name="overprivileged",
    version="0.1.0",
    description="",
    author="Nick Plutt",
    author_email="nplutt@gmail.com",
    license='MIT',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=['src'],
    entry_points={'console_scripts': ['op = src.cli:main']}
)
