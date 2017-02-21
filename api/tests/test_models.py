from django.test import TestCase, Client
from django.db import IntegrityError
import unittest

from api.models import Landmark, Category

class CategoryTest(TestCase):
    """
    This test case tests the Category model
    """

    @classmethod
    def setUpTestData(cls):
        cls.category = Category.objects.create(name='', sort_order=0)

    def setUp(self):
        pass


    def test_primary_key(self):
        # Categories should have unique id's
        with self.assertRaises(IntegrityError):
            Category.objects.create(id=0, name='', sort_order=0)
            Category.objects.create(id=0, name='', sort_order=0)

    def test_landmark_creation(self):
        # Landmark objects can be created with a Category
        l = Landmark.objects.create(name='', category=self.category,
                                           lat=0, long=0)
        self.assertEqual(Landmark.objects.get(id=l.id).category, self.category)

    def test_landmark_modification(self):
        # A Landmark's category can be changed
        l= Landmark.objects.create(name='', lat=0, long=0)
        self.assertIsNone(l.category)
        l.category = self.category
        l.save()
        self.assertEqual(Landmark.objects.get(id=l.id).category, self.category)
        print(Category.objects.all())
