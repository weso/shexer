
XSD_NAMESPACE = "http://www.w3.org/2001/XMLSchema#"
XSD_PREFIX = "xsd"

RDF_SYNTAX_NAMESPACE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
RDF_PREFIX = "rdf"
RDF_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#type"

DT_NAMESPACE = "http://dbpedia.org/datatype/"
DT_PREFIX = "dt"

OPENGIS_NAMESPACE = "http://www.opengis.net/ont/geosparql#"
OPENGIS_PREFIX = "geo"

LANG_STRING_TYPE = "http://www.w3.org/1999/02/22-rdf-syntax-ns#langString"
STRING_TYPE = "http://www.w3.org/2001/XMLSchema#string"
FLOAT_TYPE = "http://www.w3.org/2001/XMLSchema#float"
INTEGER_TYPE = "http://www.w3.org/2001/XMLSchema#integer"

from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME

def _count_prior_backslashes(an_str, quote_pos):
    """
    We assume that there is at least a backslash at an_str[pos-1], so pos-1 is a non-negative index of an_str
    """
    counter = 1
    quote_pos -= 2
    while quote_pos >= 0:
        if an_str[quote_pos] == "\\":
            counter += 1
        else:
            return counter
        quote_pos -= 1
    return counter

def find_next_unescaped_quotes(target_str, start_index):
    pos = target_str.find('"', start_index)
    while pos != -1:
        if target_str[pos - 1] != "\\":
            return pos  # not escaped
        # if pos >= 2 and target_str[pos-2] == '\\':
        #     return pos  # the scape is scaped, so not escaped
        if _count_prior_backslashes(an_str=target_str,
                                    quote_pos=pos) % 2 == 0:
            return pos  # the scape is scaped, so not escaped
        pos = target_str.find('"', pos + 1)
    if pos == -1:
        raise ValueError("Is this line malformed? Can`t find quotes matching: " + target_str)

def there_is_arroba_after_last_quotes(target_str):
    if target_str.rfind(STARTING_CHAR_FOR_SHAPE_NAME) > target_str.rfind('"'):
        return True
    return False

def decide_literal_type(a_literal, base_namespace=None):
    if there_is_arroba_after_last_quotes(a_literal):
        return LANG_STRING_TYPE
    elif "\"^^" not in a_literal:
        return STRING_TYPE
    elif "xsd:" in a_literal:
        return XSD_NAMESPACE + a_literal[a_literal.find("xsd:") + 4:]
    elif "rdf:" in a_literal:
        return RDF_SYNTAX_NAMESPACE + a_literal[a_literal.find("rdf:")+ 4:]
    elif "dt:" in a_literal:
        return DT_NAMESPACE + a_literal[a_literal.find("dt:")+ 3:]
    elif "geo:" in a_literal:
        return OPENGIS_NAMESPACE + a_literal[a_literal.find("geo:") + 4:]
    elif XSD_NAMESPACE in a_literal or RDF_SYNTAX_NAMESPACE in a_literal \
            or DT_NAMESPACE in a_literal or OPENGIS_NAMESPACE in a_literal:
        return a_literal[a_literal.find("\"^^")+4:-1]
    elif a_literal.strip().endswith(">"):
        candidate_type = a_literal[a_literal.find("\"^^") + 4:-1]  # plain uri, no corners
        if base_namespace is not None and not candidate_type.startswith("http"):
            return base_namespace + candidate_type
        return candidate_type
    else:
        raise RuntimeError("Unrecognized literal type:" + a_literal)

def parse_literal(an_elem, base_namespace=None):
    closing_quotes = find_next_unescaped_quotes(an_elem, 1)
    content = an_elem[1:closing_quotes].replace("\\\"", "\"")
    elem_type = decide_literal_type(a_literal=an_elem,
                                    base_namespace=base_namespace)
    return content, elem_type

def parse_unquoted_literal(an_elem):
    elem_type = decide_literal_type(an_elem)
    return an_elem, elem_type

