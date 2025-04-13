from shexer.core.shexing.class_shexer import ClassShexer
from shexer.consts import RDF_TYPE, SHAPES_DEFAULT_NAMESPACE
from shexer.consts import RATIO_INSTANCES

class ClassShexerFedSources(ClassShexer):


    def __init__(self, class_counts_dict, class_profile_dict=None, class_profile_json_file=None,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 discard_useless_constraints_with_positive_closure=True, keep_less_specific=True,
                 all_compliant_mode=True, instantiation_property=RDF_TYPE, disable_or_statements=True,
                 disable_comments=False, namespaces_dict=None, tolerance_to_keep_similar_rules=0,
                 allow_opt_cardinality=True, disable_exact_cardinality=False, shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
                 inverse_paths=False, decimals=-1, instances_report_mode=RATIO_INSTANCES, detect_minimal_iri=False,
                 class_min_iris_dict=None, allow_redundant_or=False, fed_sources=None):
        super().__init__(class_counts_dict, class_profile_dict, class_profile_json_file, remove_empty_shapes,
                         original_target_classes, original_shape_map, discard_useless_constraints_with_positive_closure,
                         keep_less_specific, all_compliant_mode, instantiation_property, disable_or_statements,
                         disable_comments, namespaces_dict, tolerance_to_keep_similar_rules, allow_opt_cardinality,
                         disable_exact_cardinality, shapes_namespace, inverse_paths, decimals, instances_report_mode,
                         detect_minimal_iri, class_min_iris_dict, allow_redundant_or)
        self._fed_sources = fed_sources

    def shex_classes(self, acceptance_threshold=0,
                     verbose=False):
        pass

