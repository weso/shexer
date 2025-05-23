from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME
from shexer.utils.uri import prefixize_uri_if_possible
from shexer.io.shex.formater.consts import SHAPE_LINK_CHAR

def build_shapes_name_for_class_uri(class_uri, shapes_namespace):
    if class_uri.startswith(SHAPE_LINK_CHAR): # special shape case
        return class_uri
    if class_uri.startswith("<") and class_uri.endswith(">"):
        return STARTING_CHAR_FOR_SHAPE_NAME + class_uri
    last_piece = class_uri
    if "#" in last_piece and last_piece[-1] != "#":
        last_piece = last_piece[last_piece.rfind("#") + 1:]
    if "/" in last_piece:
        if last_piece[-1] != "/":
            last_piece = last_piece[last_piece.rfind("/") + 1:]
        else:
            last_piece = last_piece[last_piece[:-1].rfind("/") + 1:]
    if last_piece.endswith(">"):
        last_piece = last_piece[:-1]
    if last_piece.startswith("<"):
        last_piece = last_piece[1:]
    return STARTING_CHAR_FOR_SHAPE_NAME + "<" + shapes_namespace + last_piece + ">" if last_piece is not None else class_uri



def build_shape_name_for_qualifier_prop_uri(prop_uri, shapes_namespace):  # TODO REVIEW!
    last_piece = None
    if "#" in prop_uri and prop_uri[-1] != "#":
        last_piece = prop_uri[prop_uri.rfind("#") + 1:]
    if "/" in prop_uri:
        if prop_uri[-1] != "/":
            last_piece = prop_uri[prop_uri.rfind("/") + 1:]
        else:
            last_piece = prop_uri[prop_uri[:-1].rfind("/") + 1:]
    if last_piece is not None:
        return STARTING_CHAR_FOR_SHAPE_NAME + "<" + shapes_namespace + last_piece + ">"
    return STARTING_CHAR_FOR_SHAPE_NAME + prop_uri.upper()


def prefixize_shape_name_if_possible(a_shape_name, namespaces_prefix_dict):
    result = prefixize_uri_if_possible(target_uri=a_shape_name[1:],                  # Avoid the "from shexer.model.shape. STARTING_CHAR_FOR_SHAPE_NAME starting char
                                       namespaces_prefix_dict=namespaces_prefix_dict)
    return result