import unittest
from shexer.shaper import Shaper
from shexer.utils.uri import prefixize_uri_if_possible, add_corners_if_it_is_an_uri
from shexer.utils.dict import reverse_keys_and_values
from test.const import G1, BASE_FILES, default_namespaces
from test.t_utils import graph_comparison_file_vs_str
from shexer.consts import ALL_EXAMPLES, MIXED_INSTANCES, ABSOLUTE_INSTANCES, RATIO_INSTANCES, CONSTRAINT_EXAMPLES, \
    SHAPE_EXAMPLES, EXAMPLE_CONFORMANCE_PROP, ABSOLUTE_COUNT_PROP, EXTRA_INFO_PROP, FREQ_PROP, SHACL_TURTLE
import os.path as pth

from shexer.consts import TURTLE, TURTLE_ITER



_BASE_DIR = BASE_FILES + "annotations" + pth.sep  # We just need something with another instantiation property


class TestAnnotations(unittest.TestCase):

    def _namespaces_for_test(self, reverse=False):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        if reverse:
            return reverse_keys_and_values(namespaces)
        return namespaces
    def _example_prop(self):
        return add_corners_if_it_is_an_uri(prefixize_uri_if_possible(
            target_uri=EXAMPLE_CONFORMANCE_PROP,
            namespaces_prefix_dict=self._namespaces_for_test(reverse=False),
            corners=False))
    def _ratio_prop(self):
        return add_corners_if_it_is_an_uri(prefixize_uri_if_possible(
            target_uri=FREQ_PROP,
            namespaces_prefix_dict=self._namespaces_for_test(reverse=False),
            corners=False)
        )

    def _abs_prop(self):
        return add_corners_if_it_is_an_uri(prefixize_uri_if_possible(
            target_uri=ABSOLUTE_COUNT_PROP,
            namespaces_prefix_dict=self._namespaces_for_test(reverse=False),
            corners=False))

    def _extra_prop(self):
        return add_corners_if_it_is_an_uri(prefixize_uri_if_possible(
            target_uri=EXTRA_INFO_PROP,
            namespaces_prefix_dict=self._namespaces_for_test(reverse=False),
            corners=False))

    def test_all_classes_g1_no_annotations(self):
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=self._namespaces_for_test(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=False,
            generate_annotations=False
        )
        str_result = shaper.shex_graph(string_output=True, output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "g1_comments_no_annot.ttl",
                                                     str_target=str_result))

    def test_shape_examples(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=SHAPE_EXAMPLES,
            input_format=TURTLE_ITER,
            # instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_shape_examples.ttl",
                                                     str_target=str_result))


    def test_constraint_examples(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=CONSTRAINT_EXAMPLES,
            input_format=TURTLE_ITER,
            # instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_constraint_examples.ttl",
                                                     str_target=str_result))

    def test_all_examples(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            # instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_examples.ttl",
                                                     str_target=str_result))

    def test_ratios(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            # examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=RATIO_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_ratios.ttl",
                                                     str_target=str_result))

    def test_absolutes(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            # examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=ABSOLUTE_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_absolutes.ttl",
                                                     str_target=str_result))

    def test_mixed_report(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            # examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_mixed_report.ttl",
                                                     str_target=str_result))

    def test_all_examples_and_stats(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True,
            detect_minimal_iri=True
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_examples_stats.ttl",
                                                     str_target=str_result))

    def test_set_extra(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True,
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            # frequency_property="http://weso.esss/RAT",
            extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_set_extra.ttl",
                                                     str_target=str_result))

    def test_set_ratios(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True,
            # absolute_counts_property="http://weso.esss/ABS",
            # example_conformance_property="http://weso.esss/CONF",
            frequency_property="http://weso.esss/RAT"
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_set_ratios.ttl",
                                                     str_target=str_result))

    def test_set_examples(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True,
            # absolute_counts_property="http://weso.esss/ABS",
            example_conformance_property="http://weso.esss/CONF"
            # frequency_property="http://weso.esss/RAT"
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_set_examples.ttl",
                                                     str_target=str_result))

    def test_set_absolutes(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "single_class_deterministic_order.ttl",
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE_ITER,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            generate_annotations=True,
            absolute_counts_property="http://weso.esss/ABS"
            # example_conformance_property="http://weso.esss/CONF"
            # frequency_property="http://weso.esss/RAT"
            # extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True,
                                       output_format=SHACL_TURTLE)
        self.assertTrue(graph_comparison_file_vs_str(file_path=_BASE_DIR + "one_class_all_set_absolutes.ttl",
                                                     str_target=str_result))