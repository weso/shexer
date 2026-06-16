import unittest
from shexer.shaper import Shaper
from test.const import default_namespaces
from test.t_utils import number_of_shapes, shape_contains_constraint


class TestDepthBuildingSubGraph(unittest.TestCase):

    """
    These test cannot be too precise, since they are made against "live" content in Wikidata.
    Also, two of them are commented, as they consume too much time to finish

    """

    def test_1_not_all_classes_format(self):
        shape_map_raw = "SPARQL'select ?p where " \
                        "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
                        "LIMIT 10'@<Flag>"
        shaper = Shaper(shape_map_raw=shape_map_raw,
                        url_endpoint="https://qlever.dev/api/wikidata",
                        namespaces_dict=default_namespaces(),
                        instantiation_property="http://www.wikidata.org/prop/direct/P31",
                        disable_comments=True,
                        depth_for_building_subgraph=1,
                        track_classes_for_entities_at_last_depth_level=False,
                        all_classes_mode=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) == 1)
        self.assertTrue(shape_contains_constraint(target_str=str_result,
                                                  shape="<Flag>",
                                                  constraint="<http://www.wikidata.org/prop/direct/P31>  "
                                                             "[<http://www.wikidata.org/entity/Q14660>]"))

    def test_1_all_classes_format(self):
        shape_map_raw = "SPARQL'select ?p where " \
                        "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
                        "LIMIT 10'@<Flag>"
        shaper = Shaper(shape_map_raw=shape_map_raw,
                        url_endpoint="https://qlever.dev/api/wikidata",
                        namespaces_dict=default_namespaces(),
                        instantiation_property="http://www.wikidata.org/prop/direct/P31",
                        disable_comments=True,
                        depth_for_building_subgraph=1,
                        track_classes_for_entities_at_last_depth_level=False,
                        all_classes_mode=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) > 1)
        self.assertTrue(number_of_shapes(str_result) < 10)
        self.assertTrue(shape_contains_constraint(target_str=str_result,
                                                  shape="<Flag>",
                                                  constraint="<http://www.wikidata.org/prop/direct/P31>  "
                                                             "[<http://www.wikidata.org/entity/Q14660>]"))

    # def test_2_not_all_classes_format(self):
    #     shape_map_raw = "SPARQL'select ?p where " \
    #                     "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
    #                     "LIMIT 10'@<Flag>"
    #     shaper = Shaper(shape_map_raw=shape_map_raw,
    #                     url_endpoint="https://qlever.dev/api/wikidata",
    #                     namespaces_dict=default_namespaces(),
    #                     instantiation_property="http://www.wikidata.org/prop/direct/P31",
    #                     disable_comments=True,
    #                     depth_for_building_subgraph=2,
    #                     track_classes_for_entities_at_last_depth_level=False,
    #                     all_classes_mode=False)
    #     str_result = shaper.shex_graph(string_output=True)
    #     self.assertTrue(number_of_shapes(str_result) == 1)
    #     self.assertTrue(shape_contains_constraint(target_str=str_result,
    #                                               shape="<Flag>",
    #                                               constraint="<http://www.wikidata.org/prop/direct/P31>  "
    #                                                          "[<http://www.wikidata.org/entity/Q14660>]"))
    #
    # def test_2_all_classes_format(self):
    #     shape_map_raw = "SPARQL'select ?p where " \
    #                     "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
    #                     "LIMIT 10'@<Flag>"
    #     shaper = Shaper(shape_map_raw=shape_map_raw,
    #                     url_endpoint="https://qlever.dev/api/wikidata",
    #                     namespaces_dict=default_namespaces(),
    #                     instantiation_property="http://www.wikidata.org/prop/direct/P31",
    #                     disable_comments=True,
    #                     depth_for_building_subgraph=2,
    #                     track_classes_for_entities_at_last_depth_level=False,
    #                     all_classes_mode=True)
    #     str_result = shaper.shex_graph(string_output=True)
    #     self.assertTrue(number_of_shapes(str_result) > 10)
    #     self.assertTrue(shape_contains_constraint(target_str=str_result,
    #                                               shape="<Flag>",
    #                                               constraint="<http://www.wikidata.org/prop/direct/P31>  "
    #                                                          "[<http://www.wikidata.org/entity/Q14660>]"))