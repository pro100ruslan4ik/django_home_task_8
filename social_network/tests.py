from django.test import TestCase
from django.urls import reverse

from social_network import factories, models


class SocialNetworkTestCase(TestCase):
    def setUp(self):
        self.user = factories.UserFactory()

    def test_get_user_list(self):
        url = reverse('user_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['users'].count(), models.User.objects.count())
        # print(response.context['users'].count(), models.User.objects.count())

    def test_get_user_detail(self):
        url = reverse('user_detail', kwargs={'pk': self.user.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_update_user(self):
        url = reverse('user_update', kwargs={'pk': self.user.pk})
        old_first_name = self.user.first_name
        old_last_name = self.user.last_name
        old_email = self.user.email
        old_date_of_birth = self.user.date_of_birth

        response = self.client.post(url, {
            'first_name': 'new_first_name',
            'last_name': old_last_name,
            'email': old_email,
            'date_of_birth': old_date_of_birth
        })
        self.user.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertNotEqual(self.user.first_name, old_first_name)

    def test_delete_user(self):
        url = reverse('user_delete', kwargs={'pk': self.user.pk})
        old_user_count = models.User.objects.count()
        response = self.client.post(url)
        self.assertEqual(response.status_code, 302)
        self.assertGreater(old_user_count, models.User.objects.count())
        # print(old_user_count, models.User.objects.count())

    def test_create_user(self):
        url = reverse('user_create')
        old_user_count = models.User.objects.count()
        response = self.client.post(url, {
            'first_name': 'new_first_name',
            'last_name': 'new_last_name',
            'email': 'new_email@email.com',
            'date_of_birth': '2000-01-01'
        })
        self.assertEqual(response.status_code, 302)
        self.assertGreater(models.User.objects.count(), old_user_count)