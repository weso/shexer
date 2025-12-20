import unittest
from shexer.shaper import Shaper
from test.const import default_namespaces, BASE_FILES_GENERAL
from test.t_utils import file_vs_str_tunned_comparison

from shexer.consts import TURTLE

raw_graph_nt = """<http://example.org/Jimmy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/Jimmy> <http://xmlns.com/foaf/0.1/age> "23"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/Jimmy> <http://xmlns.com/foaf/0.1/name> "Jimmy" .
<http://example.org/Jimmy> <http://xmlns.com/foaf/0.1/familyName> "Jones" .
<http://example.org/Sarah> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/Sarah> <http://xmlns.com/foaf/0.1/age> "22"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/Sarah> <http://xmlns.com/foaf/0.1/name> "Sarah" .
<http://example.org/Sarah> <http://xmlns.com/foaf/0.1/familyName> "Salem" .
<http://example.org/Bella> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/Bella> <http://xmlns.com/foaf/0.1/age> "56"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/Bella> <http://xmlns.com/foaf/0.1/name> "Isabella" .
<http://example.org/David> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Person> .
<http://example.org/David> <http://xmlns.com/foaf/0.1/name> "David" .
<http://example.org/David> <http://xmlns.com/foaf/0.1/familyName> "Doulofeau" .
<http://example.org/David> <http://xmlns.com/foaf/0.1/knows> <http://example.org/Sarah> .
<http://example.org/HumanLike> <http://xmlns.com/foaf/0.1/name> "Person" .
<http://example.org/HumanLike> <http://xmlns.com/foaf/0.1/familyName> "Maybe" .
<http://example.org/HumanLike> <http://xmlns.com/foaf/0.1/age> "99"^^<http://www.w3.org/2001/XMLSchema#integer> .
<http://example.org/HumanLike> <http://xmlns.com/foaf/0.1/knows> <http://example.org/David> .
<http://example.org/x1> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Document> .
<http://example.org/x1> <http://xmlns.com/foaf/0.1/depiction> "A thing that s nice" .
<http://example.org/x1> <http://xmlns.com/foaf/0.1/title> "A nice thing" .
<http://example.org/x2> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://xmlns.com/foaf/0.1/Document> .
<http://example.org/x2> <http://xmlns.com/foaf/0.1/title> "Another thing" ."""

raw_graph_turtle = """@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix ex: <http://example.org/> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:Jimmy a foaf:Person ;  # Complete
	foaf:age "23"^^xsd:integer ;
	foaf:name "Jimmy" ;
	foaf:familyName "Jones" .

ex:Sarah a foaf:Person ;  # Complete implicit type for age
	foaf:age 22 ;
	foaf:name "Sarah" ;
	foaf:familyName "Salem" .

ex:Bella a foaf:Person ;  # Missing familyName
	foaf:age "56"^^xsd:integer ;
	foaf:name "Isabella" .

ex:David a foaf:Person ;  # Missing age and use knows
	foaf:name "David" ;
	foaf:familyName "Doulofeau" ;
	foaf:knows ex:Sarah .

ex:HumanLike foaf:name "Person" ;  # foaf properties, but not explicit type.
	foaf:familyName "Maybe" ;
	foaf:age 99 ;
	foaf:knows ex:David .


ex:x1 rdf:type foaf:Document ;
	foaf:depiction "A thing that is nice" ;
	foaf:title "A nice thing" .


ex:x2 rdf:type foaf:Document ;
	foaf:title "Another thing" ."""


class TestGraphFileInput(unittest.TestCase):

    def test_some_format(self):
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        raw_graph=raw_graph_turtle,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        input_format=TURTLE,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result,
                                                      strict=False))


    def test_no_format(self):  # Should be nt
        shaper = Shaper(target_classes=["http://xmlns.com/foaf/0.1/Person",
                                        "http://xmlns.com/foaf/0.1/Document"],
                        raw_graph=raw_graph_nt,
                        namespaces_dict=default_namespaces(),
                        all_classes_mode=False,
                        disable_comments=True)
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex",
                                                      str_target=str_result))