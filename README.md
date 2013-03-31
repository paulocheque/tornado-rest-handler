tornado-rest-handler
====================

![Continuous Integration Status](https://secure.travis-ci.org/paulocheque/tornado-rest-handler.png)

A simple Python Tornado handler that manage Rest requests automatically

* [Basic Example of Usage](#basic-example-of-usage)
  * [Routes](#routes)
  * [Handlers](#handlers)
  * [Templates](#templates)
* [Installation](#installation)
* [Change Log](#change-log)
* [TODO](#todo)

Basic Example of Usage
------------------------

In the current implementation, there is only one handler for MongoEngine ORM, besides the library does not depends on the MongoEngine!

With +-10 lines of code you can create a handler for your ORM.

Routes
------------------------

One handler for every Rest routes

* GET    /animal index      display a list of all animals
* GET    /animal/new        new return an HTML form for creating a new animal
* POST   /animal create     create a new animal
* GET    /animal/:id show   show an animal
* GET    /animal/:id/edit   return an HTML form for editing a photo
* PUT    /animal/:id        update an animal data
* DELETE /animal/:id        delete an animal

Since HTML5-forms does not support PUT/DELETE. It is possible to use the following methods too:

* POST /animals/:id/delete   Same as DELETE /animals/:id
* POST /animals/:id          Same as PUT    /animals/:id


```python
from tornado_rest_handler import routes, rest_routes

application = tornado.web.Application(routes([
    # another handlers here

    rest_routes(Animal),

    # another handlers here
]))
```

The library does not support auto-plurazation yet, so you may want to change the prefix:

```python
application = tornado.web.Application(routes([
    rest_routes(Animal, prefix='animals'),
]))
```

Handlers
------------------------

All the get/post/put/delete methods are implemented for you, but if you want to customize some behavior, you write your own handler:

```python
class AnimalHandler(tornado.web.RequestHandler):
    pass # your custom methods here
```

And then, registered it:

```python
application = tornado.web.Application(routes([
    rest_routes(Animal, handler=AnimalHandler),
]))
```

To create a RestHandler for your ORM you must override the RestHandler class and implement the following methods:

```python
class CouchDBRestHandler(RestHandler):
    def instance_list(self): return [] # it can return a list or a queryset etc
    def find_instance_by_id(self, obj_id): pass
    def save_instance(self, obj): pass
    def update_instance(self, obj): pass
    def delete_instance(self, obj): pass
```

By default, the list page will show all models of that type. To filter by user or other properties, override the instance_list method:

```python
class AnimalHandler(tornado.web.RequestHandler):
    def instance_list(self):
        return Animal.objects.filter(...)
```


Templates
------------------------

You must create your own template. Tempaltes will receive the variables **obj** or **objs** and **alert** in case there is some message.

It must have the names list.html, show.html and edit.html. But you can customize if you want to:

```python
rest_routes(Animal, list_tempalte='another_name.html', edit_template='...', show_template='...'),
```

By default, the directory is the model name in lower case (animal in this example).

* animal/list.html
* animal/show.html
* animal/edit.html

But you may change the directory though:

```python
rest_routes(Animal, template_path='your_template_path'),
```


Installation
------------

```
pip install tornado-rest-handler
```

#### or

```
1. Download zip file
2. Extract it
3. Execute in the extracted directory: python setup.py install
```

#### Development version

```
pip install -e git+git@github.com:paulocheque/tornado-rest-handler.git#egg=tornado-rest-handler
```

#### requirements.txt

```
tornado-rest-handler==0.0.3
# or use the development version
git+git://github.com/paulocheque/tornado-rest-handler.git#egg=tornado-rest-handler
```

#### Upgrade:

```
pip install tornado-rest-handler --upgrade --no-deps
```

#### Requirements

* Python 2.6 or 2.7
* Tested with Tornado 2.4.1


Change Log
-------------

#### 0.0.3 (2013/03/31)
* [new] CrudHandler extracted from RestHandler.
* [new] Dynamic handlers with dynamic routes (rest_routes function).
* [new] New redirect_pos_action attribute.
* [new] Function routes added to facilitate routes integration.
* [new] Method raise403 useful method in the handler.
* [update] All attributes are now in lower case.
* [update] Stronger uri discover algoritihm.
* [update] Using only AssertionError exceptions.
* [bugfix] Using redirects instead of rendering after actions.


#### 0.0.2 (2013/03/30)
* [update] RestHandler adapted to be used for other ORMs.
* [new] MongoEngineRestHandler
* [new] Template customization: LIST_TEMPLATE, EDIT_TEMPLATE, SHOW_TEMPLATE variables.
* [update] Using OO instead of metaclasses for object list.
* [update] Better exception to alert bad implementations.
* [tests] Initial unit tests.

#### 0.0.1 (2013/03/30)

* [new] RestHandler for MongoEngine


TODO
-------------

* Handlers for another ORMs (other than MongoEngine).
* Pagination
* Send valiation errors to forms
* i18n
* Use fields and exclude to facilitate auto-generate forms:
* plurarize
* splitted handlers
