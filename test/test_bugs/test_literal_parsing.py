import unittest
from rdflib import Graph
from shexer.io.sparql.query import build_term
from shexer.model.bnode import BNode
from shexer.model.graph.rdflib_sgraph import RdflibSgraph
from shexer.utils.literal import decide_literal_type, build_literal_token, unescape_literal_content, \
    XSD_NAMESPACE, LANG_STRING_TYPE, STRING_TYPE
from shexer.utils.triple_yielders import tune_token

_XSD_INT = XSD_NAMESPACE + "int"
_XSD_STRING = XSD_NAMESPACE + "string"
_XSD_ANY_URI = XSD_NAMESPACE + "anyURI"
_XSD_DOUBLE = XSD_NAMESPACE + "double"

_SARAH = "<http://example.org/sarah>"
_AGE = "<http://example.org/age>"
_NAME = "<http://example.org/name>"
_BIO = "<http://example.org/bio>"
_KNOWS = "<http://example.org/knows>"
_FRIEND = "<http://example.org/jim>"

_MULTILINE_VALUE = 'say "hi" \\o/\nline2\r\tend'


class TestBuildTerm(unittest.TestCase):

    def test_uri(self):
        self.assertEqual("<http://example.org/sarah>",
                         build_term({"type": "uri", "value": "http://example.org/sarah"}))

    def test_typed_literal(self):
        self.assertEqual('"30"^^<http://www.w3.org/2001/XMLSchema#int>',
                         build_term({"type": "literal", "value": "30", "datatype": _XSD_INT}))

    def test_typed_literal_legacy_json_format(self):
        self.assertEqual('"1.5"^^<http://www.w3.org/2001/XMLSchema#double>',
                         build_term({"type": "typed-literal", "value": "1.5", "datatype": _XSD_DOUBLE}))

    def test_lang_literal(self):
        self.assertEqual('"Sarah"@en',
                         build_term({"type": "literal", "value": "Sarah", "xml:lang": "en"}))

    def test_plain_literal(self):
        self.assertEqual('"Sarah"',
                         build_term({"type": "literal", "value": "Sarah"}))

    def test_literal_with_quotes_and_backslash(self):
        self.assertEqual('"say \\"hi\\" \\\\o/"',
                         build_term({"type": "literal", "value": 'say "hi" \\o/'}))

    def test_literal_with_line_breaks(self):
        self.assertEqual('"line1\\nline2\\r"',
                         build_term({"type": "literal", "value": "line1\nline2\r"}))

    def test_bnode(self):
        self.assertEqual("_:b0",
                         build_term({"type": "bnode", "value": "b0"}))


class TestBuildLiteralToken(unittest.TestCase):

    def test_plain(self):
        self.assertEqual('"Sarah"', build_literal_token("Sarah"))

    def test_lang(self):
        self.assertEqual('"Sarah"@en', build_literal_token("Sarah", lang="en"))

    def test_datatype(self):
        self.assertEqual('"30"^^<http://www.w3.org/2001/XMLSchema#int>',
                         build_literal_token("30", datatype=_XSD_INT))

    def test_escaped_characters(self):
        self.assertEqual('"say \\"hi\\" \\\\o/\\nline2\\r\tend"',
                         build_literal_token(_MULTILINE_VALUE))


class TestUnescapeLiteralContent(unittest.TestCase):

    def test_quote(self):
        self.assertEqual('say "hi"', unescape_literal_content('say \\"hi\\"'))

    def test_backslash(self):
        self.assertEqual("C:\\new", unescape_literal_content("C:\\\\new"))

    def test_line_breaks_and_tab(self):
        self.assertEqual("a\nb\rc\td", unescape_literal_content("a\\nb\\rc\\td"))

    def test_short_unicode_escape(self):
        self.assertEqual("caf\u00e9", unescape_literal_content("caf\\u00e9"))

    def test_long_unicode_escape(self):
        self.assertEqual("\U0001F600", unescape_literal_content("\\U0001F600"))

    def test_unknown_escape_is_kept(self):
        self.assertEqual("\\q", unescape_literal_content("\\q"))

    def test_truncated_unicode_escape_is_kept(self):
        self.assertEqual("\\u12", unescape_literal_content("\\u12"))

    def test_inverse_of_build_literal_token(self):
        self.assertEqual(_MULTILINE_VALUE,
                         unescape_literal_content(build_literal_token(_MULTILINE_VALUE)[1:-1]))


