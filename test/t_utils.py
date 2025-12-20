from rdflib import Graph, URIRef, Literal
from rdflib.compare import to_isomorphic, graph_diff
import re
from os.path import isfile, exists as file_exists
from os import remove

_BLANKS = re.compile("[ \t]+")
_LINE_JUMPS = re.compile("\n+")

_PREFIX = "PREFIX"
_BEG_SHAPE = "{"
_END_SHAPE = "}"
_BEG_OR = "("
_END_OR = ")"
_OR = " OR "


def get_namespaces_and_shapes_from_str(str_target, or_shapes=False):
    if or_shapes:
        return get_namespaces_and_shapes_from_str_with_or(str_target)
    namespaces = []
    shapes = {}
    last_line = ""
    current_shape = None

    for a_line in str_target.split("\n"):
        if a_line.startswith(_PREFIX):
            namespaces.append(a_line)
        elif a_line.startswith(_BEG_SHAPE):
            current_shape = last_line
            shapes[last_line] = []
        elif a_line.startswith(_END_SHAPE):
            current_shape = None
        elif current_shape is not None:
            shapes[current_shape].append(
                a_line.replace(";", "").strip())  # Avoid trailing ";", that can be there or not

        last_line = a_line  # Always execute

    return namespaces, shapes


def get_namespaces_and_shapes_from_str_with_or(str_target):
    namespaces = []
    shapes = {}
    last_line = ""
    current_shape = None

    or_mode = False
    current_or = None

    for a_line in str_target.split("\n"):
        a_line = a_line.strip()
        if a_line.startswith(_PREFIX):
            namespaces.append(a_line)
        elif a_line.startswith(_BEG_SHAPE):
            current_shape = last_line
            shapes[last_line] = []
        elif a_line.startswith(_END_SHAPE):
            current_shape = None
        elif a_line.startswith(_BEG_OR):
            or_mode = True
            current_or = ""
        elif or_mode:
            if not a_line.startswith(_END_OR):
                current_or = current_or + a_line
            else:
                or_mode = False
                shapes[current_shape].append(current_or)

        elif current_shape is not None:
            shapes[current_shape].append(
                a_line.replace(";", "").strip())  # Avoid trailing ";", that can be there or not

        last_line = a_line  # Always execute

    return namespaces, shapes


def unordered_lists_match(list1, list2):
    return set(list1) == set(list2)

def no_conflict_in_namespaces(names_list_1, names_list_2):
    prefix_namespace_1 = set_of_prefix_namespaces(names_list_1)
    prefix_namespace_2 = set_of_prefix_namespaces(names_list_2)
    for a_prefix in prefix_namespace_1:
        if a_prefix in prefix_namespace_2:
            if prefix_namespace_1[a_prefix] != prefix_namespace_2[a_prefix]:
                return False
    return True

def set_of_prefix_namespaces(namespaces_list):
    result = {}
    for a_namespace_line in namespaces_list:
        sep_index = a_namespace_line.find(":")
        result[a_namespace_line[:sep_index].strip()] =  a_namespace_line[sep_index+1:].strip()
    return result


def ordered_lists_match(list1, list2):
    return list1 == list2


def unordered_sets_match(sets1, sets2):
    for a_set1 in sets1:
        if a_set1 not in sets2:
            return False
    return True


def ordered_sets_match(sets1, sets2):
    if len(sets1) != len(sets2):
        return False
    for i in range(len(sets1)):
        if sets1[i] != sets2[i]:
            return False
    return True


def simple_and_or_str_constraints(
        str_constraints):  # TODO Fix here. Receive a dict, not a list. check call to this method
    simple_c = []
    or_c = []
    for a_c in str_constraints:
        if _OR in a_c:
            or_c.append(a_c)
        else:
            simple_c.append(a_c)
    return simple_c, or_c


def ordered_or_constraints_match(or_list_1, or_list_2):
    if len(or_list_1) != len(or_list_2):
        return False
    for i in range(len(or_list_1)):
        or_list_1[i] = set(or_list_1[i].split(_OR))
        or_list_2[i] = set(or_list_2[i].split(_OR))
    return ordered_sets_match(or_list_1, or_list_2)


