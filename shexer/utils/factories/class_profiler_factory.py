from shexer.utils.factories.triple_yielders_factory import get_triple_yielder
from shexer.core.profiling.class_profiler import ClassProfiler
from shexer.core.profiling.federated_source_class_profiler import FederatedSourceClassProfiler
from shexer.utils.target_elements import tune_target_classes_if_needed
from shexer.utils.dict import reverse_keys_and_values


def get_class_profiler(target_classes_dict, source_file, list_of_source_files, input_format,
                       instantiation_property_str,
                       namespaces_to_ignore=None,
                       infer_numeric_types_for_untyped_literals=False,
                       raw_graph=None,
                       namespaces_dict=None,
                       url_input=None,
                       list_of_url_input=None,
                       rdflib_graph=None,
                       shape_map_file=None,
                       shape_map_raw=None,
                       track_classes_for_entities_at_last_depth_level=True,
                       depth_for_building_subgraph=1,
                       url_endpoint=None,
                       strict_syntax_with_corners=False,
                       target_classes=None,
                       file_target_classes=None,
                       built_remote_graph=None,
                       built_shape_map=None,
                       remove_empty_shapes=True,
                       limit_remote_instances=-1,
                       inverse_paths=False,
                       all_classes_mode=False,
                       compression_mode=None,
                       disable_endpoint_cache=None,
                       detect_minimal_iri=False,
                       examples_mode=None,
                       federated_sources=None):
    yielder = get_triple_yielder(source_file=source_file,
                                 list_of_source_files=list_of_source_files,
                                 input_format=input_format,
                                 namespaces_to_ignore=namespaces_to_ignore,
                                 raw_graph=raw_graph,
                                 allow_untyped_numbers=infer_numeric_types_for_untyped_literals,
                                 namespaces_dict=namespaces_dict,
                                 url_input=url_input,
                                 list_of_url_input=list_of_url_input,
                                 rdflib_graph=rdflib_graph,
                                 shape_map_file=shape_map_file,
                                 shape_map_raw=shape_map_raw,
                                 track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                 depth_for_building_subgraph=depth_for_building_subgraph,
                                 url_endpoint=url_endpoint,
                                 instantiation_property=instantiation_property_str,
                                 strict_syntax_with_corners=strict_syntax_with_corners,
                                 target_classes=target_classes,
                                 file_target_classes=file_target_classes,
                                 built_remote_graph=built_remote_graph,
                                 built_shape_map=built_shape_map,
                                 limit_remote_instances=limit_remote_instances,
                                 inverse_paths=inverse_paths,
                                 all_classes_mode=all_classes_mode,
                                 compression_mode=compression_mode,
                                 disable_endpoint_cache=disable_endpoint_cache)

    if federated_sources is None or len(federated_sources) == 0:
        return ClassProfiler(triples_yielder=yielder,
                             instances_dict=target_classes_dict,
                             instantiation_property_str=instantiation_property_str,
                             original_target_classes=None
                             if target_classes is None
                             else tune_target_classes_if_needed(
                                 list_target_classes=target_classes,
                                 prefix_namespaces_dict=reverse_keys_and_values(namespaces_dict)),
                             original_shape_map=built_shape_map,
                             remove_empty_shapes=remove_empty_shapes,
                             inverse_paths=inverse_paths,
                             detect_minimal_iri=detect_minimal_iri,
                             examples_mode=examples_mode)
    else:
        return FederatedSourceClassProfiler(triples_yielder=yielder,
                                            instances_dict=target_classes_dict,
                                            instantiation_property_str=instantiation_property_str,
                                            original_target_classes=None
                                            if target_classes is None
                                            else tune_target_classes_if_needed(
                                                list_target_classes=target_classes,
                                                prefix_namespaces_dict=reverse_keys_and_values(namespaces_dict)),
                                            original_shape_map=built_shape_map,
                                            remove_empty_shapes=remove_empty_shapes,
                                            inverse_paths=inverse_paths,
                                            detect_minimal_iri=detect_minimal_iri,
                                            examples_mode=examples_mode,
                                            list_of_federated_objects=federated_sources)
