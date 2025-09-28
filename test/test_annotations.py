import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
from shexer.consts import ALL_EXAMPLES, MIXED_INSTANCES
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "annotations" + pth.sep  # We just need something with another instantiation property


class TestAnnotations(unittest.TestCase):
    def test_all_classes_g1_with_freq_annotations(self):
        namespaces = default_namespaces()
        namespaces["http://weso.es/shexer/ontology/"] = "shexer"
        shaper = Shaper(
            graph_file_input=G1,
            namespaces_dict=namespaces,
            all_classes_mode=True,
            examples_mode=ALL_EXAMPLES,
            input_format=TURTLE,
            instances_report_mode=MIXED_INSTANCES,
            disable_comments=False,
            detect_minimal_iri=True,
            comments_to_annotations=True,
            absolute_counts_property="http://weso.esss/ABS",
            example_conformance_property="http://weso.esss/CONF",
            frequency_property="http://weso.esss/RAT",
            extra_info_property="http://weso.esss/EXTRA"
        )
        str_result = shaper.shex_graph(string_output=True)
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "g1_freq_annotations.shex",
                                                      str_target=str_result))

