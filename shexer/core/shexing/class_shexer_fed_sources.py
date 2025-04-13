from shexer.core.shexing.class_shexer import ClassShexer
from shexer.consts import RDF_TYPE, SHAPES_DEFAULT_NAMESPACE
from shexer.consts import RATIO_INSTANCES
from shexer.core.instances.pconsts import FEDERATION_TAG_MARK

_COMMENT_FED_PROPERTY = "# Constraint only observed in {}"

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
        result = super().shex_classes(acceptance_threshold=acceptance_threshold,
                                      verbose=verbose)
        self._annotate_properties_in_fed_shapes(result)
        return result


    def _annotate_properties_in_fed_shapes(self, list_of_shapes):
        pairs = self._find_pairs_of_origin_and_fed_shape(list_of_shapes)
        for a_origin_fed_pair in pairs:
            self._annotate_fed_properties_of_a_shape(origin_shape=a_origin_fed_pair[0],
                                                     fed_shape=a_origin_fed_pair[1])


    def _annotate_fed_properties_of_a_shape(self, origin_shape, fed_shape):
        fed_name_for_comments = fed_shape.class_uri[
                                fed_shape.class_uri.find(FEDERATION_TAG_MARK)+len(FEDERATION_TAG_MARK):]
        for a_fed_statement in fed_shape.direct_statements:
            only_in_fed = True
            for a_orig_statement in origin_shape.direct_statements:
                if a_fed_statement.st_property == self._instantiation_property_str:
                    if a_fed_statement.st_property == a_orig_statement.st_property and a_fed_statement.st_type == a_orig_statement.st_type:
                        only_in_fed = False
                        break
                else:
                    if a_fed_statement.st_property == a_orig_statement.st_property:
                        only_in_fed = False
                        break
            if only_in_fed:
                a_fed_statement.add_comment(_COMMENT_FED_PROPERTY.format(fed_name_for_comments))
        # TODO: same thing with inverse. Probably refactor
        for a_fed_statement in fed_shape.inverse_statements:
            only_in_fed = False
            for a_orig_statement in origin_shape.inverse_statements:
                if a_fed_statement.st_property == self._instantiation_property:
                    if a_fed_statement.st_property == a_orig_statement.st_property and a_fed_statement.st_type == a_orig_statement.st_type:
                        only_in_fed = True
                        break
                else:
                    if a_fed_statement.st_property == a_orig_statement.st_property:
                        only_in_fed = True
                        break
            if only_in_fed:
                a_fed_statement.add_comment(comment=_COMMENT_FED_PROPERTY.format(fed_name_for_comments),
                                            insert_first=False)

    def _find_pairs_of_origin_and_fed_shape(self, list_of_shapes):
        result = []
        for i in range(len(list_of_shapes)):
            a_shape = list_of_shapes[i]
            for a_potential_fed_shape in list_of_shapes[i+1:]:
                if a_potential_fed_shape.class_uri.startswith(a_shape.class_uri) and \
                        FEDERATION_TAG_MARK in a_potential_fed_shape.class_uri:
                    result.append((a_shape, a_potential_fed_shape))
        return result


