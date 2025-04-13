from shexer.core.shexing.class_shexer import ClassShexer
from shexer.core.shexing.class_shexer_fed_sources import ClassShexerFedSources
from shexer.consts import RDF_TYPE, SHAPES_DEFAULT_NAMESPACE, RATIO_INSTANCES


def get_class_shexer(class_counts,
                     class_profile_dict,
                     remove_empty_shapes=True,
                     original_target_classes=None,
                     original_shape_map=None,
                     discard_useless_constraints_with_positive_closure=True,
                     keep_less_specific=True,
                     all_compliant_mode=True,
                     instantiation_property=RDF_TYPE,
                     disable_or_statements=True,
                     disable_comments=False,
                     namespaces_dict=None,
                     allow_opt_cardinality=True,
                     disable_exact_cardinality=False,
                     shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
                     inverse_paths=False,
                     decimals=-1,
                     instances_report_mode=RATIO_INSTANCES,
                     detect_minimal_iri=False,
                     class_min_iris=None,
                     allow_redundant_or=False,
                     federated_sources=None):

    if federated_sources is None:
        return ClassShexer(
            class_counts_dict=class_counts,
            class_profile_dict=class_profile_dict,
            class_profile_json_file=None,
            remove_empty_shapes=remove_empty_shapes,
            original_target_classes=original_target_classes,
            original_shape_map=original_shape_map,
            discard_useless_constraints_with_positive_closure=discard_useless_constraints_with_positive_closure,
            keep_less_specific=keep_less_specific,
            all_compliant_mode=all_compliant_mode,
            instantiation_property=instantiation_property,
            disable_or_statements=disable_or_statements,
            disable_comments=disable_comments,
            namespaces_dict=namespaces_dict,
            allow_opt_cardinality=allow_opt_cardinality,
            disable_exact_cardinality=disable_exact_cardinality,
            shapes_namespace=shapes_namespace,
            inverse_paths=inverse_paths,
            instances_report_mode=instances_report_mode,
            decimals=decimals,
            detect_minimal_iri=detect_minimal_iri,
            class_min_iris_dict=class_min_iris,
            allow_redundant_or=allow_redundant_or
        )
    else:
        return ClassShexerFedSources(
            class_counts_dict=class_counts,
            class_profile_dict=class_profile_dict,
            class_profile_json_file=None,
            remove_empty_shapes=remove_empty_shapes,
            original_target_classes=original_target_classes,
            original_shape_map=original_shape_map,
            discard_useless_constraints_with_positive_closure=discard_useless_constraints_with_positive_closure,
            keep_less_specific=keep_less_specific,
            all_compliant_mode=all_compliant_mode,
            instantiation_property=instantiation_property,
            disable_or_statements=disable_or_statements,
            disable_comments=disable_comments,
            namespaces_dict=namespaces_dict,
            allow_opt_cardinality=allow_opt_cardinality,
            disable_exact_cardinality=disable_exact_cardinality,
            shapes_namespace=shapes_namespace,
            inverse_paths=inverse_paths,
            instances_report_mode=instances_report_mode,
            decimals=decimals,
            detect_minimal_iri=detect_minimal_iri,
            class_min_iris_dict=class_min_iris,
            allow_redundant_or=allow_redundant_or,
            fed_sources=federated_sources
        )
