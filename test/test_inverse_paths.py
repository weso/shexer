import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from test.t_utils import number_of_shapes

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "inverse_paths" + pth.sep  # We just need something with another instantiation property


class TestInversePaths(unittest.TestCase):

    def test_base_g1(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_inverse.shex",
                                                      str_target=str_result))

    def test_remote_wikidata(self):
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
                        all_classes_mode=False,
                        inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) == 1)
        self.assertTrue("^  <http://www.wikidata.org/prop/direct/P163>  IRI" in str_result)

