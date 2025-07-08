import json

from shexer.consts import RDF_TYPE, SHAPES_DEFAULT_NAMESPACE
from shexer.core.shexing.strategy.direct_shexing_strategy import DirectShexingStrategy
from shexer.core.shexing.strategy.direct_and_inverse_shexing_strategy import DirectAndInverseShexingStrategy
from shexer.utils.target_elements import determine_original_target_nodes_if_needed
from shexer.utils.log import log_msg
from shexer.consts import RATIO_INSTANCES


class ClassShexer(object):

    def __init__(self, class_counts_dict, class_profile_dict=None, class_profile_json_file=None,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 discard_useless_constraints_with_positive_closure=True, keep_less_specific=True,
                 all_compliant_mode=True, instantiation_property=RDF_TYPE, disable_or_statements=True,
                 disable_comments=False, namespaces_dict=None, tolerance_to_keep_similar_rules=0,
                 allow_opt_cardinality=True, disable_exact_cardinality=False,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE, inverse_paths=False,
                 decimals=-1, instances_report_mode=RATIO_INSTANCES, detect_minimal_iri=False,
                 class_min_iris_dict=None, allow_redundant_or=False, shape_names_dict=None):
        self._class_counts_dict = class_counts_dict
        self._class_profile_dict = class_profile_dict if class_profile_dict is not None else self._load_class_profile_dict_from_file(
            class_profile_json_file)
        self._class_min_iris_dict = class_min_iris_dict

        self._shapes_list = []
        self._remove_empty_shapes = remove_empty_shapes
        self._all_compliant_mode = all_compliant_mode
        self._disable_or_statements = disable_or_statements
        self._instantiation_property_str = str(instantiation_property)
        self._disable_comments = disable_comments
        self._discard_useless_positive_closures = discard_useless_constraints_with_positive_closure
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._keep_less_specific = keep_less_specific
        self._tolerance = tolerance_to_keep_similar_rules
        self._allow_opt_cardinality = allow_opt_cardinality
        self._disable_exact_cardinality = disable_exact_cardinality
        self._shapes_namespace = shapes_namespace
        self._decimals = decimals
        self._instances_report_mode = instances_report_mode
        self._detect_minimal_iri = detect_minimal_iri
        self._allow_redundant_or = allow_redundant_or
        self._shape_names_dict = shape_names_dict if shape_names_dict is not None else {}

        self._original_target_nodes = determine_original_target_nodes_if_needed(remove_empty_shapes=remove_empty_shapes,
                                                                                original_target_classes=original_target_classes,
                                                                                original_shape_map=original_shape_map,
                                                                                shape_names_dict=shape_names_dict)
        self._strategy = DirectShexingStrategy(self) if not inverse_paths \
            else DirectAndInverseShexingStrategy(self)

    def shex_classes(self, acceptance_threshold=0,
                     verbose=False):
        log_msg(verbose=verbose,
                msg="Starting shape extraction...")
        self._build_shapes(acceptance_threshold)
        log_msg(verbose=verbose,
                msg="Shape drafts built. Sorting constraints...")
        self._sort_shapes()
        log_msg(verbose=verbose,
                msg="Constraints sorted. Adjusting cardinalities...")
        self._set_valid_constraints_of_shapes()
        log_msg(verbose=verbose,
                msg="Cardinalities adjusted. Cleaning empty shapes if needed...")
        self._clean_empty_shapes()
        log_msg(verbose=verbose,
                msg="No more shapes to clean. {} definitive shapes".format(len(self._shapes_list)))
        return self._shapes_list

    def _set_valid_constraints_of_shapes(self):
        for a_shape in self._shapes_list:
            self._strategy.set_valid_shape_constraints(a_shape)

    def _build_shapes(self, acceptance_threshold):
        for a_shape in self._strategy.yield_base_shapes(acceptance_threshold=acceptance_threshold):
            self._shapes_list.append(a_shape)

    def _sort_shapes(self):
        for a_shape in self._shapes_list:
            a_shape.sort_statements(reverse=True,
                                    callback=self._value_to_compare_statements)

    def _clean_empty_shapes(self):
        if not self._remove_empty_shapes:
            return
        shapes_to_remove = self._detect_shapes_to_remove()

        while (len(shapes_to_remove) != 0):
            self._iteration_remove_empty_shapes(shapes_to_remove)
            shapes_to_remove = self._detect_shapes_to_remove()

    def _detect_shapes_to_remove(self):
        result = set()
        for a_shape in self._shapes_list:
            if a_shape.n_statements == 0:
                result.add(a_shape.name)
        return result

    def _iteration_remove_empty_shapes(self, shape_names_to_remove):
        self._remove_shapes_without_statements(shape_names_to_remove)
        self._remove_statements_to_gone_shapes(shape_names_to_remove)


    def _remove_statements_to_gone_shapes(self, shape_names_to_remove):
        for a_shape in self._shapes_list:
            self._strategy.remove_statements_to_gone_shapes(a_shape, shape_names_to_remove)

    def _remove_shapes_without_statements(self, shape_names_to_remove):
        new_shape_list = []
        for a_shape in self._shapes_list:
            if not a_shape.name in shape_names_to_remove:
                new_shape_list.append(a_shape)
        self._shapes_list = new_shape_list

    def _value_to_compare_statements(self, a_statement):
        return a_statement.probability

    @staticmethod
    def _load_class_profile_dict_from_file(source_file):
        with open(source_file, "r") as in_stream:
            return json.load(in_stream)


