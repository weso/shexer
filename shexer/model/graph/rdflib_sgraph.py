from rdflib import URIRef, Graph
from rdflib.util import from_n3
from shexer.model.graph.abstract_sgraph import SGraph
from shexer.utils.uri import add_corners_if_it_is_an_uri, remove_corners
from shexer.core.instances.pconsts import _S, _P, _O
from shexer.consts import RDF_TYPE



class RdflibSgraph(SGraph):

    def __init__(self, rdflib_graph=None, source_file=None, raw_graph=None, format="turtle"):
        """
        Pass an rdflib.Graph object or the params source_file and format to parse a local rdf

        :param rdflib_graph:
        :param source_file:
        :param format:
        """
        super().__init__()
        self._rdflib_graph = rdflib_graph if rdflib_graph is not None else self._build_rdflib_graph(source=source_file,
                                                                                                    raw_graph=raw_graph,
                                                                                                    format=format)

    def query_single_variable(self, str_query, variable_id):
        rows_res = self._rdflib_graph.query(str_query)
        return [str(a_row[0]) for a_row in rows_res]

    def serialize(self, path, format):
        self._rdflib_graph.serialize(destination=path,
                                     format=format)

    def yield_p_o_triples_of_an_s(self, target_node):
        for s, p ,o in self._rdflib_graph.triples((URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)),
                                                   None,
                                                   None)):
            yield s.n3(), p.n3(), o.n3()

    def yield_s_p_triples_of_an_o(self, target_node):
        for s, p, o in self._rdflib_graph.triples((None,
                                                   None,
                                                   URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)))):
            yield s.n3(), p.n3(), o.n3()


    def yield_class_triples_of_an_s(self, target_node, instantiation_property):
        for s ,p, o in self._rdflib_graph.triples((URIRef(remove_corners(a_uri=target_node,
                                                                         raise_error_if_no_corners=False)),
                                                   URIRef(remove_corners(a_uri=instantiation_property,
                                                                         raise_error_if_no_corners=False)),
                                                   None)):
            yield s.n3(), p.n3(), o.n3()

    def add_triple(self, a_triple):
        """
        It receives a tuple of 3 string elements. It adds it to the local rdflib graph
        :param a_triple:
        :return:
        """

        self._rdflib_graph.add(tuple(from_n3(add_corners_if_it_is_an_uri(a_token))
                                     for a_token in (a_triple[_S], a_triple[_P], a_triple[_O])))

    def yield_classes_with_instances(self, instantiation_property=RDF_TYPE):
        result = set()
        for s ,_, _ in self._rdflib_graph.triples((None,
                                                   URIRef(remove_corners(a_uri=instantiation_property,
                                                                         raise_error_if_no_corners=False)),
                                                   None)):
            result.add(str(s))
        for elem in result:
            yield elem


    def _build_rdflib_graph(self, source, raw_graph, format):
        result = Graph()
        if source is not None:
            result.parse(source=source, format=format)
        else:
            result.parse(data=raw_graph, format=format)
        return result