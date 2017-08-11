from django.test import TestCase
from django.http import Http404
from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos.polygon import Polygon
from PIL import Image, ImageDraw, ImageFont
import unittest
import mock
import os

import indoor.draw as draw
from indoor.models import Building, Floor, POI, RoomPolygon
from api.models import Landmark

class NavigationTest(TestCase):

    def setUp(self):

        self.building = Building.objects.create(name='test building')

        self.landmark = Landmark.objects.create(name='test landmark',
                                                building=self.building)

        self.floor = Floor.objects.create(name='test floor',
                                          building=self.building,
                                          level=1)

        self.start = POI.objects.create(name='test start',
                                        floor=self.floor,
                                        geom=Point(1,1))

        self.end = POI.objects.create(name='test end',
                                      floor=self.floor,
                                      geom=Point(4,4))

        self.start_room = RoomPolygon.objects.create(name=self.start.name,
                                floor=self.floor,
                                geom=self.make_polygon(1,1))

        self.end_room = RoomPolygon.objects.create(name=self.end.name,
                                floor=self.floor,
                                geom=self.make_polygon(4,4))

        self.path = [(1,1), (2,2), (3,3), (4,4)]

        self.draw_route_image_args = {
            'landmark_id': self.landmark.id,
            'floor_name': self.floor.name, 
            'path': self.path,
            'start_name': self.start.name,
            'end_name': self.end.name,
        }

        # mocks
        self._os_patcher = mock.patch('indoor.draw.os', autospec=True)
        self._Image_patcher = mock.patch('indoor.draw.Image', autospec=True)
        self._ImageDraw_patcher = mock.patch('indoor.draw.ImageDraw',
                                             autospec=True)
        self._Draw_patcher = mock.patch('indoor.draw.ImageDraw.ImageDraw',
                                             autospec=True)
        self._ImageFont_patcher = mock.patch('indoor.draw.ImageFont',
                                             autospec=True)

        self.mock_os = self._os_patcher.start()
        self.mock_Image = self._Image_patcher.start()
        self.mock_ImageDraw = self._ImageDraw_patcher.start()
        self.mock_Draw = self._Draw_patcher.start()
        self.mock_ImageFont = self._ImageFont_patcher.start()

        # mock defaults
        self.mock_os.path.isfile.return_value = False
        self.mock_Image.open.return_value = Image.new("RGB", (16, 16))
        self.mock_ImageDraw.Draw.return_value = self.mock_Draw
        self.mock_Draw.textsize.return_value = (10,10)


    def tearDown(self):
        self._os_patcher.stop()
        self._Image_patcher.stop()
        self._ImageDraw_patcher.stop()
        self._Draw_patcher.stop()
        self._ImageFont_patcher.stop()


    # Helper functions

    def make_polygon(self, x, y):
        return Polygon(((x,y), (x,y+1), (x+1,y+1), (x+1,y), (x,y)))


    def change_start_floor(self):
        new_floor = Floor.objects.create(name='new start floor', level=2,
                                         building=self.building)
        self.start.floor = new_floor
        self.start_room.floor = new_floor
        self.start.save()
        self.start_room.save()


    def change_end_floor(self):
        new_floor = Floor.objects.create(name='new end floor', level=3,
                                         building=self.building)
        self.end.floor = new_floor
        self.end_room.floor = new_floor
        self.end.save()
        self.end_room.save()


    # Tests

    def test_no_floorplan_404(self):
        self.mock_Image.open.side_effect = IOError
        with self.assertRaises(Http404):
            draw.draw_route_image(**self.draw_route_image_args)


    def test_route_image_cached(self):
        self.mock_os.path.isfile.return_value = True
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertTrue(self.mock_os.utime.called)
        self.assertFalse(self.mock_Image.open.called)
        self.assertFalse(self.mock_ImageDraw.Draw.called)


    def test_both_rooms_drawn(self):
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertEqual(2, self.mock_Draw.polygon.call_count)


    def test_start_room_drawn(self):
        self.change_end_floor()
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertEqual(1, self.mock_Draw.polygon.call_count)
        # TODO: check that the right text is passed in


    def test_end_room_drawn(self):
        self.change_end_floor()
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertEqual(1, self.mock_Draw.polygon.call_count)


    def test_no_rooms_drawn(self):
        self.change_start_floor()
        self.change_end_floor()
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertEqual(0, self.mock_Draw.polygon.call_count)


    @unittest.skip("needs fix")
    def test_empty_path(self):
        self.draw_route_image_args['path'] = []
        draw.draw_route_image(**self.draw_route_image_args)
        self.assertEqual(2, self.mock_Draw.polygon.call_count)
        self.assertEqual(0, self.mock_Draw.line.call_count)
        self.assertEqual(0, self.mock_Draw.ellipse.call_count)


    def test_num_lines_drawn(self):
        # number of calls == len(path) - 1
        pass


    def test_num_ellipses_drawn(self):
        # number of calls == len(path)
        pass


    def test_get_route_image_path_is_constant(self):
        # multiple calls return the same string
        pass
