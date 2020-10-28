# Asymmetric

<a href="https://pypi.org/project/asymmetric" target="_blank">
    <img src="https://img.shields.io/pypi/v/asymmetric?label=version&logo=python&logoColor=%23fff&color=306998&style=for-the-badge" alt="PyPI - Version">
</a>

_The async framework that calls you back_! ✨ Enable ridiculously fast and easy module-to-**[API](https://en.wikipedia.org/wiki/Web_API)** transformations. Learn in minutes, implement in seconds. Batteries included.

<a href="https://github.com/daleal/asymmetric/actions?query=workflow%3Atests" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/daleal/asymmetric/tests?label=tests&logo=python&logoColor=%23fff&style=for-the-badge" alt="Tests">
</a>

<a href="https://codecov.io/gh/daleal/asymmetric" target="_blank">
    <img src="https://img.shields.io/codecov/c/gh/daleal/asymmetric?label=coverage&logo=codecov&logoColor=ffffff&style=for-the-badge" alt="Coverage">
</a>

<a href="https://github.com/daleal/asymmetric/actions?query=workflow%3Alinters" target="_blank">
    <img src="https://img.shields.io/github/workflow/status/daleal/asymmetric/linters?label=linters&logo=github&style=for-the-badge" alt="Linters">
</a>

## Why Asymmetric?

Raw developing speed and ease of use, that's why. `asymmetric` is based on **[starlette](https://github.com/encode/starlette)** ✨! While `starlette` is a powerful tool to have, getting it to work from scratch can be a bit of a pain, especially if you have never used it before. The idea behind `asymmetric` is to be able to take any module **already written** and transform it into a working API in a matter of minutes, instead of having to design the module ground-up to work with `starlette` (it can also be used to build an API from scratch really fast). With `asymmetric`, you will also get some neat features, namely:

- Auto logging (configure logs with the `LOG_FILE` environmental variable).
- Server-side error detection and exception handling.
- **Asynchronous callback endpoints** to make a request, terminate the request **immediately** and then have the server make a request to a _callback_ endpoint with the results! ✨
- Auto-generated `/docs` and `/redoc` endpoint for your API with **interactive documentation**.
- Auto-generated [OpenAPI Specification](https://swagger.io/docs/specification/about/) documentation files for your API.

`asymmetric` is the spiritual successor to [`symmetric`](https://github.com/daleal/symmetric). In fact, **the base API is identical** (you could probably search and replace `symmetric` for `asymmetric` in legacy code), but `asymmetric` uses a more modern underlying technology to achieve better performance and [**some nifty tricks**](#call-me-back). Its internal design is also **significantly** changed! 🎉

## Installing

Install using pip!

```sh
pip install asymmetric
```

## Usage

### Running the development server

`asymmetric` has its own batteries included out of the box! To start your development API server, just run:

```sh
asymmetric run <module> --reload
```

Where `<module>` is your module name (in the examples, we will be writing in a file named `module.py`, so the module name will be just `module`). A `starlette` instance will be spawned immediately and can be reached at [http://127.0.0.1:8000](http://127.0.0.1:8000) by default. We don't have any endpoints yet, so we'll add some later. **All of the flags for `uvicorn` are accepted as flags for `asymmetric run`**.

**Sidenote**: `asymmetric` is fully compatible with any `ASGI` server! If you don't know what that is, don't worry! You don't need to. But if you want to use another `ASGI` server, you can! Just make sure to target the `asymmetric` object! In fact, the `asymmetric run <module>` command is practically an _alias_ for `uvicorn <module>:asymmetric`. So yes, by default the server running will be `uvicorn`, but, if you want to, you can also use `daphne` or `hypercorn`!

### Defining the API endpoints

The module consists of a main object called `asymmetric`, which includes an important element: the `router` decorator. Let's analyze it:

```py
from asymmetric import asymmetric

@asymmetric.router("/some-route", methods=["post"], response_code=200, callback=False)
```

The decorator recieves 4 arguments: the `route` argument (the endpoint of the API to which the decorated function will map), the `methods` argument (a list of the methods accepted to connect to that endpoint, defaults in only `POST` requests), the `response_code` argument (the response code of the endpoint if everything goes according to the plan. Defaults to `200`) and the `callback` argument (a boolean or an object specifying the request style for that endpoint, defaults to `False`, generating normal endpoint behaviour). The `callback` attribute will have its own section below, for now we will use the default `callback=False`.

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

Run `asymmetric run module --reload` and send a `GET` request to `http://127.0.0.1:8000/sample`. You should get a `Hello World!` in response! (To try it with a browser, make sure to run the above command and click [this link](http://127.0.0.1:8000/sample)).

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

To give parameters to a function, all we need to do is send a `json` body with the names of the parameters as keys. Let's see how! Run `asymmetric run module --reload` and send a `POST` request (the default `HTTP` method) to `http://127.0.0.1:8000/add`, now using the `httpx` module.

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

Given that the underlying framework is `starlette`, you can use `async` to define your methods, no problem! Here's an example:

```py
@asymmetric.router("/another-add")
async def another_async_function(a, b=372):
    """
    Adds :a and :b asynchronously and returns the
    result of that operation.
    """
    return a + b
```

## Call me back!

Don't you hate it when people don't call you back after a date? We all have lived that annoying experience. But don't worry! `asymmetric` **will** call you back!

Some functions may be **too heavy** to be executed to respond to an `HTTP` request. Maybe your function is a predictor of some sort, and it requires an hour of processing time to spit out results. Here's when the `callback` parameter of the `asymmetric` decorator comes into play! You can ask `asymmetric` to terminate the `HTTP` request **immediately**, keep processing stuff and then, once it finishes, **execute a request to a specified endpoint with the results**. Let's imagine that we have a `predict` endpoint that we want to transform into an `API`:

```python
def predict(data):
    values = Model.predict(data)

    # One hour later...
    return values
```

Just add the `asymmetric` decorator and you're good to go!

```python
@asymmetric.router("/predict", callback=True)
def predict(data):
    values = Model.predict(data)

    # One hour later...
    return values
```

Of course, if you rely on some `async` sorcery for your operations, `asymmetric` can handle it!

```python
@asymmetric.router("/predict", callback=True)
async def predict(data):
    values = await Model.predict(data)

    # One hour later...
    return values
```

Start the server with `asymmetric run module --reload` and now you are able to call the endpoint using the following snippet:

```py
import httpx

response = httpx.post(
    "http://127.0.0.1:8000/predict",
    json={"data": mydata},
    headers={
        "Asymmetric-Callback-URL": "http://callback.url/receive/predictions",
        "Asymmetric-Callback-Method": "post",
    }
)

print(response)
```

Wow... **What?!** You just witnessed **the magic of `asymmetric`**. The response will be available **immediately** with a `202` status code. Meanwhile, the server will keep processing the request. When it finishes, **it will make a `POST` request to the endpoint specified in the headers** with the content of the method's return value. Cool, right? But what if I want to send the content of the method's return value inside a `json`, as the value of a `predictions` key? Well, that's easy! Just change the headers!

```py
import httpx

response = httpx.post(
    "http://127.0.0.1:8000/predict",
    json={"data": mydata},
    headers={
        "Asymmetric-Callback-URL": "http://callback.url/receive/predictions",
        "Asymmetric-Callback-Method": "post",
        "Asymmetric-Custom-Callback-Key": "predictions",
    }
)

print(response)
```

That will send a `json` with one element, with `predictions` as a key and the result of the function as the value. **The key here are the headers**. They specify what to do with the result of your function. **You can also change the required headers, if you want to!**

```python
callback_parameters = {
    "callback_url_header": "Send-Me-Here",
    "callback_method_header": "Use-Me",
    "custom_callback_key_header": "Put-Me-In-Here",
}

@asymmetric.router("/predict", callback=callback_parameters)
async def predict(data):
    values = await Model.predict(data)

    # One hour later...
    return values
```

Now, to achieve the same result as before, the requests must change their headers!

```py
import httpx

response = httpx.post(
    "http://127.0.0.1:8000/predict",
    json={"data": mydata},
    headers={
        "Send-Me-Here": "http://callback.url/receive/predictions",
        "Use-Me": "post",
        "Put-Me-In-Here": "predictions",
    }
)

print(response)
```

As you probably imagine by now, the `callback` parameter can be a boolean or a dictionary with the following _pseudo-schema_:

```python
{
    "callback_url_header": {
        "required": False,
        "type": str,
    },
    "callback_method_header": {
        "required": False,
        "type": str,
    },
    "custom_callback_key_header": {
        "required": False,
        "type": str,
    },
}
```

If no `HTTP` method is specified, the server will `POST` the information to the callback `URL`.

## ReDoc/Swagger Documentation

By default, you can `GET` the `/docs` or the `/redoc` endpoints (using a browser) to access to **interactive auto-generated documentation** about your API. It will include request bodies for each endpoint, response codes, headers required, default values, and much more!

**Tip**: Given that the [ReDoc Documentation](https://github.com/Redocly/redoc) and the [SwaggerUI Documentation](https://swagger.io/tools/swagger-ui/) are based on the OpenAPI standard, using **type annotations** in your code will result in a more detailed interactive documentation. Instead of the parameters being allowed to be any type, they will be forced into the type declared in your code. Cool, right?

You can also get a `json` file containing the OpenAPI spec of your API by running the following command:

```sh
asymmetric docs module
```

You can also use the flag `--filename` to specify the name of the output file. It defaults to `openapi.json`.

## To Do

- Parse callback `URL`s to make sure that they are valid `URL`s, and fail if they aren't.

## Developing

Clone the repository:

```sh
git clone https://github.com/daleal/asymmetric.git

cd asymmetric
```

Recreate environment:

```sh
make get-poetry
make venv-with-dependencies
```

Run the linters:

```sh
make linters
```

Run the tests:

```sh
make tests
```

## Aknowledgements

This project wouldn't be possible without [Encode](https://github.com/encode), as literally all hard dependencies (`starlette` and `httpx`) are developed by them. Even `uvicorn` is theirs. Thanks guys! `asymmetric` also takes inspiration from [`FastAPI`](https://github.com/tiangolo/fastapi) on some implementation details, so thank you too for such an awesome project. Also, I want to thank **every person** who has given me some kind of advice or that has had to listen to me going on and on **and on** about this project and the reasons that make it **great**. Finally, thank you! Yes, you! If you are reading this, there is a good chance that you have at least some interest in `asymmetric`. If you have feedback, if you find a bug, if you want to ask for a _feature_ or even if you just want to talk, I'd be glad to hear from you! You're the reason this project exists ♥.

## Resources

- [Issue Tracker](https://github.com/daleal/asymmetric/issues/)
