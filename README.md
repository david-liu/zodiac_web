# zodiac web

Zodiac web is a Python package for creating beautiful web service interfaces for exsited python code in a composable way with as little code as necessary. 

## Installation

zodiac_web is built on python 2.7, before you run the project, please make use you python evironment is > 2.7

Before you use zodiac_web, I recommand you to use [virtualenv](https://virtualenv.pypa.io/en/stable/) to  create an isolated 'virtual' python environment for the project.

### Install virtualenv

```sh
$ [sudo] pip install virtualenv
```

### Create and active a 'virtual' python environment


```sh
$ virtualenv .env
$ source .env/bin/active
```

### Install the dependencies

```sh
$ pip install -r requirements.txt
```


## Generate a web application

When the evironemtn is ready, you can generate  a web application with `create_app.py` 

you can use `./create_app.py --help`  or `python create_app.py --help` to learn about the command.



## Usage

