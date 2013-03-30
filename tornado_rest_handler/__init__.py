# coding: utf-8
import tornado.web


class RestHandlerMetaclass(type):
    def __init__(cls, name, bases, attrs):
        result = super(RestHandlerMetaclass, cls).__init__(name, bases, attrs)
        if attrs.get('__metaclass__') is not RestHandlerMetaclass:
            # TODO
            # cls.fields = cls.model._fields.keys()
            # cls.exclude = []
            if cls.model:
                cls.TEMPLATE_PATH = cls.model.__name__.lower() + '/'
        return result

    def __call__(cls, *args):
        result = super(RestHandlerMetaclass, cls).__call__(*args)
        if not cls.model:
            raise NotImplementedError('RestHandler classes (%s) requires the field "model".' % cls.__name__)
        return result


class RestHandler(tornado.web.RequestHandler):
    __metaclass__ = RestHandlerMetaclass
    model = None
    TEMPLATE_PATH = ''
    LIST_TEMPLATE = 'list.html'
    EDIT_TEMPLATE = 'edit.html'
    SHOW_TEMPLATE = 'show.html'

    def instance_list(self): return []
    def find_instance_by_id(self, obj_id): pass
    def save_instance(self, obj): pass
    def update_instance(self, obj): pass
    def delete_instance(self, obj): pass

    def obj(self, obj_id, fail_silently=False):
        try:
            return self.find_instance_by_id(obj_id)
        except Exception as e:
            if fail_silently:
                return None
            self.raise404()

    def render(self, template_name, **kwargs):
        super(RestHandler, self).render(self.TEMPLATE_PATH + template_name, **kwargs)

    def get_request_data(self):
        data = {}
        for arg in self.request.arguments.keys():
            data[arg] = self.get_argument(arg)
        return data

    def render_list(self, alert=None):
        self.render(self.LIST_TEMPLATE, objs=self.instance_list(), alert=alert)

    def render_edit(self, instance, errors=[], alert=None):
        self.render(self.EDIT_TEMPLATE, obj=instance, errors=errors, alert=alert)

    def render_show(self, instance):
        self.render(self.SHOW_TEMPLATE, obj=instance)

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def get(self, obj_id=None, edit=False):
        if self.request.uri.endswith('/new'):
            self.render_edit(None)
        if obj_id:
            instance = self.obj(obj_id, fail_silently=True)
            if instance:
                if edit:
                    return self.render_edit(instance)
                else:
                    return self.render_show(instance)
            else:
                return self.render_list('Object not found.')
        else:
            return self.render_list()

    def post(self, obj_id=None, action=None):
        if obj_id and self.request.uri.endswith('/delete'):
            return self.delete(obj_id)
        if obj_id:
            return self.put(obj_id)
        try:
            data = self.get_request_data()
            self.save_instance(data)
            return self.render_list('Object added successfully.')
        except ValidationError as e:
            # TODO: capture errors to send to form
            return self.render_edit(instance, errors=[], alert='Data sent contains some issues.')

    def put(self, obj_id):
        try:
            data = self.get_request_data()
            instance = self.obj(obj_id)
            self.update_instance(instance, data)
            return self.render_list('Object updated successfully.')
        except ValidationError as e:
            # TODO: capture errors to send to form
            return self.render_edit(instance, errors=[], alert='Data sent contains some issues.')

    def delete(self, obj_id):
        instance = self.obj(obj_id)
        try:
            self.delete_instance(instance)
            return self.render_list('Object could not be deleted.')
        except:
            return self.render_list('Object deleted successfully.')


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


