import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES
from test.t_utils import graph_comparison_file_vs_str, text_contains_lines
import os.path as pth
from shexer.consts import SHACL_TURTLE

_BASE_DIR = BASE_FILES + "wikidata_annotation" + pth.sep


class TestAnnotation(unittest.TestCase):


    def test_no_annotation(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "wiki_example.ttl",
                        instantiation_property="http://www.wikidata.org/prop/direct/P31",
                        input_format="turtle",
                        disable_comments=True,
                        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "wiki_example_noanot_shacl.ttl",
                                                     str_target=str_result))

    def test_annotation(self):
        shaper = Shaper(all_classes_mode=True,
                        graph_file_input=_BASE_DIR + "wiki_example.ttl",
                        instantiation_property="http://www.wikidata.org/prop/direct/P31",
                        input_format="turtle",
                        disable_comments=True,
                        wikidata_annotation=True
                        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "wiki_example_noanot_shacl.ttl",
                                                     str_target=str_result))
        self.assertTrue(text_contains_lines(text=str_result,
                                            list_lines=[
                                                "# P31  -->  instance of",
                                                "# Q11689315  -->  hipopotams",
                                                "# Q215627  -->  person",
                                                "# Q5  -->  human"
                                            ]))
