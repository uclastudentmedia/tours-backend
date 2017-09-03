from django.test import TestCase, Client
from django.forms.models import model_to_dict
from django.conf import settings

import unittest
import os
import json

from api.models import Landmark, Category

class ApiLandmarkListTest(TestCase):
    """
    This test case tests the Landmark list api endpoint, /api/landmark/
    """

    @classmethod
    def setUpTestData(cls):
        # create some test Landmarks
        cached_filename = os.path.join(settings.MEDIA_ROOT,
                                       'landmark/cache/landmark.json')
        with open(cached_filename) as cached_file:
            js = json.load(cached_file)['results']
        landmarks = [Landmark(id=l['id'], name=l['name']) for l in js]
        cls.landmarks = Landmark.objects.bulk_create(landmarks)


    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/api/landmark/')
        self.results = self.response.json()['results']


    def test_status_200(self):
        # endpoint should give status 200
        self.assertEqual(self.response.status_code, 200)

    def test_is_list(self):
        # should return a list of landmarks
        self.assertIs(type(self.results), list)

    def test_list_length(self):
        # the landmark list should have the correct number of items
        # TODO: change this test if we limit the number of results
        self.assertEqual(len(self.results), len(self.landmarks))

    def test_valid_ids(self):
        # the list should only have landmarks with existing id's
        valid_ids = [landmark.id for landmark in self.landmarks]
        for landmark in self.results:
            self.assertIn(landmark['id'], valid_ids)

    def test_included_fields(self):
        landmark = self.results[0]
        # this endpoint should give basic data, including coords and name
        for attr in ['id', 'lat', 'long', 'name', 'category_id']:
            landmark[attr]


class ApiLandmarkDetailTest(TestCase):
    """
    This test case tests the Landmark list detail endpoint, /api/landmark/<id>
    """
    @classmethod
    def setUpTestData(cls):
        # create some test Landmarks
        cls.landmarks = []
        for id in range(1, 4):
            cls.landmarks.append(Landmark.objects.create(id=id, name=str(id)))

    def setUp(self):
        self.client = Client()


    def test_status_200(self):
        # endpoint should give status 200
        response = self.client.get('/api/landmark/1/')
        self.assertEqual(response.status_code, 200)

    def test_status_error(self):
        # invalid id's should not give status 200
        id = len(self.landmarks) + 1
        response = self.client.get('/api/landmark/' + str(id) + '/')
        self.assertNotEqual(response.status_code, 200)

    def test_single_result(self):
        # endpoint should return a single landmark
        response = self.client.get('/api/landmark/1/')
        results = response.json()['results']
        self.assertIs(type(results), dict)

    def test_detail_data(self):
        # the returned data should match the landmark object
        for landmark in self.landmarks:
            response = self.client.get('/api/landmark/' + str(landmark.id) + '/')
            results = response.json()['results']
            landmark_dict = {
                "id": landmark.id,
                "name": landmark.name,
                "text_description": landmark.text_description,
            }
            self.assertDictContainsSubset(landmark_dict, results)
