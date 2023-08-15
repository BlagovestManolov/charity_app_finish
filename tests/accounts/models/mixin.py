from charity_app.accounts.models import CharityUserProfile, CharityUser, OrganizationUserProfile


class CreateProfileObjectsMixin:
    VALID_USER_DATA = {
        'username': 'testuser',
        'email': 'test_user@gmail.com',
        'password': 'testpassword',
        'user_type': 'U',
    }

    INVALID_FIRST_NAME_LENGTH_SMALLER_THAN_MIN_LEN = {
        'first_name': 'Bo',
        'last_name': 'Manolov',
        'phone_number': '+359123123123',
        'information': 'This is some random text.',
        'profile_picture': 'user-photo/pexels-pixabay-220453.jpg',
    }

    VALID_PROFILE_USER_DATA = {
        'first_name': 'Bo',
        'last_name': 'Manolov',
        'phone_number': '+359123123123',
        'information': 'This is some random text.',
        'profile_picture': 'user-photo/pexels-pixabay-220453.jpg',
    }

    def _create_user_with_valid_values(self):
        return CharityUser.objects.create_user(
            **self.VALID_USER_DATA,
        )

    @staticmethod
    def _create_user_with_valid_values_two():
        return CharityUser.objects.create_user(
            username='testwo',
            email='testtwo@gmail.com',
            password='testTwo',
            user_type='U',
        )

    @staticmethod
    def _create_organization_valid_values():
        return CharityUser.objects.create_user(
            username='usertest',
            email='test@gmail.com',
            password='testTwo',
            user_type='O'
        )

    def _create_user_profile_with_invalid_first_name_min_len_value(self):
        return CharityUserProfile.objects.create(
            user_id=self._create_user_with_valid_values().pk,
            **self.VALID_PROFILE_USER_DATA,
        )

