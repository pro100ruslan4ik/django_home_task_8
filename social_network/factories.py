import factory
from factory.django import ImageField

from social_network import models


class UserFactory(factory.django.DjangoModelFactory):
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    email = factory.Faker('email')
    avatar = factory.django.ImageField()
    created_at = factory.Faker('date_time')
    date_of_birth = factory.Faker('date_of_birth',minimum_age=14,maximum_age=99)

    class Meta:
        model = models.User