def unordered_or_constraints_match(or_list_1, or_list_2):
    if len(or_list_1) != len(or_list_2):
        return False

    for i in range(len(or_list_1)):
        or_list_1[i] = set(or_list_1[i].split("  "))
        or_list_2[i] = set(or_list_2[i].split("  "))
    return unordered_sets_match(or_list_1, or_list_2)


def or_shapes_comparison(shapes1, shapes2, check_order):
    for a_key_label in shapes1:
        if a_key_label not in shapes2:
            return False
        simple_constraints1, or_constraints1 = simple_and_or_str_constraints(shapes1[a_key_label])
        simple_constraints2, or_constraints2 = simple_and_or_str_constraints(shapes2[a_key_label])
        if not check_order:
            if not unordered_lists_match(simple_constraints1, simple_constraints2):
                return False
            if not unordered_or_constraints_match(or_constraints1, or_constraints2):
                return False
        else:
            if not ordered_lists_match(simple_constraints1, simple_constraints2):
                return False
            if not ordered_or_constraints_match(or_constraints1, or_constraints2):
                return False
    return True


def namespaces_match(names1, names2, strict=True):
    if strict:
        return unordered_lists_match(names1, names2)
    else:
        return no_conflict_in_namespaces(names1, names2)


def unsorted_constraints_comparison(shapes1, shapes2):
    for a_key_label in shapes1:
        if a_key_label not in shapes2:
            return False
        if not unordered_lists_match(shapes1[a_key_label], shapes2[a_key_label]):
            return False
    return True


def sorted_constraints_comparison(shapes1, shapes2):
    for a_key_label in shapes1:
        if a_key_label not in shapes2:
            return False
        if not ordered_lists_match(shapes1[a_key_label], shapes2[a_key_label]):
            return False
    return True


def simple_constraints_comparison(shapes1, shapes2, check_order=False):
    if not check_order:
        return unsorted_constraints_comparison(shapes1, shapes2)
    else:
        return sorted_constraints_comparison(shapes1, shapes2)


def shapes_match(shapes1, shapes2, or_shapes=False, check_order=False):
    if len(shapes1) != len(shapes2):
        return False
    if or_shapes:
        return or_shapes_comparison(shapes1, shapes2, check_order)
    return simple_constraints_comparison(shapes1, shapes2, check_order)


def complex_shape_comparison(str1, str2, or_shapes=False, check_order=False, strict=True):
    namespaces1, shapes1 = get_namespaces_and_shapes_from_str(str1, or_shapes)
    namespaces2, shapes2 = get_namespaces_and_shapes_from_str(str2, or_shapes)

    if not namespaces_match(namespaces1, namespaces2, strict):
        return False
    return shapes_match(shapes1, shapes2, or_shapes, check_order)


def normalize_str(str_target):
    result = str_target.strip()
    result = _BLANKS.sub(result, " ")
    return _LINE_JUMPS.sub(result, "\n")


def tunned_str_comparison(str1, str2, or_shapes=False, check_order=False, strict=True):
    if normalize_str(str1) == normalize_str(str2):
        return True
    else:
        return complex_shape_comparison(str1, str2, or_shapes, check_order, strict)


def file_vs_str_tunned_comparison(file_path, str_target, or_shapes=False, check_order=False, strict=True):
    with open(file_path, "r") as in_stream:
        content = in_stream.read()
    return tunned_str_comparison(content, str_target, or_shapes, check_order, strict)


def file_vs_str_exact_comparison(file_path, target_str):
    with open(file_path, "r") as in_stream:
        return in_stream.read().strip() == target_str.strip()

def file_vs_str_strip_comparison(file_path, target_str):
    with open(file_path, "r") as in_stream:
        content = in_stream.read().strip().split("\n")
        target_strip = target_str.strip().split("\n")
        if len(content) != len(target_strip):
            return False
        for i in range(len(content)):
            if content[i].strip() != target_strip[i].strip():
                return False
    return True



