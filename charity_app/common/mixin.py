import random

from django.views import View


class TakeInformationForModelMixin(View):
    @staticmethod
    def _get_n_random_objects_from_model(model_name, numbers_of_objects, **kwargs):
        if kwargs:
            objects = model_name.objects.filter(**kwargs)
        else:
            objects = model_name.objects.all()
        if len(list(objects)) < numbers_of_objects:
            number_of_objects = len(list(objects))
            return random.sample(list(objects), number_of_objects)
        else:
            return random.sample(list(objects), numbers_of_objects)

    @staticmethod
    def _get_objects_from_model(model_name, **kwargs):
        if kwargs:
            objects = model_name.objects.filter(**kwargs)
        else:
            objects = model_name.objects.all()
        return objects


class AddToContextMixin(View):
    @staticmethod
    def _add_to_context(**kwargs):
        return {**kwargs}
