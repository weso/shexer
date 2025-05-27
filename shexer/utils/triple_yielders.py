from shexer.model.IRI import IRI
from shexer.model.property import Property
from shexer.model.Literal import Literal
from shexer.model.bnode import BNode
from shexer.utils.uri import remove_corners
from shexer.utils.literal import parse_literal, parse_unquoted_literal, FLOAT_TYPE, INTEGER_TYPE


def check_if_property_belongs_to_namespace_list(str_prop, namespaces):
    """
    It return True if the property balongs to some namespace directly, i.e.,
    without adding any hierarchical element before reaching the name of the property itself.
    Example:
    Property http:example.org/prop, namespace http:example.org/ ---> True
    Property http:example.org/properties/prop, namespace http:example.org/ ---> False
    :param str_prop:
    :param namespaces:
    :return:
    """
    for a_namespace in namespaces:
        if str_prop.startswith(a_namespace):
            if "/" not in str_prop[len(a_namespace):] and "#" not in str_prop[len(a_namespace):]:
                return True
    return False


def tune_subj(a_token, raise_error_if_no_corners=True):
    if a_token.startswith("<"):
        return IRI(remove_corners(a_uri=a_token,
                                  raise_error_if_no_corners=raise_error_if_no_corners))
    elif a_token.startswith("_:"):
        return BNode(identifier=a_token)
    elif a_token.strip() == "[]":
        return BNode(identifier=a_token)

    else:  # ???
        raise ValueError("Unrecognized token in subject position: " + a_token)


def tune_token(a_token, allow_untyped_numbers=False, raise_error_if_no_corners=True, base_namespace=None):
    if a_token.startswith("<"):
        return IRI(remove_corners(a_uri=a_token,
                                  raise_error_if_no_corners=raise_error_if_no_corners))
    elif a_token.startswith('"'):
        content, elem_type = parse_literal(an_elem=a_token,
                                           base_namespace=base_namespace)
        return Literal(content=content,
                       elem_type=elem_type)
    elif a_token.startswith("_:"):
        return BNode(identifier=a_token)
    elif a_token.strip() == "[]":
        return BNode(identifier=a_token)
    if allow_untyped_numbers:
        try:
            candidate_float = float(a_token)
            if _is_integer(candidate_float):
                return Literal(content=a_token.strip(),
                               elem_type=INTEGER_TYPE)
            return Literal(content=a_token.strip(),
                           elem_type=FLOAT_TYPE)
        except:
            pass

    content, elem_type = parse_unquoted_literal(a_token)
    return Literal(content=content,
                   elem_type=elem_type)


def _is_integer(float_number):
    if float_number % 1.0 == 0:
        return True
    return False


def tune_prop(a_token, raise_error_if_no_corners=True):
    return Property(remove_corners(a_uri=a_token,
                                   raise_error_if_no_corners=raise_error_if_no_corners))
