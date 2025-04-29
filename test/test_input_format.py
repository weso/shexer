import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, G1_JSON_LD, G1_NT, G1_TSVO_SPO, G1_XML, G1_N3, \
    default_namespaces, G1_TTL_WITH_BASE, G1_TTL_WITH_USELESS_BNODE, G1_TTL_WITH_ABSOLUTES, \
    G1_TTL_WITH_SCAPED_QUOTES, G1_TTL_WITH_SCAPED_QUOTES_AND_MULTILINE, G1_TTL_WITH_MULTILINE_STR
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth
from shexer.consts import NT, TSV_SPO, RDF_XML, JSON_LD, N3, TURTLE, TURTLE_ITER

_BASE_DIR = BASE_FILES + "general" + pth.sep

class TestInputFormat(unittest.TestCase):

    def test_ttl(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_nt(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_NT,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=NT,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_n3(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_N3,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=N3,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_tsv_spo(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TSVO_SPO,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TSV_SPO,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_xml(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_XML,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=RDF_XML,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_json_ld(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_JSON_LD,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=JSON_LD,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_ttl_iter(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_ttl_iter_with_base(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_BASE,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_ttl_iter_with_bnode(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_USELESS_BNODE,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_ttl_iter_with_absolute_IRIs(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_ABSOLUTES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_ttl_iter_with_scaped_quotes(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_SCAPED_QUOTES,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))


    def test_ttl_iter_with_multiline_strs(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_MULTILINE_STR,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))

    def test_ttl_iter_with_multiline_strs_and_scaped_quotes(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1_TTL_WITH_SCAPED_QUOTES_AND_MULTILINE,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE_ITER,
                        disable_comments=True,
                        infer_numeric_types_for_untyped_literals=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))



