import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "repeated_names" + pth.sep  # We just need something with another instantiation property


class TestRepeatedShapeNames(unittest.TestCase):

    def test_potentially_repeated_shape_name(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "two_person_classes.ttl",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "two_person_classes.shex",
                                                      str_target=str_result)
                        or
                        file_vs_str_tunned_comparison(file_path=_BASE_DIR + "two_person_classes_op2.shex",
                                                      str_target=str_result)
                        )  # There is a non-deterministic part. Different shape names could be generated
                           # depending on the first shape explored

