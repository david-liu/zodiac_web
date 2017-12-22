
PACKAGE = "zodiac_web"
NAME = "zodiac_web"
DESCRIPTION = "A web generating framework for python"
AUTHOR = "david.liu"
AUTHOR_EMAIL = "willow900.cn@gmail.om"
URL = ""
VERSION = '0.1'

from setuptools import setup, find_packages

setup(
    name=PACKAGE,
    description=DESCRIPTION,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    #py_modules=[NAME],
    include_package_data=True,
    install_requires=[
        'gevent',
        'rainbow_logging_handler',
        'gunicorn==19.7.1',
        'flask',
        'python-json-logger'
    ],
    package_dir={'': 'src'},
    packages=find_packages("src", exclude="tests")
)
