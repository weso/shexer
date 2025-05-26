

def _add_prefix(unprefixed_elem, prefix):
    return prefix + ":" + unprefixed_elem


def remove_corners(a_uri, raise_error_if_no_corners=True):
    if a_uri.startswith("<") and a_uri.endswith(">"):
        return a_uri[1:-1]
    if raise_error_if_no_corners:
        raise ValueError("Wrong parameter of function: '" + a_uri + "'")
    else:
        return a_uri


def add_corners(a_uri):
    return "<" + a_uri + ">"

def add_corners_if_needed(a_uri):
    if a_uri.startswith("<"):
        return a_uri
    return add_corners(a_uri)

def longest_common_prefix(uri1, uri2):
    """
    It returns an str containing the longest possible common initial part of uri1 and uri2

    :param uri1:
    :param uri2:

    :return:
    """

    if len(uri1) == 0 or len(uri2) == 0:
        return ""
    shortest = len(uri1) if len(uri1) < len(uri2) else len(uri2)
    for i in range(shortest):
        if uri1[i] != uri2[i]:
            return uri1[:i]
    return uri1[:shortest]

def add_corners_if_it_is_an_uri(a_candidate_uri):
    if a_candidate_uri.startswith("http://") or a_candidate_uri.startswith("https://"):  # TODO, check this!
        return "<" + a_candidate_uri + ">"
    return a_candidate_uri


def is_a_correct_uri(target_uri, prefix_namespace_dict):
    """
    TODO: Here I am assuming that there is no forbiden char ( " < > # % { } | \ ^ ~ [ ] ` )
    :param target_uri:
    :param prefix_namespace_dict:
    :return:
    """
    if target_uri[0] == "<" and target_uri[-1] == ">":
        return True
    for a_prefix in prefix_namespace_dict:
        if target_uri.startswith(a_prefix + ":"):
            return True
        return False

def unprefixize_uri_if_possible(target_uri, prefix_namespaces_dict, include_corners=True):
    for a_prefix in prefix_namespaces_dict:
        if target_uri.startswith(a_prefix+":"):
            result = target_uri.replace(a_prefix+":", prefix_namespaces_dict[a_prefix])
            if include_corners:
                result = add_corners(result)
            return result
    return target_uri

def unprefixize_uri_mandatory(target_uri, prefix_namespaces_dict, include_corners=True):
    for a_prefix in prefix_namespaces_dict:
        if target_uri.startswith(a_prefix+":"):
            result = target_uri.replace(a_prefix+":", prefix_namespaces_dict[a_prefix])
            if include_corners:
                result = add_corners(result)
            return result
    raise ValueError("Unrecognized prefix in the following element" + target_uri)


def prefixize_uri_if_possible(target_uri, namespaces_prefix_dict, corners=True):
    best_match = None
    candidate_uri = remove_corners(target_uri) if corners else target_uri
    for a_namespace in namespaces_prefix_dict:  # Prefixed element (all literals are prefixed elements)
        if candidate_uri.startswith(a_namespace):
            if "/" not in candidate_uri[len(a_namespace):] and \
                "#" not in candidate_uri[len(a_namespace):]:
                best_match = a_namespace
                break
            # if best_match is None or len(best_match) < len(a_namespace):
            #     best_match = a_namespace

    return target_uri if best_match is None else candidate_uri.replace(best_match, namespaces_prefix_dict[best_match] + ":")


def get_prefix_of_namespace_if_it_exists(target_uri, namespaces_prefix_dict, corners=True):
    candidate_uri = remove_corners(target_uri) if corners else target_uri
    for a_namespace in namespaces_prefix_dict:  # Prefixed element (all literals are prefixed elements)
        if candidate_uri.startswith(a_namespace):
            if "/" not in candidate_uri[len(a_namespace):] and \
                    "#" not in candidate_uri[len(a_namespace):]:
                return namespaces_prefix_dict[a_namespace]


