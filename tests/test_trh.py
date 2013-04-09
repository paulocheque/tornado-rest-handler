# coding: utf-8
import unittest
from nose.tools import raises

import tornado.web
import python_rest_handler
from tornado_rest_handler import *

# All tests moved to the python-rest-handler library

class Model(object):
    pass


class TemplatePathTests(unittest.TestCase):
    def test_rest_routes(self):
        cls = rest_routes(Model)[0][1]
        self.assertEquals(True, issubclass(cls, TornadoRestHandler))
        self.assertEquals(True, issubclass(cls, tornado.web.RequestHandler))
        self.assertEquals(True, issubclass(cls, python_rest_handler.RestRequestHandler))

        self.assertEquals(MongoEngineDataManager, cls.data_manager)

        self.assertEquals('list.html', cls.list_template)
        self.assertEquals('edit.html', cls.edit_template)
        self.assertEquals('show.html', cls.show_template)
        self.assertEquals('/', cls.redirect_pos_action)
