from django.contrib.auth import get_user_model
from django.core.validators import MinLengthValidator
from django.db import models

from charity_app.projects.models import Project

UserModel = get_user_model()


class Blogs(models.Model):
    BLOG_TITLE_MIN_LEN = 8
    BLOG_TITLE_MAX_LEN = 30

    project = models.ForeignKey(
        Project,
        on_delete=models.CASCADE,
    )

    blog_title = models.CharField(
        max_length=BLOG_TITLE_MAX_LEN,
        validators=(
            MinLengthValidator(BLOG_TITLE_MIN_LEN),
        )
    )

    blog_information = models.TextField()

    date_of_creation = models.DateField(
        auto_now_add=True
    )

    def __str__(self):
        return self.blog_title


class BlogComments(models.Model):
    blog = models.ForeignKey(
        Blogs,
        on_delete=models.CASCADE,
    )

    user = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
