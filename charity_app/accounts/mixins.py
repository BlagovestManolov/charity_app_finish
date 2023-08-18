from django.views import View


class ChoicesMixin:
    """
    This mixin provides class methods to retrieve the choices from a choice enumeration
    and calculate the maximum length of choice names.
    """
    @classmethod
    def choices(cls):
        return [(choice.value, choice.name) for choice in cls]

    @classmethod
    def max_len(cls):
        return max(len(name) for _, name in cls.choices())


class GetInformationFromModelMixin(View):
    """
    This mixin provides methods to retrieve information from models based on specified criteria,
    such as the primary key of the authenticated user or additional keyword arguments.
    """
    def _get_user_primary_key(self):
        """
        Returns the primary key of the authenticated user.
        """
        return self.request.user.pk

    @staticmethod
    def _get_objects_from_model(model_name, **kwargs):
        """
        Retrieve objects from a model based on specified criteria.

        Args:
            model_name (Model): The model class from which to retrieve objects.
            **kwargs: Additional keyword arguments for filtering the objects.
        """
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
    """
    This mixin provides a method to easily add data to the context dictionary.
    """
    @staticmethod
    def _add_to_context(**kwargs):
        """
        Create a context dictionary with the provided key-value pairs.

        Args:
            **kwargs: Key-value pairs to be added to the context.
        """
        return {**kwargs}


