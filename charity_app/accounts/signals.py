from django.contrib.auth import get_user_model, user_logged_in
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.utils import timezone
from charity_app.accounts.models import CharityUserProfile, OrganizationUserProfile
from charity_app.blogs.models import Blogs, BlogComments
from charity_app.projects.models import Project, ProjectImages

UserModel = get_user_model()


@receiver(post_save, sender=UserModel)
def create__user_profile__or__organization_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to create a user profile or organization profile upon user creation.

    This receiver function is connected to the post_save signal of the UserModel and creates
    either a CharityUserProfile or an OrganizationUserProfile depending on the user_type of
    the newly created user.
    """
    if created:
        if instance.user_type == 'U':
            CharityUserProfile.objects.create(user=instance)
        # Logic when user_type == Organization (O)
        else:
            OrganizationUserProfile.objects.create(user=instance)


@receiver(post_save, sender=UserModel)
def save__user_profile__or__organization_profile(sender, instance, **kwargs):
    """
    Signal handler to save the associated profile for a User instance after it is saved.

    This function is connected to the `post_save` signal of the `UserModel` and is responsible
    for saving the corresponding profile based on the user's type ('U' for User or 'O' for Organization).
    """
    if instance.user_type == 'U':
        instance.charityuserprofile.save()
    # Logic when user_type == Organization (O)
    else:
        instance.organizationuserprofile.save()


@receiver(user_logged_in)
def save__last_login_date(sender, request, user, **kwargs):
    """
    Signal handler to update the last login date for a user upon successful login.

    This function is connected to the `user_logged_in` signal and is responsible for
    updating the `last_login` attribute of the provided user instance with the current
    date and time upon a successful login.
    """
    user.last_login = timezone.now()
    user.save()


@receiver(post_save, sender=UserModel)
def delete__user_automatically_if_not_log_in_more_than_year(sender, instance, **kwargs):
    """
    Signal handler to automatically delete a user if they haven't logged in for over a year.

    This function is connected to the `post_save` signal of the `UserModel` and checks whether
    the user instance has not logged in for more than a year. If so, it automatically deletes
    the user instance from the database.
    """
    if instance.last_login is not None:
        days_inactive = (timezone.now() - instance.last_login).days
        if days_inactive > 365:
            instance.delete()


@receiver(post_delete, sender=UserModel)
def delete__user_profile_related_to_the_deleted_user(sender, instance, **kwargs):
    """
    Signal handler to automatically delete the associated user profile when a user is deleted.

    This function is connected to the `post_delete` signal of the `UserModel` and is responsible
    for deleting the associated profile (CharityUserProfile or OrganizationUserProfile) when a
    User instance is deleted.
    """
    if instance.user_type == 'O':
        try:
            organization_profile = instance.organizationuserprofile
            organization_profile.delete()
        except OrganizationUserProfile.DoesNotExist:
            raise Exception('Not deleted!')

    elif instance.user_type == 'U':
        try:
            volunteer_profile = instance.charityuserprofile
            volunteer_profile.delete()
        except CharityUserProfile.DoesNotExist:
            return Exception('Not deleted!')


@receiver(post_delete, sender=UserModel)
def delete__projects_related_to_the_deleted_organization(sender, instance, **kwargs):
    """
    Signal handler to automatically delete projects and related content when an organization is deleted.

    This function is connected to the `post_delete` signal of the `UserModel` and is responsible for
    deleting projects associated with an organization, along with their related images, blogs, comments,
    and volunteer associations.
    """
    if instance.user_type == 'O':
        organization_projects = Project.objects.filter(organization=instance)

        for project in organization_projects:
            project_images = ProjectImages.objects.filter(project=project)
            project_images.delete()

            project_blogs = Blogs.objects.filter(project=project)

            for blog in project_blogs:
                blog_comments = BlogComments.objects.filter(blog=blog)
                blog_comments.delete()

            project_blogs.delete()

            project.volunteers.clear()

        organization_projects.delete()

