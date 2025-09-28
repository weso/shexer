#OUTPUTS
SHEXC = "ShEx"
SHACL_TURTLE = "Shacl"

#INPUT FORMATS
NT = "nt"
TSV_SPO = "tsv_spo"
TURTLE = "turtle"
TURTLE_ITER = "turtle_iter"
RDF_XML = "xml"
N3 = "n3"
JSON_LD = "json-ld"

#SHAPE MAP FORMATS
JSON = "json"
FIXED_SHAPE_MAP = "fsm"

#FREQUENT INSTATIATION PROPERTIES
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"
WIKIDATA_INSTACE_OF = "http://www.wikidata.org/prop/direct/P31"

#NAMESPACES
SHAPES_DEFAULT_NAMESPACE = "http://weso.es/shapes/"

#COMPRESSION FORMATS
ZIP = "zip"
GZ = "gz"
XZ = "xz"

# FREQUENCY MODES

RATIO_INSTANCES = "ratio"
ABSOLUTE_INSTANCES = "abs"
MIXED_INSTANCES = "mixed"


# EXAMPLES
SHAPE_EXAMPLES = "shape"
CONSTRAINT_EXAMPLES = "cons"
ALL_EXAMPLES = "all"

# UML
UML_PLANT_SERVER = "http://www.plantuml.com/plantuml/img/"

DEFAULT_NAMESPACES = {"http://example.org/": "ex",
            "http://www.w3.org/XML/1998/namespace/": "xml",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
            "http://www.w3.org/2001/XMLSchema#": "xsd",
            "http://xmlns.com/foaf/0.1/": "foaf"
            }

# WESO-SHAPES-ONTO  # todo !
FREQ_PROP = "http://weso.es/shexer/ontology/ratio_property_usage"
EXTRA_INFO_PROP = "http://www.w3.org/2000/01/rdf-schema#comment"
EXAMPLE_CONFORMANCE_PROP = "http://weso.es/shexer/ontology/conformant_example"
ABSOLUTE_COUNT_PROP = "http://weso.es/shexer/ontology/total_conforming_instances"