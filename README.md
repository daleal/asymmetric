# Asymmetric

![PyPI - Version](https://img.shields.io/pypi/v/asymmetric?style=for-the-badge&logo=python&color=306998&logoColor=%23fff&label=version)

A powerful tool to enable super fast _[async]_ module-to-**[API](https://en.wikipedia.org/wiki/Web_API)** transformations. Learn in minutes, implement in seconds.

![Linters Workflow](https://img.shields.io/github/workflow/status/daleal/asymmetric/linters?label=linters&logo=github&style=for-the-badge)

## Why Asymmetric?

Raw developing speed and ease of use, that's why. `asymmetric` is based on **[Starlette](https://github.com/encode/starlette)** ✨! While `Starlette` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, especially if you have never used it before. The idea behind `asymmetric` is to be able to take any module **already written** and transform it into a working API in a matter of minutes, instead of having to design the module ground-up to work with `Starlette` (it can also be used to build an API from scratch really fast). With `asymmetric`, you will also get some neat features, namely:

- Auto logging.
- Server-side error detection and exception handling.
- ~~Auto-generated `/docs` endpoint for your API with **interactive documentation**.~~ **[UNDER CONSTRUCTION]**
- ~~Auto-generated [OpenAPI Specification](https://swagger.io/docs/specification/about/) documentation files for your API.~~ **[UNDER CONSTRUCTION]**

The [complete documentation](https://asymmetric.one/docs/) is available on the [official website](https://asymmetric.one/).

## Installing

Install using pip!

```sh
pip install asymmetric
```

## Usage

### Running the development server

To start a server, choose your favorite `ASGI` server and target the `asymmetric` object!

```sh
uvicorn run:<module>
```

Where `<module>` is your module name (in the examples, we will be writing in a file named `module.py`, so the module name will be just `module`). A `Starlette` instance will be spawned immediately and can be reached at [http://127.0.0.1:8000](http://127.0.0.1:8000) by default. We don't have any endpoints yet, so we'll add some later.

### Defining the API endpoints

The module consists of a main object called `asymmetric`, which includes an important element: the `router` decorator. Let's analyze it:

```py
from asymmetric import asymmetric

@asymmetric.router("/some-route", methods=["post"], response_code=200)
```

The decorator recieves 3 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `POST` requests) and the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`).

Now let's imagine that we have the following method:

```py
def some_function():
    """Greets the world."""
    return "Hello World!"
```

To transform that method into an API endpoint, all you need to do is add one line:

```py
@asymmetric.router("/sample", methods=["get"])
def some_function():
    """Greets the world."""
    return "Hello World!"
```

Run `uvicorn run:module` and send a `GET` request to `http://127.0.0.1:8000/sample`. You should get a `Hello World!` in response! (To try it with a browser, make sure to run the above command and click [this link](http://127.0.0.1:8000/sample)).

But what about methods with arguments? Of course they can be API'd too! Let's now say that you have the following function:

```py
def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

To transform that method into an API endpoint, all you need to do, again, is add one line:

```py
@asymmetric.router("/add")
def another_function(a, b=372):
    """
    Adds :a and :b and returns the result of
    that operation.
    """
    return a + b
```

### Querying API endpoints

To give parameters to a function, all we need to do is send a `json` body with the names of the parameters as keys. Let's see how! Run `symmetric run module` and send a `POST` request (the default `HTTP` method) to `http://127.0.0.1:8000/add`, now using the `httpx` module.

```python
import httpx

payload = {
    "a": 48,
    "b": 21
}
response = httpx.post("http://127.0.0.1:8000/add", json=payload)
print(response.json())
```

We got a `69` response! (`48 + 21 = 69`). Of course, you can return dictionaries from your methods and those will get returned as a `json` body in the response object **automagically**!

With this in mind, you can transform any existing project into a usable API very quickly!

## What about `async`?

Given that the underlying framework is `Starlette`, you can use `async` to define your methods, no problem! Here's an example:

```py
@asymmetric.router("/another-add")
async def another_async_function(a, b=372):
    """
    Adds :a and :b asynchronously and returns the
    result of that operation.
    """
    return a + b
```

## ~~ReDoc Documentation~~

**[UNDER CONSTRUCTION]**

By default, you can `GET` the `/docs` endpoint (using a browser) to access to **interactive auto-generated documentation** about your API. It will include request bodies for each endpoint, response codes, authentication required, default values, and much more!

**Tip**: Given that the [ReDoc Documentation](https://github.com/Redocly/redoc) is based on the OpenAPI standard, using **type annotations** in your code will result in a more detailed interactive documentation. Instead of the parameters being allowed to be any type, they will be forced into the type declared in your code. Cool, right?

## Developing

Clone the repository:

```sh
git clone https://github.com/daleal/asymmetric.git

cd asymmetric
```

Recreate environment:

```sh
./environment.sh

. .venv/bin/activate
```

Test install:

```sh
poetry install
```

## Resources

- [Official Website](https://asymmetric.one/)
- [Issue Tracker](https://github.com/daleal/asymmetric/issues/)
