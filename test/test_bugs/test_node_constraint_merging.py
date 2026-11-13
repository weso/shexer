import unittest
from shexer.shaper import Shaper
from shexer.consts import TURTLE

_PREFIXES = "@prefix ex: <http://example.org/> .\n"

_SEVERAL_CLASSES = _PREFIXES + """
ex:sarah a ex:Person ; ex:owns ex:rex , ex:tom .
ex:jim a ex:Person ; ex:owns ex:fido .
ex:ann a ex:Person .
ex:rex a ex:Dog .
ex:fido a ex:Dog .
ex:tom a ex:Cat .
"""

_UNTYPED_OBJECT = _PREFIXES + """
ex:sarah a ex:Person ; ex:owns ex:rex , ex:stone .
ex:jim a ex:Person ; ex:owns ex:fido .
ex:rex a ex:Dog .
ex:fido a ex:Dog .
"""

_SAME_CLASS = _PREFIXES + """
ex:sarah a ex:Person ; ex:owns ex:rex , ex:fido .
ex:jim a ex:Person ; ex:owns ex:max .
ex:rex a ex:Dog .
ex:fido a ex:Dog .
ex:max a ex:Dog .
"""

_IRI_AND_BNODE = _PREFIXES + """
ex:sarah a ex:Person ; ex:owns ex:rex , _:b1 .
ex:jim a ex:Person ; ex:owns ex:fido .
ex:rex a ex:Dog .
ex:fido a ex:Dog .
"""

_UNTYPED_IRI_AND_BNODE = _PREFIXES + """
ex:sarah a ex:Person ; ex:owns ex:stone , _:b1 .
ex:jim a ex:Person ; ex:owns ex:rock .
"""

_IRI_AND_BNODE_SUBJECTS = _PREFIXES + """
ex:rex a ex:Dog .
ex:fido a ex:Dog .
ex:sarah ex:owns ex:rex .
_:b1 ex:owns ex:rex .
ex:jim ex:owns ex:fido .
"""

_PERSON_TYPE = "rdf:type [ex:Person]"


def _shape_constraints(label, raw_graph, **params):
    shaper = Shaper(raw_graph=raw_graph,
                    input_format=TURTLE,
                    namespaces_dict={"http://example.org/": "ex",
                                     "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf"},
                    all_classes_mode=True,
                    instances_cap=-1,
                    all_instances_are_compliant_mode=True,
                    disable_comments=True,
                    **params)
    lines = shaper.shex_graph(string_output=True, acceptance_threshold=0).splitlines()
    start = next(i for i, a_line in enumerate(lines) if a_line.strip().endswith(":" + label)) + 2
    end = next(i for i in range(start, len(lines)) if lines[i].strip().startswith("}"))
    return sorted(" ".join(a_line.replace(";", " ").split()) for a_line in lines[start:end])


class TestNodeConstraintMerging(unittest.TestCase):

    def test_several_classes_or_disabled(self):
        self.assertEqual(["ex:owns IRI *", _PERSON_TYPE],
                         _shape_constraints("Person", _SEVERAL_CLASSES, disable_or_statements=True))

    def test_several_classes_or_enabled(self):
        self.assertEqual(["ex:owns @:Dog OR @:Cat *", _PERSON_TYPE],
                         _shape_constraints("Person", _SEVERAL_CLASSES, disable_or_statements=False))

    def test_several_classes_or_enabled_without_opt_nor_exact_cardinality(self):
        self.assertEqual(["ex:owns @:Dog OR @:Cat *", _PERSON_TYPE],
                         _shape_constraints("Person", _SEVERAL_CLASSES, disable_or_statements=False,
                                            allow_opt_cardinality=False, disable_exact_cardinality=True))

    def test_untyped_object_or_disabled(self):
        self.assertEqual(["ex:owns IRI +", _PERSON_TYPE],
                         _shape_constraints("Person", _UNTYPED_OBJECT, disable_or_statements=True))

    def test_untyped_object_or_enabled(self):
        self.assertEqual(["ex:owns IRI +", _PERSON_TYPE],
                         _shape_constraints("Person", _UNTYPED_OBJECT, disable_or_statements=False))

    def test_same_class_or_disabled(self):
        self.assertEqual(["ex:owns @:Dog +", _PERSON_TYPE],
                         _shape_constraints("Person", _SAME_CLASS, disable_or_statements=True))

    def test_same_class_or_enabled(self):
        self.assertEqual(["ex:owns @:Dog +", _PERSON_TYPE],
                         _shape_constraints("Person", _SAME_CLASS, disable_or_statements=False))

    def test_iri_and_untyped_bnode(self):
        self.assertEqual(["ex:owns NONLITERAL +", _PERSON_TYPE],
                         _shape_constraints("Person", _IRI_AND_BNODE, disable_or_statements=True))

    def test_untyped_iri_and_untyped_bnode(self):
        self.assertEqual(["ex:owns NONLITERAL +", _PERSON_TYPE],
                         _shape_constraints("Person", _UNTYPED_IRI_AND_BNODE, disable_or_statements=True))

    def test_inverse_iri_and_bnode_subjects(self):
        self.assertEqual(["^ ex:owns NONLITERAL +", "rdf:type [ex:Dog]"],
                         _shape_constraints("Dog", _IRI_AND_BNODE_SUBJECTS, inverse_paths=True))
