import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE



_BASE_DIR = BASE_FILES + "instantiation_prop" + pth.sep  # We just need something with another instantiation property


class TestRepeatedShapeNames(unittest.TestCase):

    def test_potentially_repeated_shape_name(self):
        input = """
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Jimmy a foaf:Person ;  
	foaf:age "23"^^xsd:integer ;
	foaf:name "Jimmy" ;
	foaf:familyName "Jones" .

ex:Sarah a ex:Person ;  
	ex:age 22 ;
	ex:name "Sarah" ;
	ex:familyName "Salem" .

"""

        shaper = Shaper(
            raw_graph=input,
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        print(str_result)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

