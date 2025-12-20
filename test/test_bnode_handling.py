import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE_ITER, NT



_BASE_DIR = BASE_FILES + "bnodes" + pth.sep  # We just need something with another instantiation property


class TestBNodeHandling(unittest.TestCase):

    def test_format_turtle_iter(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "bnode_people.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_bnode_people.shex",
                                                      str_target=str_result,
                                                      strict=False))

    def test_format_nt(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "bnode_people.nt",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_bnode_people.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_some_bnodes_dont_have_shape(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_some_bnodes_dont_have_shape.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_people_some_bnodes_dont_have_shape.shex",
                                                      str_target=str_result,
                                                      strict=False))

    def test_some_bnodes_dont_have_shape_comments(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_some_bnodes_dont_have_shape.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue("100.0 % obj: BNode" in str_result)
        self.assertTrue("50.0 % obj: @:person" in str_result)

    def test_target_mixes_bnodes_and_iris(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_and_iris.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(
            file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_bnode_people.shex",
                                          str_target=str_result))

    def test_target_mixes_bnodes_and_iris_comments(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_and_iris.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=False,
            decimals=2)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue("66.67 % obj: @:person" in str_result)
        self.assertTrue("33.33 % obj: BNode" in str_result)
        self.assertTrue("33.33 % obj: IRI" in str_result)

    def test_target_mixes_bnodes_iris_and_no_shapes(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_iris_and_no_shapes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(
            file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_people_target_mixes_bnodes_iris_and_no_shapes.shex",
                                          str_target=str_result))

    def test_target_mixes_bnodes_iris_and_no_shapes_comments(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_iris_and_no_shapes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=False,
            decimals=2)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue("66.67 % obj: @:person" in str_result)
        self.assertTrue("66.67 % obj: BNode" in str_result)
        self.assertTrue("33.33 % obj: IRI" in str_result)

    def test_enable_or_but_it_is_not_useful(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "bnode_people.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            disable_or_statements=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_bnode_people.shex",
                                                      str_target=str_result))

    def test_enable_or_without_redundant(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_some_bnodes_dont_have_shape.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_or_statements=False,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_people_some_bnodes_dont_have_shape.shex",
                                                      str_target=str_result,
                                                      strict=False))

    def test_enable_or_with_redundant_only_bnodes(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_some_bnodes_dont_have_shape.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_or_statements=False,
            allow_redundant_or=True,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_with_redundant_bnodes_and_shapes.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_enable_or_without_redundant_with_shapes_bnodes_and_iris(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_iris_and_no_shapes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            disable_or_statements=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(
            file_vs_str_tunned_comparison(file_path=_BASE_DIR + "schema_people_target_mixes_bnodes_iris_and_no_shapes.shex",
                                          str_target=str_result))

    def test_enable_or_with_redundant_with_shapes_bnodes_and_iris(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_iris_and_no_shapes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            disable_or_statements=False,
            allow_redundant_or=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(
            file_vs_str_tunned_comparison(file_path=_BASE_DIR + "or_with_redundant_bnodes_iris_and_shapes.shex",
                                          str_target=str_result))

    def test_enable_or_with_redundant_with_shapes_bnodes_and_iris_comments(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "people_target_mixes_bnodes_iris_and_no_shapes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=False,
            decimals=2,
            disable_or_statements=False,
            allow_redundant_or=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue("66.67 % obj: @:person" in str_result)
        self.assertTrue("66.67 % obj: BNode" in str_result)
        self.assertTrue("33.33 % obj: IRI" in str_result)



