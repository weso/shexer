import unittest
from shexer.shaper import Shaper
from shexer.consts import TURTLE

_PREFIXES = "@prefix ex: <http://example.org/> .\n"

_VARYING_COUNTS = _PREFIXES + """
ex:sarah a ex:Person ; ex:nick "a" , "b" ; ex:owns ex:rex , ex:fido .
ex:jim a ex:Person ; ex:nick "c" ; ex:owns ex:max .
ex:ann a ex:Person ; ex:nick "d" ; ex:owns ex:bo .
ex:rex a ex:Dog .
ex:fido a ex:Dog .
ex:max a ex:Dog .
ex:bo a ex:Dog .
"""

_VARYING_COUNTS_AND_MISSING = _VARYING_COUNTS + """
ex:bob a ex:Person .
"""

_SINGLE_COUNT_AND_MISSING = _PREFIXES + """
ex:sarah a ex:Person ; ex:nick "a" ; ex:owns ex:rex .
ex:jim a ex:Person ; ex:nick "c" ; ex:owns ex:max .
ex:bob a ex:Person .
ex:rex a ex:Dog .
ex:max a ex:Dog .
"""

_PERSON_TYPE = "rdf:type [ex:Person]"


def _person_constraints(raw_graph, **params):
    shaper = Shaper(raw_graph=raw_graph,
                    input_format=TURTLE,
                    namespaces_dict={"http://example.org/": "ex",
                                     "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
                                     "http://www.w3.org/2001/XMLSchema#": "xsd"},
                    all_classes_mode=True,
                    instances_cap=-1,
                    all_instances_are_compliant_mode=True,
                    disable_comments=True,
                    **params)
    lines = shaper.shex_graph(string_output=True, acceptance_threshold=0).splitlines()
    start = next(i for i, a_line in enumerate(lines) if a_line.strip().endswith(":Person")) + 2
    end = next(i for i in range(start, len(lines)) if lines[i].strip().startswith("}"))
    return sorted(" ".join(a_line.replace(";", " ").split()) for a_line in lines[start:end])


class TestAllCompliantCardinality(unittest.TestCase):

    def test_varying_counts_keep_less_specific(self):
        self.assertEqual(["ex:nick xsd:string +", "ex:owns @:Dog +", _PERSON_TYPE],
                         _person_constraints(_VARYING_COUNTS, keep_less_specific=True))

    def test_varying_counts_keep_most_specific(self):
        self.assertEqual(["ex:nick xsd:string +", "ex:owns @:Dog +", _PERSON_TYPE],
                         _person_constraints(_VARYING_COUNTS, keep_less_specific=False))

    def test_varying_counts_keep_most_specific_without_opt_cardinality(self):
        self.assertEqual(["ex:nick xsd:string +", "ex:owns @:Dog +", _PERSON_TYPE],
                         _person_constraints(_VARYING_COUNTS, keep_less_specific=False,
                                             allow_opt_cardinality=False))

    def test_varying_counts_and_missing_keep_less_specific(self):
        self.assertEqual(["ex:nick xsd:string *", "ex:owns @:Dog *", _PERSON_TYPE],
                         _person_constraints(_VARYING_COUNTS_AND_MISSING, keep_less_specific=True))

    def test_varying_counts_and_missing_keep_most_specific(self):
        self.assertEqual(["ex:nick xsd:string *", "ex:owns @:Dog *", _PERSON_TYPE],
                         _person_constraints(_VARYING_COUNTS_AND_MISSING, keep_less_specific=False))

    def test_single_count_and_missing_keep_less_specific(self):
        self.assertEqual(["ex:nick xsd:string ?", "ex:owns @:Dog ?", _PERSON_TYPE],
                         _person_constraints(_SINGLE_COUNT_AND_MISSING, keep_less_specific=True))

    def test_single_count_and_missing_keep_most_specific(self):
        self.assertEqual(["ex:nick xsd:string ?", "ex:owns @:Dog ?", _PERSON_TYPE],
                         _person_constraints(_SINGLE_COUNT_AND_MISSING, keep_less_specific=False))
