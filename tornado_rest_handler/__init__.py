# coding: utf-8
import re

import tornado.web
import tornado.util


class CrudHandlerMetaclass(type):
    def __init__(cls, name, bases, attrs):
        result = super(CrudHandlerMetaclass, cls).__init__(name, bases, attrs)
        if attrs.get('__metaclass__') is not CrudHandlerMetaclass:
            # TODO
            # cls.fields = list(cls.model._fields.keys())
            # cls.exclude = []
            if cls.model:
                cls.template_path = cls.model.__name__.lower() + '/'
        return result

    def __call__(cls, *args):
        result = super(CrudHandlerMetaclass, cls).__call__(*args)
        if not cls.model:
            raise NotImplementedError('RestHandler classes (%s) requires the field "model".' % cls.__name__)
        return result


class CrudHandler(tornado.web.RequestHandler):
    model = None
    template_path = ''
    list_template = 'list.html'
    edit_template = 'edit.html'
    show_template = 'show.html'
    redirect_pos_action = None

    def render(self, template_name, **kwargs):
        return super(CrudHandler, self).render(self.template_path + template_name, **kwargs)

    def raise403(self):
        raise tornado.web.HTTPError(403, 'Not enough permissions to perform this action')

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def get_request_data(self):
        data = {}
        for arg in list(self.request.arguments.keys()):
            data[arg] = self.get_argument(arg)
        return data

    def page_list(self, alert=None):
        return self.render(self.list_template, objs=self.instance_list(), alert=alert)

    def page_new(self):
        return self.page_edit(None)

    def page_show(self, instance):
        return self.render(self.show_template, obj=instance)

    def page_edit(self, instance, exception=None, alert=None):
        errors = None
        if exception:
            alert = 'Data sent contains some issues.'
            errors = tornado.util.ObjectDict()
            if hasattr(exception, 'to_dict'):
                errors.update(**exception.to_dict())
        value_for = lambda field: getattr(instance, field, '') if getattr(instance, field, '') else ''
        has_error = lambda field: errors and field in list(errors.keys())
        error_for = lambda field: errors[field] if errors and field in errors else ''
        return self.render(self.edit_template, obj=instance, errors=errors, alert=alert,
                    value_for=value_for, has_error=has_error, error_for=error_for)

    def redirect_with_message(self, message=None):
        if self.redirect_pos_action:
            return self.redirect(self.redirect_pos_action)
        else:
            return self.redirect('/')

    def action_create(self):
        data = self.get_request_data()
        try:
            self.save_instance(data)
            return self.redirect_with_message(message='Object added successfully.')
        except AssertionError as e:
            instance = tornado.util.ObjectDict()
            instance.update(**data)
            return self.page_edit(instance, exception=e)

    def action_read(self, model_id, fail_silently=False):
        try:
            return self.find_instance_by_id(model_id)
        except AssertionError as e:
            if fail_silently:
                return None
            self.raise404()

    def action_update(self, model_id):
        data = self.get_request_data()
        instance = self.action_read(model_id)
        try:
            self.update_instance(instance, data)
            return self.redirect_with_message(message='Object updated successfully.')
        except AssertionError as e:
            return self.page_edit(instance, exception=e)

    def action_delete(self, model_id):
        instance = self.action_read(model_id)
        try:
            self.delete_instance(instance)
            return self.redirect_with_message(message='Object deleted successfully.')
        except:
            return self.page_list('Object could not be deleted.')

    def instance_list(self): return []
    def find_instance_by_id(self, model_id): pass
    def save_instance(self, obj): pass
    def update_instance(self, obj): pass
    def delete_instance(self, obj): pass


CrudHandler = CrudHandlerMetaclass(CrudHandler.__name__, CrudHandler.__bases__, dict(CrudHandler.__dict__))


class RestHandler(CrudHandler):
    '''
    GET    /animals            Index display a list of all animals
    GET    /animals/new        New return an HTML form for creating a new animal
    POST   /animals            Create create a new animal
    GET    /animals/:id        Show show an animal
    GET    /animals/:id/edit   Return an HTML form for editing a photo
    PUT    /animals/:id        Update an animal data
    DELETE /animals/:id        Delete an animal

    POST   /animals/:id/delete Same as DELETE /animals/:id
    POST   /animals/:id        Same as PUT /animals/:id

    Since HTML5-forms does not support PUT/DELETE. It is possible to use those two methods above.
    '''

    def get(self, model_id=None, edit=False):
        if re.match('^/.+/new', self.request.uri):
            return self.page_new()
        if model_id:
            instance = self.action_read(model_id, fail_silently=True)
            if instance:
                if edit:
                    return self.page_edit(instance)
                else:
                    return self.page_show(instance)
            else:
                return self.page_list('Object not found.')
        else:
            return self.page_list()

    def post(self, model_id=None, action=None):
        if model_id and re.match('^/.+/delete', self.request.uri):
            return self.action_delete(model_id)
        if model_id:
            return self.action_update(model_id)
        return self.action_create()

    def put(self, model_id):
        return self.action_update(model_id)

    def delete(self, model_id):
        return self.action_delete(model_id)


class MongoEngineRestHandler(RestHandler):
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
    routes = []
    for route in route_list:
        if isinstance(route, list):
            routes.extend(route)
        else:
            routes.append(route)
    return routes


def create_internal_handler(base, model, **kwargs):
    model_name = model.__name__
    attrs = {}
    attrs['model'] = model
    attrs['template_path'] = kwargs.get('template_path', model_name.lower() + '/')
    attrs['list_template'] = kwargs.get('list_template', 'list.html')
    attrs['edit_template'] = kwargs.get('edit_template', 'edit.html')
    attrs['show_template'] = kwargs.get('show_template', 'show.html')
    attrs['redirect_pos_action'] = kwargs.get('redirect_pos_action', '/')
    handler = kwargs.get('handler', None)
    base_name = base.__name__
    if handler:
        rest_handler = type(model_name + base_name, (handler, base), attrs)
    else:
        rest_handler = type(model_name + base_name, (base,), attrs)
    return rest_handler


def rest_routes(model, **kwargs):
    prefix = kwargs.get('prefix', model.__name__.lower())
    handler = create_internal_handler(MongoEngineRestHandler, model, **kwargs)
    return [
        (r'/%s/?' % prefix, handler),
        (r'/%s/new/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/(edit|delete|)/?' % prefix, handler),
    ]
