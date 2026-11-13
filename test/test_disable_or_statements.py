import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "disable_or" + pth.sep

class TestDisableOrStatements(unittest.TestCase):

    def test_or_enabled_choice_useful_IRI(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g3_or_example.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_enabled_useful_IRI.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))

    def test_or_enabled_choice_expendable_IRI(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g_or_example_expandable_IRI.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_enabled.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))

    def test_or_disabled(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g3_or_example.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_disabled.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))