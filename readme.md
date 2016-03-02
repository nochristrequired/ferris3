# Ferris 3

[![Build Status](https://travis-ci.org/jonparrott/ferris3.svg?branch=master)](https://travis-ci.org/jonparrott/ferris3)
[![codecov.io](https://codecov.io/github/jonparrott/ferris3/coverage.svg?branch=master)](https://codecov.io/github/jonparrott/ferris3?branch=master)

**Ferris 3** is a collection of flexible utilities for Google App Engine Python.

**Ferris 3** makes using App Engine services easier regardless of which web framework you're using. It provides tools for ndb, memcache, search, oauth2, google APIs, and more.

If you plan on using [Google Cloud Endpoints](https://cloud.google.com/endpoints/), Ferris provides excellent standalone tooling around Cloud Endpoints that can make defining and managing your services much easier.

Examples
--------

There are lots of tools for caching, such as the ``@cache`` decorator:

```python
@ferris3.caching.cache('guestbook-posts', ttl=30)
def get_greetings():
    return GuestbookPost.query().order(-GuestbookPost.created).fetch(20)

@app.route('/')
def guestbook_list():
    greetings = get_greetings()
    return render_template("guestbook.html", greetings=greetings)
```

[Read more about Ferris & Caching](http://ferris-framework.appspot.com/docs3alpha/users_guide/caching.html)

Using Cloud Endpoints has never been easier:

```python
from protorpc import messages
from ferris3 import auto_service, auto_method, Service


class BasicMessage(messages.Message):
    content = messages.StringField(1)


@auto_service
class BasicService(Service):

    @auto_method(returns=BasicMessage)
    def get(self, request, name=(str,)):
        return BasicMessage(content="Hello, %s!" % name)

```

[Read more about Ferris & Endpoints](http://ferris-framework.appspot.com/docs3alpha/users_guide/endpoints.html)

Getting Started & Installation
------------------------------

If you're using Ferris within an existing project or starting a new project with a framework other than webapp2:
* Install Ferris via pip: ``pip install --pre --target=lib ferris``
* Make sure you have [vendoring](http://blog.jonparrott.com/managing-vendored-packages-on-app-engine/) setup in your project. If you don't, you can use [darth](https://github.com/jonparrott/Darth-Vendor).
* That's all. If you run into issues or want to see more you can checkout the [Ferris 3 & Flask](https://github.com/jonparrott/flask-ferris-example) example.

If you're starting from scratch and you're using webapp2 or just using Cloud Endpoints:
* [Ferris 3 Project Skeleton](https://github.com/jonparrott/Ferris-3-Skeleton)
* Go through the [Ferris 3 Tutorial](http://ferris-framework.appspot.com/docs3alpha/tutorial.html).

Documentation
-------------

The documentation is generated with sphinx and is available on the [ferris framework website](http://ferris-framework.appspot.com/docs3alpha/index.html).

Contribution & Feedback
-----------------------

Ferris 3 is still in the early stages and we would love to hear any feedback you have.

* Use the [mailing list](https://groups.google.com/forum/?fromgroups#!forum/ferris-framework) for questions, comments, and general feedback.
* Use github issues to submit bugs and feature requests.
* Submit pull requests to help out directly.

License
-------

Apache Version 2.0, see license in the source directory for more details.
