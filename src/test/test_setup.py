from rest_framework.test import APIClient, APITestCase
from user.models import User
from faker import Faker

faker = Faker()


class TestSetup(APITestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super(TestSetup, cls).setUpClass()

    def setUp(self, authenticate=True) -> None:
        self.client_auth = APIClient()

        user = User.objects.create_user(email=faker.user_name(), password=faker.password())
        self.user = user
        if authenticate:
            self.client_auth.force_authenticate(user=user)
