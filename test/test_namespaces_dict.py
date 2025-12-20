import unittest
from shexer.shaper import Shaper
from test.const import G1_NT, G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import TURTLE, NT

_BASE_DIR = BASE_FILES + "namespaces_dict" + pth.sep

class TestNamespacesDict(unittest.TestCase):

    def test_same_namespaces_as_source_ttl_file(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_no_foaf(self):
        namespaces = {"http://example.org/" : "ex",
                               "http://www.w3.org/XML/1998/namespace/" : "xml",
                               "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                               "http://www.w3.org/2000/01/rdf-schema#" : "rdfs",
                               "http://www.w3.org/2001/XMLSchema#": "xsd"
                               # "http://xmlns.com/foaf/0.1/": "foaf"
                               }
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_NT,
                        namespaces_dict=namespaces,
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + pth.sep +"no_foaf.shex",
                                                      str_target=str_result))

    def test_overwrite_empty(self):
        namespaces = default_namespaces()
        namespaces["http://unuseful.but.yet/here/"] = ""

        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=namespaces,
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + pth.sep +"overwrite_empty.shex",
                                                      str_target=str_result))

    def test_overwrite_some_namespaces(self):
        namespaces = {"http://example.org/": "ex",
                      "http://www.w3.org/XML/1998/namespace/": "xml",
                      "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                      "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
                      "http://www.w3.org/2001/XMLSchema#": "xxssdd",
                      "http://xmlns.com/foaf/0.1/": "fooo"
                      }

        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=namespaces,
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + pth.sep +"overwrite.shex",
                                                      str_target=str_result))
