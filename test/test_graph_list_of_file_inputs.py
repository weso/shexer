import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, G1_NT, default_namespaces, BASE_FILES_GENERAL
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import NT, TURTLE

_BASE_DIR = BASE_FILES + "graph_list_of_files_input" + pth.sep

class TestGraphListOfFilesInput(unittest.TestCase):

    def test_one_turtle(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_list_of_files_input=[G1],
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_one_nt(self):  # Should be nt
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_list_of_files_input=[G1_NT],
                        namespaces_dict=default_namespaces(),
                        input_format=NT,
                        all_classes_mode=False,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_several_nt(self):  # Should be nt
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_list_of_files_input=[_BASE_DIR + "g1_p1.nt",
                                                   _BASE_DIR + "g1_p2.nt"],
                        namespaces_dict=default_namespaces(),
                        input_format=NT,
                        all_classes_mode=False,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_several_turtle(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_list_of_files_input=[_BASE_DIR + "g1_p1.ttl",
                                                   _BASE_DIR + "g1_p2.ttl"],
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result,
                                                      strict=False))
