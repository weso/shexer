import os.path as pth

BASE_FILES = pth.join(pth.dirname(pth.normpath(__file__)), "t_files" + pth.sep)
BASE_FILES_GENERAL = BASE_FILES + "general" + pth.sep

G1 = BASE_FILES + "t_graph_1.ttl"
G1_NT = BASE_FILES + "t_graph_1.nt"
G1_TSVO_SPO = BASE_FILES + "t_graph_1.tsv"
G1_JSON_LD = BASE_FILES + "t_graph_1.json"
G1_XML = BASE_FILES + "t_graph_1.xml"
G1_TTL_WITH_BASE = BASE_FILES + "t_graph_1_base.ttl"
G1_TTL_WITH_ABSOLUTES = BASE_FILES + "t_graph_1_absolutes.ttl"
G1_TTL_WITH_USELESS_BNODE = BASE_FILES + "t_graph_1_bnode.ttl"
G1_TTL_WITH_SCAPED_QUOTES = BASE_FILES + "t_graph_1_scaped_quotes.ttl"
G1_TTL_WITH_SCAPED_QUOTES_AND_MULTILINE = BASE_FILES + "t_graph_1_scaped_quotes_and_multiline.ttl"
G1_TTL_WITH_MULTILINE_STR = BASE_FILES + "t_graph_1_multiline_str.ttl"

G1_N3 = BASE_FILES + "t_graph_1.n3"

G1_ALL_CLASSES_NO_COMMENTS = BASE_FILES_GENERAL + "g1_all_classes_no_comments.shex"


# PREFIX xml: <http://www.w3.org/XML/1998/namespace/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
# PREFIX foaf: <http://xmlns.com/foaf/0.1/>

# NAMESPACES_WITH_FOAF_AND_EX = {"http://example.org/" : "ex",
#                                "http://www.w3.org/XML/1998/namespace/" : "xml",
#                                "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
#                                "http://www.w3.org/2000/01/rdf-schema#" : "rdfs",
#                                "http://www.w3.org/2001/XMLSchema#": "xsd",
#                                "http://xmlns.com/foaf/0.1/": "foaf"
#                                }

def default_namespaces():
    return {"http://example.org/": "ex",
            "http://www.w3.org/XML/1998/namespace/": "xml",
            "http://www.w3.org/1999/02/22-rdf-syntax-ns#": "rdf",
            "http://www.w3.org/2000/01/rdf-schema#": "rdfs",
            "http://www.w3.org/2001/XMLSchema#": "xsd",
            "http://xmlns.com/foaf/0.1/": "foaf"
            }
