import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces
from test.t_utils import file_vs_str_tunned_comparison, file_vs_str_shex_exact_comparison_excluding_prefixes
from shexer.consts import ALL_EXAMPLES, SHAPE_EXAMPLES, CONSTRAINT_EXAMPLES, ABSOLUTE_INSTANCES, EXAMPLE_CONFORMANCE_PROP
import os.path as pth

from shexer.consts import TURTLE

_BASE_DIR = BASE_FILES + "example_features" + pth.sep


class TestExamplesMode(unittest.TestCase):

    def test_examples_disabled(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            examples_mode=None)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "determ_no_examples_no_inverse.shex",
                                                      str_target=str_result))

    def test_constraint_examples_no_inverse(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=CONSTRAINT_EXAMPLES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(file_path=_BASE_DIR + "determ_constraint_examples_no_inverse.shex",
                                                                             str_target=str_result))

    def test_constraint_examples_with_inverse(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=CONSTRAINT_EXAMPLES,
            inverse_paths=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(file_path=_BASE_DIR + "determ_constraint_examples_with_inverse.shex",
                                                                             str_target=str_result))

    def test_shape_examples_no_instance_stats(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_instance_single_prop.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=SHAPE_EXAMPLES,
            inverse_paths=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(
            file_path=_BASE_DIR + "determ_single_instance_single_prop_only_shape_examples_no_count.shex",
            str_target=str_result))

    def test_shape_examples_with_instance_stats(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_instance_single_prop.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=SHAPE_EXAMPLES,
            inverse_paths=False,
            instances_report_mode=ABSOLUTE_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_shex_exact_comparison_excluding_prefixes(
            file_path=_BASE_DIR + "determ_single_instance_single_prop_only_shape_examples_with_count.shex",
            str_target=str_result))

    def test_all_examples_with_instance_stats(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_instance_2_prop.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=ALL_EXAMPLES,
            inverse_paths=False,
            instances_report_mode=ABSOLUTE_INSTANCES)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue('// rdfs:comment "22" ;' in str_result)
        self.assertTrue(":Person   # 1 instance." in str_result)
        self.assertTrue("// <{}> ex:Jimmy".format(EXAMPLE_CONFORMANCE_PROP) in str_result)

    def test_all_examples_no_instance_stats(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_instance_2_prop.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            examples_mode=ALL_EXAMPLES,
            inverse_paths=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue('// rdfs:comment "22" ;' in str_result)
        self.assertTrue("// <{}> ex:Jimmy".format(EXAMPLE_CONFORMANCE_PROP) in str_result)
        self.assertFalse("<{}>   # 1 instance." in str_result)



