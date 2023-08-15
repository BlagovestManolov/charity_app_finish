from django.views import View


class ChoicesMixin:
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for _, name in cls.choices())


class GetInformationFromModelMixin(View):

    def _get_user_primary_key(self):
        """
        Returns the primary key of the authenticated user.
        """
        return self.request.user.pk

    @staticmethod
    def _get_objects_from_model(model_name, **kwargs):
        if kwargs:
            objects = model_name.objects.filter(**kwargs)
        else:
            objects = model_name.objects.all()
        return objects


class GetCharityUserMixin(View):
    """
    Returns the authenticated user.
    """
    def _get_user(self):
        return self.get_object()


class AddToContextMixin(View):
    @staticmethod
    def _add_to_context(**kwargs):
        return {**kwargs}


