from rdflib.graph import Graph, URIRef, Literal, BNode
from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.consts import N3, TURTLE, RDF_XML, NT, JSON_LD, ZIP, GZ, XZ

from shexer.model.Literal import Literal as model_Literal
from shexer.model.IRI import IRI as model_IRI
from shexer.model.bnode import BNode as model_BNode
from shexer.model.property import Property as model_Property

from shexer.utils.literal import decide_literal_type
from shexer.utils.compression import get_content_gz_file, get_content_zip_internal_file, get_content_xz_file

_SUPPORTED_FORMATS = [N3, TURTLE, RDF_XML, NT, JSON_LD]

_XML_WRONG_URI = "http://www.w3.org/XML/1998/namespace"


class RdflibTripleYielder(BaseTriplesYielder):
    def __init__(self, rdflib_graph, namespaces_dict=None):
        super().__init__()
        self._rdflib_graph = rdflib_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._triples_count = 0

        self._prefixes_parsed = False

    def yield_triples(self, parse_namespaces=True):
        self._reset_count()
        tmp_graph = self._get_tmp_graph()
        if parse_namespaces:
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        for sub, pred, obj in tmp_graph:
            yield (
                self._turn_rdflib_token_into_model_obj(sub),
                self._turn_rdflib_prop_into_model_obj(pred),
                self._turn_rdflib_token_into_model_obj(obj)
            )
            self._triples_count += 1

    @property
    def rdflib_graph(self):
        return self._rdflib_graph


    def _turn_rdflib_token_into_model_obj(self, rdflib_obj):
        if type(rdflib_obj) == URIRef:
            return model_IRI(str(rdflib_obj))
        elif type(rdflib_obj) == Literal:
            return self._turn_into_model_literal(rdflib_obj)
        elif type(rdflib_obj) == BNode:
            return model_BNode(identifier=str(rdflib_obj))
        else:
            raise ValueError("Not recognized type of rdflib element: " + type(rdflib_obj) + " ( " + str(rdflib_obj) + " )")

    def _turn_rdflib_prop_into_model_obj(self, rdflib_obj):
        if type(rdflib_obj) == URIRef:
            return model_Property(str(rdflib_obj))
        else:
            raise ValueError("Trying to convert into a model property en element which is not "
                             "supposed to be a property: " + type(rdflib_obj) + " ( " + str(rdflib_obj) + " )")

    def _get_tmp_graph(self):
        return self._rdflib_graph

    @staticmethod
    def _integrate_namespaces_from_parsed_graph(a_graph, namespaces_dict):

        for a_prefix_namespace_tuple in a_graph.namespaces():
            candidate_uri = str(a_prefix_namespace_tuple[1])
            if candidate_uri not in namespaces_dict:
                if candidate_uri == _XML_WRONG_URI:  # XML fix...
                    candidate_uri += "/"             # XML fix...
                namespaces_dict[candidate_uri] = str(a_prefix_namespace_tuple[0])
            # There is no else here. In case of conflict between the parsed content and the dict provided by the user,
            # the user's one have priority


    @staticmethod
    def _turn_into_model_literal(rdflib_literal):
        content = str(rdflib_literal)
        if rdflib_literal.language is not None:
            content = '"' + content + '"@' + rdflib_literal.language
        return model_Literal(content=content,
                             elem_type=str(rdflib_literal.datatype)
                             if rdflib_literal.datatype is not None
                             else decide_literal_type(content))


    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return 0  # With rdflib, a single error will cause to fail the parsing process


    @property
    def namespaces(self):
        if not self._prefixes_parsed:
            tmp_graph = self._get_tmp_graph()
            self._integrate_namespaces_from_parsed_graph(tmp_graph, self._namespaces_dict)
            self._prefixes_parsed = True
        return self._namespaces_dict


    def _reset_count(self):
        self._triples_count = 0


class RdflibParserTripleYielder(RdflibTripleYielder):

    def __init__(self, input_format=TURTLE, source=None, allow_untyped_numbers=False, raw_graph=None,
                 namespaces_dict=None, compression_mode=None, zip_archive_file=None):
        """

        :param input_format:
        :param source: It can be local (a file path) or remote (an url to download some content)
        :param namespaces_to_ignore:
        :param allow_untyped_numbers:
        :param raw_graph:
        :param namespaces_dict:
        """

        super().__init__(rdflib_graph=None,
                         namespaces_dict=namespaces_dict)
        self._check_input_format(input_format)
        self._input_format = input_format
        self._source = source
        self._compression_mode = compression_mode
        self._zip_archive_file = zip_archive_file
        self._allow_untyped_numbers = allow_untyped_numbers
        self._raw_graph = raw_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
                                              # This object can be modified (and will be consumed externaly)
                                              # when parse_namespaces in yiled_triples() is set to True

        self._triples_count = 0

        self._prefixes_parsed = False


    def _get_tmp_graph(self):
        result = Graph()
        if self._compression_mode is not None:
            self._parse_compressed_files(result)
        elif self._source is not None:
            result.parse(source=self._source, format=self._input_format)
        else:
            result.parse(data=self._raw_graph, format=self._input_format)
        return result

    def _parse_compressed_files(self, rdflib_graph):
        if self._compression_mode == GZ:
            rdflib_graph.parse(data=get_content_gz_file(self._source), format=self._input_format)
        elif self._compression_mode == ZIP:
            rdflib_graph.parse(data=get_content_zip_internal_file(base_archive=self._zip_archive_file,
                                                                  target_file=self._source),
                               format=self._input_format)
        elif self._compression_mode == XZ:
            rdflib_graph.parse(data=get_content_xz_file(self._source), format=self._input_format)
        else:
            raise ValueError("Unknown compression format")

    @staticmethod
    def _check_input_format(input_format):
        if input_format not in _SUPPORTED_FORMATS:
            raise ValueError("Unsupported input format: " + input_format)





