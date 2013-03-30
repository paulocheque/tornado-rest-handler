# coding: utf-8
import unittest

from tornado_rest_handler import *


class RestHandlerMetaclassTests(unittest.TestCase):
    def test_it_does_not_validate_base_classes_creation(self):
        RestHandler
        MongoEngineRestHandler
        # no exception is raised

    def test_it_must_raise_an_error_if_custom_handler_does_not_have_model_attribute(self):
        class InvalidHandler(RestHandler):
            def __init__(self): pass
        try:
            InvalidHandler()
            raise Exception('invalid validation')
        except NotImplementedError as e:
            self.assertTrue('requires the field "model"' in str(e))

    def test_it_must_raise_an_error_if_custom_mongo_handler_does_not_have_model_attribute(self):
        try:
            class InvalidMongoHandler(MongoEngineRestHandler):
                def __init__(self): pass
            InvalidMongoHandler()
            raise Exception('invalid validation')
        except NotImplementedError as e:
            self.assertTrue('requires the field "model"' in str(e))

    def test_it_create_custom_handler_correctly(self):
        class ModelObject(object): pass
        class ValidHandler(RestHandler):
            model = ModelObject
        # no exception is raised

    def test_it_create_custom_mongo_handler_correctly(self):
        class ModelObject(object): pass
        class ValidMongoHandler(MongoEngineRestHandler):
            model = ModelObject
        # no exception is raised


class TemplatePathTests(unittest.TestCase):
    def test_default_template_path_is_blank(self):
        self.assertEquals('', RestHandler.TEMPLATE_PATH)
        self.assertEquals('', MongoEngineRestHandler.TEMPLATE_PATH)

    def test_default_template_path_is_the_model_name_as_lower_case(self):
        class ModelObject(object): pass
        class ValidMongoHandler(MongoEngineRestHandler):
            model = ModelObject
        self.assertEquals('modelobject/', ValidMongoHandler.TEMPLATE_PATH)
