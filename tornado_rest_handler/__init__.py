# coding: utf-8
import tornado.web


class RestHandlerMetaclass(type):
    def __init__(cls, name, bases, attrs):
        result = super(RestHandlerMetaclass, cls).__init__(name, bases, attrs)
        if attrs.get('__metaclass__') is not RestHandlerMetaclass:
            if not cls.document:
                raise NotImplementedError('RestHandler classes requires the field "document".')
            cls.query = cls.document.objects.all()
            cls.fields = cls.document._fields.keys()
            cls.exclude = []
            cls.template_path = cls.document.__name__.lower() + '/'
        else:
            cls.document = None
        return result


class RestHandler(tornado.web.RequestHandler):
    __metaclass__ = RestHandlerMetaclass

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
        super(RestHandler, self).render(self.template_path + template_name, **kwargs)

    def get_request_data(self):
        data = {}
        for arg in self.request.arguments.keys():
            data[arg] = self.get_argument(arg)
        return data

    def render_list(self, message=None):
        self.render('list.html', objs=self.query, message=message)

    def raise404(self):
        raise tornado.web.HTTPError(404, 'Object not found')

    def get(self, obj_id=None, edit=False):
        if self.request.uri.endswith('/new'):
            self.render('edit.html', obj=None)
        if obj_id:
            instance = self.obj(obj_id, fail_silently=True)
            if instance:
                if edit:
                    self.render('edit.html', obj=instance)
                else:
                    data = self.get_arguments('obj_data')
                    self.render('show.html', obj=instance)
            else:
                self.render_list('Object not found.')
        else:
            self.render_list()

    def put(self, obj_id):
        try:
            data = self.get_request_data()
            instance = self.obj(obj_id)
            self.update_instance(instance, data)
            self.render_list('Object updated successfully.')
        except ValidationError as e:
            # TODO: capture errors to send to form
            self.render('edit.html', obj=instance, errors=[], alert='Data sent contains some issues.')

    def post(self, obj_id=None, action=None):
        if obj_id and self.request.uri.endswith('/delete'):
            return self.delete(obj_id)
        if obj_id:
            return self.put(obj_id)
        try:
            data = self.get_request_data()
            self.save_instance(data)
            self.render_list('Object added successfully.')
        except ValidationError as e:
            # TODO: capture errors to send to form
            self.render('edit.html', obj=instance, errors=[], alert='Data sent contains some issues.')

    def delete(self, obj_id):
        instance = self.obj(obj_id)
        try:
            self.delete_instance(instance)
            self.render_list('Object could not be deleted.')
        except:
            self.render_list('Object deleted successfully.')


class MongoEngineRestHandler(RestHandler):
    def find_instance_by_id(self, instance_id):
        return self.query.clone().get(pk=instance_id)

    def save_instance(self, data):
        instance = self.document(**data)
        instance.save()

    def update_instance(self, instance, data):
        instance.update(**data)

    def delete_instance(self, instance):
        instance.delete()
