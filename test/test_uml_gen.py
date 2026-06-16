import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import check_file_exist, delete_file, file_vs_str_tunned_comparison, number_of_shapes
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "uml" + pth.sep
_A_PATH_FOR_IMG = _BASE_DIR + "any_path.png"


class TestUmlGen(unittest.TestCase):

    def test_base_gen(self):
        delete_file(_A_PATH_FOR_IMG)  # pre-condition
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        shaper.shex_graph(to_uml_path=_A_PATH_FOR_IMG)
        try:
            check_file_exist(_A_PATH_FOR_IMG)
        finally:
            delete_file(_A_PATH_FOR_IMG)

    def test_gen_uml_and_classical_output(self):

        delete_file(_A_PATH_FOR_IMG)  # pre-condition
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(to_uml_path=_A_PATH_FOR_IMG, string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))
        try:
            check_file_exist(_A_PATH_FOR_IMG)
        finally:
            delete_file(_A_PATH_FOR_IMG)

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
        str_result = shaper.shex_graph(string_output=True, to_uml_path=_A_PATH_FOR_IMG)
        self.assertTrue(number_of_shapes(str_result) == 1)
        try:
            check_file_exist(_A_PATH_FOR_IMG)
        finally:
            delete_file(_A_PATH_FOR_IMG)

