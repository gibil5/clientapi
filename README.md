# clientapi

[![Version](https://img.shields.io/badge/version-0.1.1-blue)](https://img.shields.io/badge/version-0.1.1-blue)
[![CircleCI](https://circleci.com/gh/ElectricAI/clientapi.svg?style=svg&circle-token=116bb1eeb17c6c4313e6789f3602159fe3f01b39)](https://circleci.com/gh/ElectricAI/clientapi)
[![Maintainability](https://api.codeclimate.com/v1/badges/808f871258566a76cfe0/maintainability)](https://codeclimate.com/repos/606c928b15a5f61085017d7c/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/808f871258566a76cfe0/test_coverage)](https://codeclimate.com/repos/606c928b15a5f61085017d7c/test_coverage)
[![Team](https://img.shields.io/badge/team-ite-orange)](https://img.shields.io/badge/team-ite-orange)

Library to provide a opinionated implementation for building REST API clients

&nbsp;
## Installation


Add this to your python requirements:

    clientapi==0.1.1


This package is stored in Gemfury. You'll need to add the gemfury index to
your python requirements file. For that you can add:

    --extra-index-url https://repo.fury.io/${FURY_AUTH}/electric/

The `FURY_AUTH` variable can be taken from [here](https://manage.fury.io/manage/electric/tokens/shared)

> You may need to add the PyPI index as a fallback
>
> `--extra-index-url https://pypi.org/simple/`


&nbsp;
## Usage

#### Creating a Client

The following block shows how to create a new Client with schema parsing

```python3
from enum import Enum
from typing import Optional
from uuid import UUID

from clientapi import ClientAPI, parse
from pydantic import BaseModel


class Path(str, Enum):
    EMPLOYEES = "/api/employees"
    EMPLOYEE = "/api/employees/{employee_id}"


class Employee(BaseModel):  # pylint: disable=too-few-public-methods
    id: UUID
    customer_id: UUID
    slack_id: Optional[str]
    email: str
    first_name: str
    last_name: str


class UpdateEmployeePayload(BaseModel):  # pylint: disable=too-few-public-methods
    first_name: str
    last_name: str
    email: Optional[str]
    avatar: Optional[str]


class CustomersAPI(ClientAPI):

    def __init__(self, session, url="some default url"):
        super().__init__(session, url)

    def update_employee(self, employee_id, payload: UpdateEmployeePayload) -> Employee:
        """Updates an Employee record in api-customers.

        Args:
            employee_id (str): Id of the Employee in the Electric platform
            payload (EmployeeUpdatedRequest): Pydantic model that represents the body of the request.
        """
        url = Path.EMPLOYEE.format(employee_id=employee_id)
        response = self.execute_request(
            url,
            method="PATCH",
            data=payload.json(),
        )
        return parse(response, model=Employee)
```


#### Using the clients

For using the client, you have a set of different sessions as context managers

```python
from clientapi import APIClientError, sessions

from your.project.someplace import (
    CustomersAPI,
    UpdateEmployeePayload,
    API_CUSTOMERS_SHARED_SECRET,
)

with sessions.shared_secret(secret_key=API_CUSTOMERS_SHARED_SECRET) as session:
    api = CustomersAPI(session)

    try:
        payload = UpdateEmployeePayload(...)
        api.update_employee(employee_id="some_id", payload=payload)
    except APIClientError as err:
        # something to do with err
        pass
```

> You can check the exception hierarchy [here](clientapi/exceptions.py)

#### Testing the clients

One way to test the clients is to take advantage of the `responses` library and also
the `clientapi.mocks` module

```python3
import json

import responses
from requests import Session

from clientapi import ClientAPI
from clientapi.mocks import http_200_callback


@responses.activate
def test_execute_success():
    # Given
    url = "https://url.com"
    resource = "/hello"
    body = {"attribute": 1234}

    responses.add_callback(
        url=f"{url}{resource}",
        method="GET",
        callback=http_200_callback(body=body),
    )

    session = Session()

    # When
    api = ClientAPI(url=url, session=session)
    response = api.execute_request(resource=resource)

    # Then
    assert json.loads(response.content) == body

```


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
