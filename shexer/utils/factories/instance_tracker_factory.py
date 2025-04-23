from shexer.consts import NT, FIXED_SHAPE_MAP, SHAPES_DEFAULT_NAMESPACE
from shexer.utils.factories.triple_yielders_factory import get_triple_yielder, tune_target_classes_if_needed, \
    read_target_classes_from_file
from shexer.core.instances.instance_tracker import InstanceTracker
from shexer.core.instances.mappings.shape_map_instance_tracker import ShapeMapInstanceTracker
from shexer.core.instances.mix.mixed_instance_tracker import MixedInstanceTracker
from shexer.utils.factories.iri_factory import create_IRIs_from_string_list
from shexer.utils.factories.shape_map_parser_factory import get_shape_map_parser
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.model.graph.rdflib_sgraph import RdflibSgraph
from shexer.utils.dict import reverse_keys_and_values
from shexer.core.instances.federated_source_instance_tracker import FederatedSourceInstanceTracker


def get_instance_tracker(instances_file_input=None, graph_file_input=None,
                         graph_list_of_files_input=None, target_classes=None,
                         file_target_classes=None, input_format=NT,
                         instantiation_property=None,
                         infer_numeric_types_for_untyped_literals=None,
                         namespaces_to_ignore=None,
                         raw_graph=None,
                         all_classes_mode=False,
                         namespaces_dict=None,
                         url_input=None,
                         list_of_url_input=None,
                         rdflib_graph=None,
                         shape_map_file=None,
                         shape_map_raw=None,
                         shape_map_format=FIXED_SHAPE_MAP,
                         track_classes_for_entities_at_last_depth_level=True,
                         depth_for_building_subgraph=1,
                         url_endpoint=None,
                         strict_syntax_with_corners=False,
                         namespaces_for_qualifier_props=None,
                         shape_qualifiers_mode=False,
                         built_remote_graph=None,
                         built_shape_map=None,
                         shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
                         limit_remote_instances=-1,
                         inverse_paths=False,
                         compression_mode=None,
                         disable_endpoint_cache=False,
                         instances_cap=-1,
                         federates_sources=None
                         ):
    """

    :param instances_file_input:
    :param graph_file_input:
    :param graph_list_of_files_input:
    :param target_classes:
    :param file_target_classes:
    :param input_format:
    :param instantiation_property:
    :param namespaces_to_ignore:
    :param raw_graph:
    :param all_classes_mode:
    :param namespaces_dict:
    :param url_input:
    :param list_of_url_input:
    :param shape_map_file:
    :param shape_map_raw:
    :param shape_map_format:
    :param track_classes_for_entities_at_last_depth_level:
    :param depth_for_building_subgraph:
    :param url_endpoint:
    :param strict_syntax_with_corners:
    :param namespaces_for_qualifier_props:
    :param shape_qualifiers_mode:
    :param built_remote_graph:
    :param built_shape_map:
    :return:
    """

    prefix_namespaces_dict = reverse_keys_and_values(namespaces_dict)
    instance_yielder = None  # Old-schooler
    if instances_file_input is not None:
        instance_yielder = get_triple_yielder(source_file=instances_file_input,
                                              input_format=input_format,
                                              namespaces_to_ignore=namespaces_to_ignore,
                                              raw_graph=raw_graph,
                                              namespaces_dict=namespaces_dict,
                                              allow_untyped_numbers=infer_numeric_types_for_untyped_literals,
                                              url_input=url_input,
                                              list_of_url_input=list_of_url_input,
                                              rdflib_graph=rdflib_graph,
                                              instantiation_property=instantiation_property,
                                              shape_map_file=shape_map_file,
                                              shape_map_raw=shape_map_raw,
                                              track_classes_for_entities_at_last_depth_level=
                                              track_classes_for_entities_at_last_depth_level,
                                              depth_for_building_subgraph=depth_for_building_subgraph,
                                              url_endpoint=url_endpoint,
                                              strict_syntax_with_corners=strict_syntax_with_corners,
                                              target_classes=target_classes,
                                              file_target_classes=file_target_classes,
                                              built_remote_graph=built_remote_graph,
                                              built_shape_map=built_shape_map,
                                              limit_remote_instances=limit_remote_instances,
                                              inverse_paths=inverse_paths,
                                              all_classes_mode=all_classes_mode,
                                              compression_mode=compression_mode,
                                              disable_endpoint_cache=disable_endpoint_cache
                                              )
    else:
        instance_yielder = get_triple_yielder(source_file=graph_file_input,
                                              list_of_source_files=graph_list_of_files_input,
                                              input_format=input_format,
                                              namespaces_to_ignore=namespaces_to_ignore,
                                              raw_graph=raw_graph,
                                              namespaces_dict=namespaces_dict,
                                              allow_untyped_numbers=infer_numeric_types_for_untyped_literals,
                                              url_input=url_input,
                                              list_of_url_input=list_of_url_input,
                                              rdflib_graph=rdflib_graph,
                                              instantiation_property=instantiation_property,
                                              shape_map_file=shape_map_file,
                                              shape_map_raw=shape_map_raw,
                                              track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                              depth_for_building_subgraph=depth_for_building_subgraph,
                                              url_endpoint=url_endpoint,
                                              strict_syntax_with_corners=strict_syntax_with_corners,
                                              target_classes=target_classes,
                                              file_target_classes=file_target_classes,
                                              built_remote_graph=built_remote_graph,
                                              built_shape_map=built_shape_map,
                                              limit_remote_instances=limit_remote_instances,
                                              inverse_paths=inverse_paths,
                                              all_classes_mode=all_classes_mode,
                                              compression_mode=compression_mode,
                                              disable_endpoint_cache=disable_endpoint_cache
                                              )

    selectors_tracker = None
    pure_instances_tracker = None

    if _are_there_selectors(shape_map_file, shape_map_raw):
        sgraph = _get_adequate_sgraph(endpoint_url=url_endpoint,
                                      raw_graph=raw_graph,
                                      graph_file_input=graph_file_input,
                                      url_input=url_input,
                                      graph_format=input_format,
                                      built_remote_graph=built_remote_graph,
                                      disable_endpoint_cache=disable_endpoint_cache)
        valid_shape_map = built_shape_map
        if built_shape_map is None:
            shape_map_parser = get_shape_map_parser(format=shape_map_format,
                                                    sgraph=sgraph,
                                                    namespaces_prefix_dict=namespaces_dict)
            valid_shape_map = shape_map_parser.parse_shape_map(source_file=shape_map_file,
                                                               raw_content=shape_map_raw)
        selectors_tracker = ShapeMapInstanceTracker(shape_map=valid_shape_map)
    if _are_there_some_target_classes(target_classes, file_target_classes, all_classes_mode, shape_qualifiers_mode):
        model_classes = None
        if file_target_classes or target_classes is not None:
            list_of_str_target_classes = tune_target_classes_if_needed(
                list_target_classes=target_classes,
                prefix_namespaces_dict=prefix_namespaces_dict) if target_classes is not None else read_target_classes_from_file(
                file_target_classes=file_target_classes,
                prefix_namespaces_dict=prefix_namespaces_dict)
            model_classes = get_list_of_model_classes(list_of_str_target_classes)

        pure_instances_tracker = InstanceTracker(target_classes=model_classes,
                                                 triples_yielder=instance_yielder,
                                                 instantiation_property=instantiation_property,
                                                 all_classes_mode=all_classes_mode,
                                                 track_hierarchies=False,
                                                 namespaces_for_qualifier_props=namespaces_for_qualifier_props,
                                                 shape_qualifiers_mode=shape_qualifiers_mode,
                                                 shapes_namespace=shapes_namespace,
                                                 instances_cap=instances_cap)

    candidate_tracker = _decide_tracker_to_return(selectors_tracker, pure_instances_tracker)
    if federates_sources is None or len(federates_sources) == 0:
        return candidate_tracker
    return FederatedSourceInstanceTracker(instance_tracker=candidate_tracker,
                                          federated_source_objs=federates_sources)