def filter_prefixes_str_shex(target_str):
    result = []
    lines = target_str.split("\n")
    counter = 0
    while len(lines) > counter:
        if not lines[counter].startswith("PREFIX"):
            break
        counter += 1
    return "\n".join(lines[counter:]).strip() if counter > 0 else target_str


def file_vs_str_shex_exact_comparison_excluding_prefixes(file_path, str_target):
    with open(file_path, "r") as in_stream:
        target_file_content = filter_prefixes_str_shex(in_stream.read().strip())
        target_str_content = filter_prefixes_str_shex(str_target.strip())

        return target_file_content == target_str_content


def file_vs_file_tunned_comparison(file_path1, file_path2, or_shapes=False):
    with open(file_path1, "r") as in_stream:
        content1 = in_stream.read()
    with open(file_path2, "r") as in_stream:
        content2 = in_stream.read()
    return tunned_str_comparison(content1, content2, or_shapes)


def number_of_shapes(target_str):
    counter = 0
    for a_line in target_str.split("\n"):
        if a_line.startswith(_BEG_SHAPE):
            counter += 1
    return counter


def shape_contains_constraint(target_str, shape, constraint):
    constraint = constraint.replace(";", "").strip()
    lines = target_str.split("\n")
    seeking_mode = False
    for i in range(len(lines)):
        if seeking_mode:
            if lines[i].replace(";", "").strip() == constraint:
                return True
            if lines[i].startswith(_END_SHAPE):
                return False
        if lines[i].startswith(_BEG_SHAPE) and shape == lines[i - 1].strip():
            seeking_mode = True
    return False


def graph_comparison_rdflib(g1, g2):
    iso1 = to_isomorphic(g1)
    iso2 = to_isomorphic(g2)
    # both, in1, in2 = graph_diff(iso1, iso2)
    # return len(both) == len(g1) and len(in1) == 0 and len(in2) == 0
    return to_isomorphic(g1) == to_isomorphic(g2)


def _tune_elem_for_rdflib_comparison(original_elem):
    if original_elem is None:
        return None
    elif original_elem.startswith("<"):
        return URIRef(original_elem[1:-1])
    else:  # It should be a literal
        return Literal(original_elem)


def rdflib_exist_triple(graph, t_subject, t_predicate, t_object):
    return any(
        [a_triple for a_triple in graph.triples(
            (_tune_elem_for_rdflib_comparison(t_subject),
             _tune_elem_for_rdflib_comparison(t_predicate),
             _tune_elem_for_rdflib_comparison(t_object)
             )
        )]
    )


def rdflib_counts_triples(graph, t_subject, t_predicate, t_object):
    return len(
        [a_triple for a_triple in graph.triples(
            (_tune_elem_for_rdflib_comparison(t_subject),
             _tune_elem_for_rdflib_comparison(t_predicate),
             _tune_elem_for_rdflib_comparison(t_object)
             )
        )]
    )


def graph_comparison_file_vs_str(file_path, str_target, format="turtle"):
    g1 = Graph()
    g1.parse(data=str_target, format=format)

    g2 = Graph()
    g2.parse(source=file_path, format=format)

    return graph_comparison_rdflib(g1, g2)


def text_contains_lines(text, list_lines):
    text = _BLANKS.sub(" ", text)
    for a_line in list_lines:
        a_line = _BLANKS.sub(" ", a_line)
        if a_line not in text:
            return False
        return True


def no_sharp_in_shepe_names(str_shapes):
    _, shapes = get_namespaces_and_shapes_from_str(str_shapes, or_shapes=False)
    for a_key_label in shapes:
        if '#' in a_key_label:
            return False
    return True


def check_file_exist(file_path):
    if not isfile(file_path):
        raise FileExistsError(f"The expected file was not found in disk: {file_path}")


def delete_file(file_path):
    if file_exists(file_path):
        try:
            remove(file_path)
        except:
            pass
