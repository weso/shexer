import string
import random

_PRIORITY_PREFIXES_FOR_SHAPES = ["", "weso-s", "shapes", "w-shapes"]
_RAND_PREFIX_LENGHT = 3

def find_adequate_prefix_for_shapes_namespaces(current_namespace_prefix_dict, avoid_empty=False):
    curr_prefixes = current_namespace_prefix_dict.values()
    for a_prefix in _PRIORITY_PREFIXES_FOR_SHAPES[1 if avoid_empty else 0:]:
        if a_prefix not in curr_prefixes:
            return a_prefix
    # At this point, all the deff prefixes are used. So we generate a random one
    candidate = get_random_string(3)
    while candidate in curr_prefixes:
        candidate = get_random_string(3)
    return candidate

def get_random_string(length):
    result_str = ''.join(random.choice(string.ascii_lowercase) for i in range(length))
    return result_str
