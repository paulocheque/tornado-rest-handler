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
        self.assertEquals('', RestHandler.template_path)
        self.assertEquals('', MongoEngineRestHandler.template_path)

    def test_default_template_path_is_the_model_name_as_lower_case(self):
        class ModelObject(object): pass
        class ValidMongoHandler(MongoEngineRestHandler):
            model = ModelObject
        self.assertEquals('modelobject/', ValidMongoHandler.template_path)


class DynamicHandlersTests(unittest.TestCase):
    def test_routes(self):
        self.assertEquals([(1, 2), (3, 4)], routes([(1, 2), (3, 4)]))
        self.assertEquals([(1, 2), (3, 4)], routes([[(1, 2), (3, 4)]]))
        self.assertEquals([(1, 2), (5, 6), (7, 8), (3, 4)], routes([(1, 2), [(5, 6), (7, 8)], (3, 4)]))

    def test_dynamic_class_requires_model_attribute(self):
        class ModelObject(object): pass
        cls = rest_routes(ModelObject)[0][1]
        self.assertEquals(ModelObject, cls.model)

    def test_dynamic_class_use_model_name_to_prefix(self):
        class ModelObject(object): pass
        prefix = rest_routes(ModelObject)[0][0]
        self.assertEquals('/modelobject/?', prefix)

    def test_dynamic_class_template_path_equal_to_model_name(self):
        class ModelObject(object): pass
        cls = rest_routes(ModelObject)[0][1]
        self.assertEquals('modelobject/', cls.template_path)

    def test_dynamic_class_set_default_attributes(self):
        class ModelObject(object): pass
        cls = rest_routes(ModelObject)[0][1]
        self.assertEquals('list.html', cls.list_template)
        self.assertEquals('edit.html', cls.edit_template)
        self.assertEquals('show.html', cls.show_template)
        self.assertEquals('/', cls.redirect_pos_action)
