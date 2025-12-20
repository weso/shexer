import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

_BASE_DIR = BASE_FILES + "target_classes" + pth.sep

class TestFileTargetClasses(unittest.TestCase):

    def test_one_target(self):
        shaper = Shaper(file_target_classes=_BASE_DIR + "input_classes_one_target.tsv",
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "one_target.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_several_targets(self):
        shaper = Shaper(file_target_classes=_BASE_DIR + "input_classes_two_targets.tsv",
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "two_targets.shex",
                                                      str_target=str_result,
                                                      strict=False))

    # NOT SUPPORTED YET
    #
    def test_one_target_prefixed_targets(self):
        shaper = Shaper(file_target_classes=_BASE_DIR + "input_classes_one_target_prefixed.tsv",  # Not written yet
                        namespaces_dict={"http://xmlns.com/foaf/0.1/" : "foaf"},
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "one_target.shex",
                                                      str_target=str_result,
                                                      strict=False))
