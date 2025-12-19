import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "min_iri" + pth.sep  # We just need something with another instantiation property


class TestDetectMinimalIri(unittest.TestCase):

    def test_all_classes_g1_disabled(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_all_classes_g1_enabled(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments_min_iri.shex",
                                                      str_target=str_result))

    def test_g1_different_namespaces_per_class(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_namespaces_per_class.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_different_namespaces_per_class.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_g1_different_namespaces_per_instance(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_namespaces_per_instance.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_different_namespaces_per_instance.shex",
                                                      str_target=str_result,
                                                      strict=False))

    def test_g1_different_base_per_instance_no_sep_char(self):
        """
        :Person should be [http://example.org/ns1/], not [http://example.org/ns1/aa]
        :return:
        """
        shaper = Shaper(
            graph_file_input=_BASE_DIR+"g1_different_base_per_instance_no_sep_char.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            detect_minimal_iri=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_different_namespaces_per_class.shex",
                                                      str_target=str_result,
                                                      strict=False))