class TestDecideLiteralType(unittest.TestCase):

    def test_prefixed_datatype(self):
        self.assertEqual(_XSD_INT, decide_literal_type('"30"^^xsd:int'))

    def test_full_iri_datatype(self):
        self.assertEqual(_XSD_INT, decide_literal_type('"30"^^<http://www.w3.org/2001/XMLSchema#int>'))

    def test_dt_prefix_inside_value(self):
        self.assertEqual(_XSD_STRING,
                         decide_literal_type('"Helmut Schmidt: a life"^^<http://www.w3.org/2001/XMLSchema#string>'))

    def test_xsd_prefix_inside_value(self):
        self.assertEqual(_XSD_STRING,
                         decide_literal_type('"see xsd:date for details"^^<http://www.w3.org/2001/XMLSchema#string>'))

    def test_geo_prefix_inside_value(self):
        self.assertEqual(_XSD_ANY_URI,
                         decide_literal_type('"geo:50.85,4.35"^^<http://www.w3.org/2001/XMLSchema#anyURI>'))

    def test_custom_datatype_with_escaped_quotes_in_value(self):
        self.assertEqual("http://example.org/myType",
                         decide_literal_type('"a \\"b\\""^^<http://example.org/myType>'))


class TestLanguageTag(unittest.TestCase):

    def test_lang_tag(self):
        self.assertEqual(LANG_STRING_TYPE, decide_literal_type('"Sarah"@en'))

    def test_at_inside_plain_value(self):
        self.assertEqual(STRING_TYPE, decide_literal_type('"mail me @ home"'))

    def test_at_inside_typed_value(self):
        self.assertEqual(_XSD_STRING, decide_literal_type('"a@b"^^<http://www.w3.org/2001/XMLSchema#string>'))


class TestEndpointTermRoundTrip(unittest.TestCase):

    def test_typed_literal(self):
        literal = tune_token(build_term({"type": "literal", "value": "30", "datatype": _XSD_INT}))
        self.assertEqual(_XSD_INT, literal.elem_type)
        self.assertEqual("30", str(literal))

    def test_lang_literal(self):
        literal = tune_token(build_term({"type": "literal", "value": "Sarah", "xml:lang": "en"}))
        self.assertEqual(LANG_STRING_TYPE, literal.elem_type)
        self.assertEqual("Sarah", str(literal))

    def test_literal_with_quotes(self):
        literal = tune_token(build_term({"type": "literal", "value": 'say "hi"'}))
        self.assertEqual(STRING_TYPE, literal.elem_type)
        self.assertEqual('say "hi"', str(literal))

    def test_literal_with_escaped_characters(self):
        literal = tune_token(build_term({"type": "literal", "value": _MULTILINE_VALUE}))
        self.assertEqual(STRING_TYPE, literal.elem_type)
        self.assertEqual(_MULTILINE_VALUE, str(literal))


class TestRdflibSgraphRoundTrip(unittest.TestCase):

    def setUp(self):
        self.triples = [(_SARAH, _AGE, '"30"^^<http://www.w3.org/2001/XMLSchema#int>'),
                        (_SARAH, _NAME, '"Sarah"@en'),
                        (_SARAH, _NAME, '"Sarah"@fr'),
                        (_SARAH, _BIO, build_literal_token(_MULTILINE_VALUE)),
                        (_SARAH, _KNOWS, _FRIEND),
                        (_SARAH, _KNOWS, "_:b0")]
        self.sgraph = RdflibSgraph(rdflib_graph=Graph())
        for a_triple in self.triples:
            self.sgraph.add_triple(a_triple)

    def test_triples_read_back_unchanged(self):
        self.assertEqual(sorted(self.triples),
                         sorted(self.sgraph.yield_p_o_triples_of_an_s("http://example.org/sarah")))

    def test_types_of_read_back_objects(self):
        objects = {o: tune_token(o) for _, _, o in self.sgraph.yield_p_o_triples_of_an_s("http://example.org/sarah")}
        self.assertEqual(_XSD_INT, objects['"30"^^<http://www.w3.org/2001/XMLSchema#int>'].elem_type)
        self.assertEqual(LANG_STRING_TYPE, objects['"Sarah"@en'].elem_type)
        self.assertEqual(LANG_STRING_TYPE, objects['"Sarah"@fr'].elem_type)
        self.assertEqual("http://example.org/jim", objects[_FRIEND].iri)
        self.assertIsInstance(objects["_:b0"], BNode)

    def test_escaped_characters_read_back(self):
        objects = {o: tune_token(o) for _, _, o in self.sgraph.yield_p_o_triples_of_an_s("http://example.org/sarah")}
        literal = objects[build_literal_token(_MULTILINE_VALUE)]
        self.assertEqual(STRING_TYPE, literal.elem_type)
        self.assertEqual(_MULTILINE_VALUE, str(literal))
