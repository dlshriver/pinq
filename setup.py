"""
pylinq setup script.
"""

from distutils.core import setup

with open("README.rst", 'r') as f:
    readme = f.read()
with open("HISTORY.rst", 'r') as f:
    history = f.read()

setup(
    name='pinq',
    version='0.1.1',
    description='LINQ for python.',
    long_description="%s\n\n%s" % (readme, history),
    license='MIT',
    author='David Shriver',
    author_email='david.shriver@outlook.com',
    url='https://github.com/dlshriver/pinq',
    packages=[
        'pinq',
    ],
    classifiers=(
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
    )
)
