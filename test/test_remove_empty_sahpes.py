import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison, number_of_shapes
import os.path as pth

_BASE_DIR = BASE_FILES + "empty_shapes" + pth.sep

class TestRemoveEmptyShapes(unittest.TestCase):

    def test_one_empty_remove(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Machine"],
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True,
                        remove_empty_shapes=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(number_of_shapes(str_result) == 0)

    def test_one_empty_not_remove(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Machine"],
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True,
                        remove_empty_shapes=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "one_empty_not_remove.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_some_empty_remove(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Machine",
                                        "http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True,
                        remove_empty_shapes=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result,
                                                      strict=False))

    def test_some_empty_not_remove(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Machine",
                                        "http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        graph_file_input=G1,
                        all_classes_mode=False,
                        input_format="turtle",
                        disable_comments=True,
                        remove_empty_shapes=False)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=_BASE_DIR + "some_empty_not_remove.shex",
                                                      str_target=str_result,
                                                      strict=False))
