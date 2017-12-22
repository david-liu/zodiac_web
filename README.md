# zodiac web

Zodiac web is a Python package for creating beautiful web service interfaces for exsited python code in a composable way with as little code as necessary. It's also can support to deploy the service in a docker image without any code.

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

you can use `./create_app.py --help`  or `python create_app.py --help` to learn about the command, and the usage will been printed in the console.

```sh
Usage: create_app.py [OPTIONS] NAME

Options:
  --force         whether to override the existed directory or not
  --path TEXT     directory to create the app
  --port INTEGER  Port for the app
  --help          Show this message and exit.
```

For example, if you want to create a new web application named `helloword_app` in the your home path, you can run the following command

```sh
./create_app.py --path ~ helloword_app
```

then a fold `helloword_app` with create in your home path.

## Usage

