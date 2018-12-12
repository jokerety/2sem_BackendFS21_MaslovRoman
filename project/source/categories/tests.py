# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client

import json
from core.models import User
from django.test import TestCase, Client
from django.contrib.auth.models import  User
from mock  import patch
import factory
from faker import Factory
from core.models import User
from categories.models import Category
import categories.views


class TestEntryList(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='test category')

    def test_entry_list (self):
        response = self.client.get('/categories/test/')
        self.assertEqual(response.status_code, 200)


class CategoriesTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.author = UserFactory()
        self.category = CategoryFactory()

    def test_category_list (self):
        categories = CategoryFactory.build_batch(8, author=self.author)
        for category in categories:
            self.assertEqual(category.description, 'description')
            self.assertEqual(category.author.username, 'John')


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = "John"


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category

    name = factory.Iterator(["category1", "category2", "category3"])
    description = "description"
    author = factory.SubFactory(UserFactory)


class NumberCategoriesTest(TestCase):
    fixtures = ['data.json']

    def test_number (self):
        self.assertEqual(Category.objects.all().count(), 10)


class MockTest(TestCase):
    @patch('categories.views.mock')
    def test_mock(self, mock_status):
        mock_status.return_value = 200
        value = categories.views.mock()
        self.assertEqual(value, 200)


class WithoutMock(TestCase):
    def test_you(self):
        value = categories.views.mock()
        self.assertEqual(value, 200)

