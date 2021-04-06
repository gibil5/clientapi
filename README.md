# clientapi

[![Version](https://img.shields.io/badge/version-0.1.0-blue)](https://img.shields.io/badge/version-0.1.0-blue)
[![CircleCI](https://circleci.com/gh/ElectricAI/clientapi.svg?style=svg&circle-token=116bb1eeb17c6c4313e6789f3602159fe3f01b39)](https://circleci.com/gh/ElectricAI/clientapi)
[![Maintainability](https://api.codeclimate.com/v1/badges/808f871258566a76cfe0/maintainability)](https://codeclimate.com/repos/606c928b15a5f61085017d7c/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/808f871258566a76cfe0/test_coverage)](https://codeclimate.com/repos/606c928b15a5f61085017d7c/test_coverage)
[![Team](https://img.shields.io/badge/team-ite-orange)](https://img.shields.io/badge/team-ite-orange)

Library to provide a opinionated implementation for building REST API clients

&nbsp;
## Installation


Add this to your python requirements:

    clientapi==0.1.0


This package is stored in Gemfury. You'll need to add the gemfury index to
your python requirements file. For that you can add:

    --extra-index-url https://repo.fury.io/${FURY_AUTH}/electric/

The `FURY_AUTH` variable can be taken from [here](https://manage.fury.io/manage/electric/tokens/shared)

> You may need to add the PyPI index as a fallback
>
> `--extra-index-url https://pypi.org/simple/`


&nbsp;
## Development


### Pre requisites

- Install [Make](https://www.gnu.org/software/make)
- Obtain your [Gemfury Token](https://manage.fury.io/manage/electric/tokens/shared) (aka `FURY_AUTH`)

### Set your Gemfury token as an environment variable

For this step you must have already obtained your Gemfury token. Then create a new environment variable called `FURY_AUTH` and assign your Gemfury token to it so it will be available when running scripts from the terminal.

For this you have two options:

- Add it for your current terminal session (this must be repeated every time you want to use this variable):

  - *Linux/macOS*:

        export FURY_AUTH=<your_gemfury_token>

- Add the variable to your environment variables and restart your terminal (this won't require you to set it again):

  - *Linux/macOS*:

        Add `export FURY_AUTH=<your_gemfury_token>` to your `.bashrc`/`.zshrc` file.


### Initialize your development environment

Just run:

    make init


&nbsp;
### Test & Coverage

For running the tests:

    make test

For checking coverage:

    make coverage

&nbsp;
### Build

Run:

    make build

This will output a `gz` in the `/dist/` folder. Inside that folder
you'll find a file called `clientapi-{VERSION}.tar.gz`. This is the artifact that
we upload to gemfury
