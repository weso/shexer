import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "disable_or" + pth.sep

class TestAllowRedundantOr(unittest.TestCase):

    def test_or_enabled_choice_useful_IRI_redundant_disabled(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g3_or_example.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False,
                        allow_redundant_or=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_enabled_useful_IRI.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))

    def test_or_enabled_choice_useful_IRI_redundant_enabled(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g3_or_example.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False,
                        allow_redundant_or=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "redundant_enabled_useful_IRI.shex",
                                                      str_target=str_result,
                                                      or_shapes=True))

    def test_or_enabled_choice_expendable_IRI_redundant_enabled(self):
        shaper = Shaper(graph_file_input=_BASE_DIR + "g_or_example_expandable_IRI.ttl",
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=True,
                        input_format=TURTLE,
                        disable_comments=True,
                        disable_or_statements=False,
                        allow_redundant_or=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_enabled.shex",  # IRI should not be included
                                                      str_target=str_result,
                                                      or_shapes=True))

    def test_or_disabled_redundant_enabled(self):
        try:
            shaper = Shaper(graph_file_input=_BASE_DIR + "g3_or_example.ttl",
                            namespaces_dict=default_namespaces(),
                            all_classes_mode=True,
                            input_format=TURTLE,
                            disable_comments=True,
                            disable_or_statements=True,
                            allow_redundant_or=True)
            self.fail("This shouldn't execute, the configuration or_disabled + allow_redundant makes no sense")
        except ValueError:
            pass