from django.test import TestCase
from django.contrib.gis.geos.point import Point
from django.contrib.gis.geos.linestring import LineString
import unittest
import mock
import networkx as nx

import indoor.navigation as nav
from indoor.models import Building, Floor, POI, Path
from api.models import Landmark

class NavigationTest(TestCase):

    def setUp(self):
        self.landmark = Landmark.objects.create(name='TEST')
        self.building = Building.objects.create(name='test')

        for i in range(5):
            floor = Floor.objects.create(name=str(i), level=i,
                                         building=self.building)
            POI.objects.create(name='ST_' + str(i), floor=floor,
                               type='stair', geom=Point(1, 1))
            POI.objects.create(name='RM_' + str(i), floor=floor,
                               type='room', geom=Point(2, 2))
            POI.objects.create(name='EL_' + str(i), floor=floor,
                               type='elevator', geom=Point(3, 3))
            Path.objects.create(path_id=1, floor=floor,
                                geom=LineString((1, 1), (2, 2)))
            Path.objects.create(path_id=1, floor=floor,
                                geom=LineString((2, 2), (3, 3)))

        self.floors = Floor.objects.all()

        building_graph = nav.generate_building_graph(self.building)
        self.building.graph_pickled_data = building_graph
        self.building.save()


    def tearDown(self):
        pass


    def test_generate_floor_graph(self):
        floor = Floor.objects.get(building__name=self.building.name,
                                  name=self.floors[0].name)

        floor_graph = nav.generate_floor_graph(floor)
        self.assertIsInstance(floor_graph, nx.Graph)

        for node in floor_graph.nodes():
            self.assertIsInstance(node, tuple)
            self.assertEqual(node[2], self.floors[0].name)

        names = nx.get_node_attributes(floor_graph, 'name').values()
        for poi in POI.objects.filter(floor=floor):
            self.assertIn(poi.name, names)

        edge_types = nx.get_edge_attributes(floor_graph, 'type').values()
        for e in edge_types:
            self.assertEqual('path', e)


    def test_generate_building_graph(self):
        building_graph = nav.generate_building_graph(self.building)
        self.assertIsInstance(building_graph, nx.Graph)

        names = nx.get_node_attributes(building_graph, 'name').values()
        for poi in POI.objects.filter(floor__building=self.building):
            self.assertIn(poi.name, names)

        edge_types = nx.get_edge_attributes(building_graph, 'type').values()
        for e in edge_types:
            self.assertIn(e, ['path', 'stair', 'elevator'])


    def test_get_building_graph_equals_generated(self):
        generated = nav.generate_building_graph(self.building)
        saved = nav.get_building_graph(self.building, True, True)
        
        matcher = lambda a,b: cmp(a,b) == 0
        self.assertTrue(nx.is_isomorphic(generated, saved, matcher, matcher))


    def test_get_building_graph_no_elevator(self):
        building_graph = nav.get_building_graph(self.building, True, False)
        edge_types = nx.get_edge_attributes(building_graph, 'type').values()
        for e in edge_types:
            self.assertIn(e, ['path', 'stair'])


    def test_get_building_graph_no_stairs(self):
        building_graph = nav.get_building_graph(self.building, False, True)
        edge_types = nx.get_edge_attributes(building_graph, 'type').values()
        for e in edge_types:
            self.assertIn(e, ['path', 'elevator'])


    def test_get_building_graph_no_elevators_or_stairs(self):
        building_graph = nav.get_building_graph(self.building, False, False)
        edge_types = nx.get_edge_attributes(building_graph, 'type').values()
        for e in edge_types:
            self.assertEqual(e, 'path')


    def test_format_route_output(self):
        # RM_0 -> ST_0 -> ST_2 -> RM_2 -> EL_2
        graph = self.building.graph_pickled_data
        path = nx.shortest_path(graph, (2, 2, '0'), (3, 3, '2'),
                                weight='weight')

        paths, floors = nav.format_route_output(graph, path)

        expected_paths = [
            [(2, 2), (1, 1)],
            [(1, 1), (2, 2), (3, 3)],
        ]
        expected_floors = ['0', '2']

        self.assertEqual(expected_paths, paths)
        self.assertEqual(expected_floors, floors)


    @mock.patch('indoor.navigation.get_building_graph')
    def test_elevator_threshold(self, mock_get_building_graph):
        # should use stairs
        nav.ELEVATOR_THRESHOLD = 4
        high_threshold_graph = nav.generate_building_graph(self.building)
        mock_get_building_graph.return_value = high_threshold_graph
        path, floors = nav.route('test', 'RM_0', 'RM_4', True, True)
        for floor_path in path:
            self.assertNotIn((3, 3), floor_path)

        # should use elevator
        nav.ELEVATOR_THRESHOLD = 3
        low_threshold_graph = nav.generate_building_graph(self.building)
        mock_get_building_graph.return_value = low_threshold_graph
        path, floors = nav.route('test', 'RM_0', 'RM_4', True, True)
        for floor_path in path:
            self.assertNotIn((1, 1), floor_path)
