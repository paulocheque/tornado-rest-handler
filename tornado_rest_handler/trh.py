# coding: utf-8
import tornado.web

import python_rest_handler


class TornadoRestHandler(tornado.web.RequestHandler, python_rest_handler.RestRequestHandler):
    def get(self, instance_id=None, edit=False):
        return self.rest_handler.get(instance_id=instance_id, edit=edit)

    def post(self, instance_id=None, action=None):
        return self.rest_handler.post(instance_id=instance_id, action=action)

    def put(self, instance_id):
        return self.rest_handler.put(instance_id=instance_id)

    def delete(self, instance_id):
        return self.rest_handler.delete(instance_id=instance_id)

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def get_request_uri(self):
        return self.request.uri

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
            if data[arg] == '': # Tornado 3.0+ compatibility
                data[arg] = None
        return data

    def render(self, template_name, **kwargs):
        return super(TornadoRestHandler, self).render(template_name, **kwargs)

    def redirect(self, url, permanent=False, status=None, **kwargs):
        return super(TornadoRestHandler, self).redirect(url, permanent=permanent, status=status)


class MongoEngineDataManager(python_rest_handler.DataManager):
    def instance_list(self):
        return self.model.objects.all()

    def find_instance_by_id(self, instance_id):
        return self.instance_list().get(pk=instance_id)

    def save_instance(self, data):
        instance = self.model(**data)
        instance.save()

    def update_instance(self, instance, data):
        instance.__dict__['_data'].update(**data)
        instance.save()

    def delete_instance(self, instance):
        instance.delete()


def routes(route_list):
    return python_rest_handler.routes(route_list)


def rest_routes(model, **kwargs):
    data_manager = kwargs.pop('data_manager', MongoEngineDataManager)
    kwargs['base_handler'] = kwargs['base_handler'] if 'base_handler' in kwargs else TornadoRestHandler
    return python_rest_handler.rest_routes(model, data_manager, **kwargs)

