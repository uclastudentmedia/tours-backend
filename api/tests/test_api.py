from django.test import TestCase, Client
from api.models import Landmark

class ApiLandmarkListTest(TestCase):
    """
    This test case tests the Landmark list api endpoint, /api/landmark/
    """

    @classmethod
    def setUpTestData(cls):
        # create some test Landmarks
        cls.landmarks = []
        for id in range(1, 4):
            cls.landmarks.append(Landmark.objects.create(id=id, name=str(id),
                                           lat=0, long=0, text_description=''))

    def setUp(self):
        self.client = Client()
        self.response = self.client.get('/api/landmark/')
        self.results = self.response.json()['results']


    def test_status_200(self):
        # endpoint should give status 200
        self.assertEqual(self.response.status_code, 200)

    def test_list_length(self):
        # the landmark list should have the correct number of items
        # TODO: change this test if we limit the number of results
        self.assertEqual(len(self.results), len(self.landmarks))

    def test_landmark_list_valid_ids(self):
        # the list should only have landmarks with existing id's
        valid_ids = [landmark.id for landmark in self.landmarks]
        for landmark in self.results:
            self.assertIn(landmark['id'], valid_ids)


class ApiLandmarkDetailTest(TestCase):
    """
    This test case tests the Landmark list detail endpoint, /api/landmark/<id>
    """
    pass
