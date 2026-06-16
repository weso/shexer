import unittest
from shexer.shaper import Shaper
from test.const import default_namespaces
from test.t_utils import number_of_shapes


class TestUrlEndpoint(unittest.TestCase):

    """
    These test cannot be too precise, since they are made against "live" content in Wikidata and DBpedia.

    """

    def test_wikidata(self):
        shape_map_raw = "SPARQL'select ?p where " \
                        "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
                        "LIMIT 1'@<Flag>"
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

    def test_dbpedia(self):
        shape_map_raw = "SPARQL'select ?s where {?s a <http://dbpedia.org/ontology/Person>} LIMIT 1'@<Flag>"
        shaper = Shaper(shape_map_raw=shape_map_raw,
                        url_endpoint="https://dbpedia.org/sparql",
                        namespaces_dict=default_namespaces(),
                        disable_comments=True,
                        depth_for_building_subgraph=1,
                        track_classes_for_entities_at_last_depth_level=False,
                        all_classes_mode=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) == 1)

    def test_all_classes_mode(self):
        # shape_map_raw = "SPARQL'select ?s where {?s a <http://dbpedia.org/ontology/Person>} LIMIT 1'@<Flag>"
        shaper = Shaper(all_classes_mode=True,
                        url_endpoint="https://agrovoc.fao.org/sparql",
                        namespaces_dict=default_namespaces(),
                        disable_comments=True,
                        depth_for_building_subgraph=1,
                        track_classes_for_entities_at_last_depth_level=False,
                        limit_remote_instances=5)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) > 2)


