tornado-rest-handler
====================

A simple Python Tornado handler that manage Rest requests automatically

* [Basic Example of Usage](#basic-example-of-usage)
  * Routes
  * Handler implementation
  * Templates
* [Installation](#installation)
* [More Handlers](#more-handlers)
* [Customization](#customization)
* [Change Log](#change-log)
* [TODO](#todo)

Basic Example of Usage
------------------------

In the current implementation, there is only one handler for MongoEngine ORM.

### Routes

One handler for every Rest routes

* GET    /animals index      display a list of all animals
* GET    /animals/new        new return an HTML form for creating a new animal
* POST   /animals create     create a new animal
* GET    /animals/:id show   show an animal
* GET    /animals/:id/edit   return an HTML form for editing a photo
* PUT    /animals/:id        update an animal data
* DELETE /animals/:id        delete an animal

Since HTML5-forms does not support PUT/DELETE. It is possible to use the following methods too:

* POST /animals/:id/delete   Same as DELETE /animals/:id
* POST /animals/:id          Same as PUT    /animals/:id


```python
    (r'/animals/?', AnimalHandler), # GET, POST
    (r'/animals/new/?', AnimalHandler), # GET
    (r'/animals/([0-9a-fA-F]{24,})/?', AnimalHandler), # GET, POST, PUT, DELETE
    (r'/animals/([0-9a-fA-F]{24,})/(edit|delete)/?', AnimalHandler), # GET, POST
```


### Handler implementation

All the get/post/put/delete methods are implemented for you. Simple as that:

```python
from tornardo_rest_handler import MongoEngineRestHandler

class AnimalHandler(MongoEngineRestHandler):
    model = Animal
```

### Templates

You must create your own template. It must have the names list.html, show.html and edit.html.

* animal/list.html
* animal/show.html
* animal/edit.html

By default, the directory is the model name in lower case. You may change the directory though:

```python
class AnimalHandler(MongoEngineRestHandler):
    model = Animal
    template_path = 'my_dir'
```

More Handlers
-------------

To create a RestHandler for your ORM you must override the RestHandler class and implement the following methods:

```python
class CouchDBRestHandler(RestHandler):
    def instance_list(self): return [] # it can return a list or a queryset etc
    def find_instance_by_id(self, obj_id): pass
    def save_instance(self, obj): pass
    def update_instance(self, obj): pass
    def delete_instance(self, obj): pass
```

Customization
-------------

By default, the list page will show all models of that type. To filter by user or other properties, override the instance_list method:

```python
class AnimalHandler(MongoEngineRestHandler):
    model = Animal

    def instance_list(self):
        return Animal.objects.filter(...)
```

To change the template names, override the following variables:

```python
class AnimalHandler(MongoEngineRestHandler):
    LIST_TEMPLATE = 'list.html'
    EDIT_TEMPLATE = 'edit.html'
    SHOW_TEMPLATE = 'show.html'
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
tornado-rest-handler==0.0.2
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
* redirect instead of render for successffull actions.
* Use fields and exclude to facilitate auto-generate forms:

```python
class AnimalHandler(MongoEngineRestHandler):
    model = Animal
    fields = []
    exclude = []
```
