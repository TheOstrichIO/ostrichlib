import codecs
from os.path import abspath, dirname, join

from setuptools import setup, find_packages

import ostrich


with codecs.open(join(abspath(dirname(__file__)), 'README.rst'),
                 encoding='utf-8') as readme_f:
    long_description = readme_f.read()


setup(
    name='ostrichlib',
    version=ostrich.__version__,
    author=ostrich.__author__,
    author_email='python@ostricher.com',
    url='https://github.com/TheOstrichIO/ostrichlib',
    description=ostrich.__oneliner__,
    long_description=long_description,
    packages=find_packages(),
    install_requires=['future'],
    setup_requires=['pytest-runner'],
    extras_require={
        'test': ['pytest', 'pytest-cov', 'pytest-pep8'],
    },
    zip_safe=True,
    license='MIT',
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
