import unittest
from shexer.shaper import Shaper
from test.const import BASE_FILES
from test.t_utils import rdflib_exist_triple, rdflib_counts_triples
import os.path as pth
from shexer.consts import SHACL_TURTLE
from rdflib import Graph

_BASE_DIR = BASE_FILES + "shacl" + pth.sep


class TestShapeMapCompatibility(unittest.TestCase):

    def test_shape_map_compatibility_single_node(self):
        shape_map_raw = "<http://dbpedia.org/resource/Ladilla_Rusa>@<http://example.org/shapes/MusicGroup>"

        shaper = Shaper(
            shape_map_raw=shape_map_raw,
            url_endpoint="https://dbpedia.org/sparql",
            instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            namespaces_dict={
                "http://dbpedia.org/resource/": "dbr",
                "http://dbpedia.org/ontology/": "dbo",
                "http://www.w3.org/2001/XMLSchema#": "xsd",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                "http://www.w3.org/2000/01/rdf-schema#": "rdfs"
            },
            disable_comments=True
        )
        str_result = shaper.shex_graph(string_output=True, output_format=SHACL_TURTLE)
        graph = Graph()
        graph.parse(data=str_result)
        self.assertTrue(rdflib_exist_triple(graph=graph,
                                            t_subject="<http://example.org/shapes/MusicGroup>",
                                            t_predicate="<http://www.w3.org/ns/shacl#targetNode>",
                                            t_object="<http://dbpedia.org/resource/Ladilla_Rusa>"))

    def test_shape_map_compatibility_sparql_selector(self):
        shape_map_raw = "SPARQL'select ?s where {?s a <http://dbpedia.org/ontology/MusicalArtist>} LIMIT 2'" \
                        "@<http://example.org/shapes/MusicGroup>"

        shaper = Shaper(
            shape_map_raw=shape_map_raw,
            url_endpoint="https://dbpedia.org/sparql",
            track_classes_for_entities_at_last_depth_level=False,
            depth_for_building_subgraph=1,
            instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            namespaces_dict={
                "http://dbpedia.org/resource/": "dbr",
                "http://dbpedia.org/ontology/": "dbo",
                "http://www.w3.org/2001/XMLSchema#": "xsd",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                "http://www.w3.org/2000/01/rdf-schema#": "rdfs"
            },
            disable_comments=True
        )
        str_result = shaper.shex_graph(string_output=True, output_format=SHACL_TURTLE)
        graph = Graph()
        graph.parse(data=str_result)
        self.assertTrue(rdflib_counts_triples(graph=graph,
                                              t_subject="<http://example.org/shapes/MusicGroup>",
                                              t_predicate="<http://www.w3.org/ns/shacl#targetNode>",
                                              t_object=None) == 2)

    def test_shape_map_compatibility_focus_expression(self):
        shape_map_raw = "{dbr:Felipe_VI dbo:predecessor FOCUS}" \
                        "@<http://example.org/shapes/Someone>"
        # We are assuming in this test that this information won't change in DBpedia:
        # Felipe VI has a single predecessor (dbr:Juan_Carlos_I)

        shaper = Shaper(
            shape_map_raw=shape_map_raw,
            url_endpoint="https://dbpedia.org/sparql",
            track_classes_for_entities_at_last_depth_level=False,
            depth_for_building_subgraph=1,
            instantiation_property="http://www.w3.org/1999/02/22-rdf-syntax-ns#type",
            namespaces_dict={
                "http://dbpedia.org/resource/": "dbr",
                "http://dbpedia.org/ontology/": "dbo",
                "http://www.w3.org/2001/XMLSchema#": "xsd",
                "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                "http://www.w3.org/2000/01/rdf-schema#": "rdfs"
            },
            disable_comments=True
        )
        str_result = shaper.shex_graph(string_output=True, output_format=SHACL_TURTLE)
        graph = Graph()
        graph.parse(data=str_result)
        self.assertTrue(rdflib_counts_triples(graph=graph,
                                              t_subject="<http://example.org/shapes/Someone>",
                                              t_predicate="<http://www.w3.org/ns/shacl#targetNode>",
                                              t_object=None) == 1)