def _get_adequate_sgraph(endpoint_url, graph_file_input, url_input, graph_format,
                         raw_graph, built_remote_graph, disable_endpoint_cache):
    if endpoint_url is not None:
        return built_remote_graph if built_remote_graph is not None else EndpointSGraph(endpoint_url=endpoint_url,
                                                                                        store_locally=not disable_endpoint_cache)
    else:
        return RdflibSgraph(source_file=graph_file_input if graph_file_input is not None else url_input,
                            raw_graph=raw_graph,
                            format=graph_format)


def _decide_tracker_to_return(selectors_tracker, pure_instances_tracker):
    if selectors_tracker is not None and pure_instances_tracker is not None:
        return MixedInstanceTracker(list_of_instance_trackers=[selectors_tracker, pure_instances_tracker])
    return selectors_tracker if selectors_tracker is not None else pure_instances_tracker


def _are_there_selectors(shape_map_file, shape_map_raw):
    if shape_map_file is None and shape_map_raw is None:
        return False
    return True


def _are_there_some_target_classes(target_classes, file_target_classes, all_classes_mode, shape_qualifiers_mode):
    if target_classes is None and file_target_classes is None and not all_classes_mode and not shape_qualifiers_mode:
        return False
    return True


def get_list_of_model_classes(list_of_str_target_classes):
    return create_IRIs_from_string_list(list_of_str_target_classes)
