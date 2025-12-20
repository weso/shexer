from shexer.io.graph.yielder.multi_nt_triples_yielder import MultiNtTriplesYielder
from shexer.io.graph.yielder.nt_triples_yielder import NtTriplesYielder
from shexer.io.graph.yielder.tsv_nt_triples_yielder import TsvNtTriplesYielder
from shexer.io.graph.yielder.multi_tsv_nt_triples_yielder import MultiTsvNtTriplesYielder
from shexer.io.graph.yielder.rdflib_triple_yielder import RdflibParserTripleYielder, RdflibTripleYielder
from shexer.io.graph.yielder.multi_rdflib_triple_yielder import MultiRdfLibTripleYielder
from shexer.io.graph.yielder.remote.sgraph_from_selectors_triple_yielder import SgraphFromSelectorsTripleYielder
from shexer.io.graph.yielder.filter.filter_namespaces_triple_yielder import FilterNamespacesTriplesYielder
from shexer.io.graph.yielder.big_ttl_triples_yielder import BigTtlTriplesYielder
from shexer.io.graph.yielder.multi_big_ttl_files_triple_yielder import MultiBigTtlTriplesYielder
from shexer.io.graph.yielder.multi_zip_triples_yielder import MultiZipTriplesYielder
from shexer.io.graph.yielder.light_turtle_triples_yielder import LightTurtleTriplesYielder, MultiLightTurtleTriplesYielder
from shexer.utils.factories.shape_map_parser_factory import get_shape_map_parser
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.utils.translators.list_of_classes_to_shape_map import ListOfClassesToShapeMap
from shexer.utils.target_elements import tune_target_classes_if_needed
from shexer.utils.dict import reverse_keys_and_values
from shexer.utils.compression import list_of_zip_internal_files
from zipfile import ZipFile

from shexer.consts import NT, TSV_SPO, N3, TURTLE, RDF_XML, FIXED_SHAPE_MAP, JSON_LD, TURTLE_ITER, ZIP


def produce_shape_map_according_to_input(sm_format, sgraph, namespaces_prefix_dict, target_classes,
                                         file_target_classes, shape_map_file, shape_map_raw,
                                         instantiation_property, shape_map_already_built=None,
                                         limit_remote_instances=-1, all_classes_mode=False):
    if shape_map_already_built is not None:
        return shape_map_already_built
    prefix_namespaces_dict = reverse_keys_and_values(namespaces_prefix_dict)
    if shape_map_raw is not None or shape_map_file is not None:
        shape_map_parser = get_shape_map_parser(format=sm_format,
                                                sgraph=sgraph,
                                                namespaces_prefix_dict=namespaces_prefix_dict)

        return shape_map_parser.parse_shape_map(source_file=shape_map_file,
                                                raw_content=shape_map_raw)
    else:
        translator = ListOfClassesToShapeMap(sgraph=sgraph,
                                             prefix_namespaces_dict=prefix_namespaces_dict)
        if all_classes_mode:
            return translator.str_class_list_to_shape_map_sparql_selectors(str_list=[a_class for
                                                                                     a_class in
                                                                                     sgraph.yield_classes_with_instances()],
                                                                           instantiation_property=instantiation_property,
                                                                           limit_remote_instances=limit_remote_instances)
        else:
            target_classes = tune_target_classes_if_needed(list_target_classes=target_classes,
                                                           prefix_namespaces_dict=prefix_namespaces_dict) \
                if target_classes is not None \
                else read_target_classes_from_file(file_target_classes=file_target_classes,
                                                   prefix_namespaces_dict=prefix_namespaces_dict)

            return translator.str_class_list_to_shape_map_sparql_selectors(str_list=target_classes,
                                                                           instantiation_property=instantiation_property,
                                                                           limit_remote_instances=limit_remote_instances)


def get_triple_yielder(source_file=None, list_of_source_files=None, input_format=NT, namespaces_to_ignore=None,
                       allow_untyped_numbers=False, raw_graph=None, namespaces_dict=None, url_input=None,
                       list_of_url_input=None, rdflib_graph=None, shape_map_file=None, shape_map_raw=None,
                       shape_map_format=FIXED_SHAPE_MAP,
                       track_classes_for_entities_at_last_depth_level=True, depth_for_building_subgraph=1,
                       url_endpoint=None, instantiation_property=None, strict_syntax_with_corners=False,
                       target_classes=None, file_target_classes=None, built_remote_graph=None,
                       built_shape_map=None, limit_remote_instances=-1, inverse_paths=False, all_classes_mode=False,
                       compression_mode=None, disable_endpoint_cache=False):
    zip_base_archives = _get_base_zip_archive_if_needed(source_file, list_of_source_files, compression_mode)
    result = None
    if url_endpoint is not None:
        result = _yielder_for_url_endpoint(built_remote_graph=built_remote_graph,
                                           url_endpoint=url_endpoint,
                                           built_shape_map=built_shape_map,
                                           shape_map_format=shape_map_format,
                                           namespaces_dict=namespaces_dict,
                                           target_classes=target_classes,
                                           file_target_classes=file_target_classes,
                                           shape_map_file=shape_map_file,
                                           shape_map_raw=shape_map_raw,
                                           instantiation_property=instantiation_property,
                                           limit_remote_instances=limit_remote_instances,
                                           all_classes_mode=all_classes_mode,
                                           depth_for_building_subgraph=depth_for_building_subgraph,
                                           track_classes_for_entities_at_last_depth_level=track_classes_for_entities_at_last_depth_level,
                                           strict_syntax_with_corners=strict_syntax_with_corners,
                                           allow_untyped_numbers=allow_untyped_numbers,
                                           inverse_paths=inverse_paths,
                                           disable_endpoint_cache=disable_endpoint_cache)

    elif url_input is not None or list_of_url_input is not None:  # Always use rdflib to parse remote graphs
        result = _yielder_for_url_input(url_input=url_input,
                                        allow_untyped_numbers=allow_untyped_numbers,
                                        raw_graph=raw_graph,
                                        input_format=input_format,
                                        namespaces_dict=namespaces_dict,
                                        list_of_url_input=list_of_url_input)
    elif rdflib_graph is not None:
        result = RdflibTripleYielder(rdflib_graph=rdflib_graph,
                                     namespaces_dict=namespaces_dict)
    elif input_format == NT:
        result = _yielder_for_nt(source_file=source_file,
                                 raw_graph=raw_graph,
                                 allow_untyped_numbers=allow_untyped_numbers,
                                 list_of_source_files=list_of_source_files,
                                 compression_mode=compression_mode,
                                 zip_base_archives=zip_base_archives)
    elif input_format == TSV_SPO:
        result = _yielder_for_tsv_spo(source_file=source_file,
                                      allow_untyped_numbers=allow_untyped_numbers,
                                      raw_graph=raw_graph,
                                      list_of_files=list_of_source_files,
                                      compression_mode=compression_mode,
                                      zip_base_archives=zip_base_archives)

    elif input_format in [TURTLE_ITER, TURTLE] and compression_mode is None:
        result = _yielder_for_turtle_light(source_file=source_file,
                                           list_of_files=list_of_source_files,
                                           namespaces_dict=namespaces_dict,
                                           raw_graph=raw_graph)
    elif input_format == TURTLE_ITER:
        result = _yielder_for_turtle_iter(source_file=source_file,
                                          allow_untyped_numbers=allow_untyped_numbers,
                                          raw_graph=raw_graph,
                                          list_of_files=list_of_source_files,
                                          compression_mode=compression_mode,
                                          zip_base_archives=zip_base_archives)
    elif input_format in [N3, RDF_XML, JSON_LD, TURTLE]:
        result = _yielder_for_rdflib_parser(source_file=source_file,
                                            allow_untyped_numbers=allow_untyped_numbers,
                                            raw_graph=raw_graph,
                                            input_format=input_format,
                                            namespaces_dict=namespaces_dict,
                                            list_of_source_files=list_of_source_files,
                                            compression_mode=compression_mode,
                                            zip_base_archives=zip_base_archives)
    else:
        raise ValueError("Not supported format: " + input_format)

    if namespaces_to_ignore is None:
        return result
    else:
        return FilterNamespacesTriplesYielder(actual_triple_yielder=result,
                                              namespaces_to_ignore=namespaces_to_ignore)


def _yielder_for_compressed_inputs(base_yielders):
    if len(base_yielders) == 1:
        result = base_yielders[0]
        return base_yielders[0]
    return MultiZipTriplesYielder(multiyielders=base_yielders)


def _yielder_for_rdflib_parser(source_file, allow_untyped_numbers, raw_graph,
                               input_format, namespaces_dict, list_of_source_files,
                               compression_mode, zip_base_archives):
    if zip_base_archives is not None:
        return _yielder_for_compressed_inputs(
            base_yielders=[MultiRdfLibTripleYielder(list_of_files=list_of_zip_internal_files(a_zip_file),
                                                    allow_untyped_numbers=allow_untyped_numbers,
                                                    input_format=input_format,
                                                    namespaces_dict=namespaces_dict,
                                                    compression_mode=compression_mode,
                                                    zip_archive_file=a_zip_file) for a_zip_file in
                           zip_base_archives])

    elif source_file is not None or raw_graph is not None:
        return RdflibParserTripleYielder(source=source_file,
                                         allow_untyped_numbers=allow_untyped_numbers,
                                         raw_graph=raw_graph,
                                         input_format=input_format,
                                         namespaces_dict=namespaces_dict,
                                         compression_mode=compression_mode)

    else:
        return MultiRdfLibTripleYielder(list_of_files=list_of_source_files,
                                        allow_untyped_numbers=allow_untyped_numbers,
                                        input_format=input_format,
                                        namespaces_dict=namespaces_dict,
                                        compression_mode=compression_mode)


def _yielder_for_turtle_iter(source_file, raw_graph, allow_untyped_numbers, list_of_files,
                             compression_mode, zip_base_archives):
    if zip_base_archives is not None:
        # return MultiBigTtlTriplesYielder(list_of_files=list_of_zip_internal_files(zip_base_archive),
        #                                  compression_mode=compression_mode,
        #                                  allow_untyped_numbers=allow_untyped_numbers,
        #                                  zip_base_archives=zip_base_archives)
        return _yielder_for_compressed_inputs(
            [MultiBigTtlTriplesYielder(list_of_files=list_of_zip_internal_files(a_zip_file),
                                       compression_mode=compression_mode,
                                       allow_untyped_numbers=allow_untyped_numbers,
                                       zip_base_archive=a_zip_file) for a_zip_file in zip_base_archives])
    elif source_file is not None or raw_graph is not None:
        return BigTtlTriplesYielder(source_file=source_file,
                                    allow_untyped_numbers=allow_untyped_numbers,
                                    raw_graph=raw_graph,
                                    compression_mode=compression_mode)
    else:
        return MultiBigTtlTriplesYielder(list_of_files=list_of_files,
                                         allow_untyped_numbers=allow_untyped_numbers,
                                         compression_mode=compression_mode)

def _yielder_for_turtle_light(source_file, list_of_files, namespaces_dict, raw_graph):
    if list_of_files is None:
        return LightTurtleTriplesYielder(source_file=source_file,
                                         raw_graph=raw_graph,
                                         namespaces_dict=namespaces_dict)
    return MultiLightTurtleTriplesYielder(list_of_files=list_of_files,
                                          namespaces_dict=namespaces_dict)


def _yielder_for_tsv_spo(source_file, raw_graph, allow_untyped_numbers, list_of_files,
                         compression_mode, zip_base_archives):
    if zip_base_archives is not None:
        # return MultiTsvNtTriplesYielder(list_of_files=list_of_zip_internal_files(zip_base_archive),
        #                                 compression_mode=compression_mode,
        #                                 allow_untyped_numbers=allow_untyped_numbers,
        #                                 zip_base_archives=zip_base_archives)
        return _yielder_for_compressed_inputs(
            [MultiTsvNtTriplesYielder(list_of_files=list_of_zip_internal_files(a_zip_file),
                                      compression_mode=compression_mode,
                                      allow_untyped_numbers=allow_untyped_numbers,
                                      zip_base_archive=a_zip_file) for a_zip_file in zip_base_archives])
    elif source_file is not None or raw_graph is not None:
        return TsvNtTriplesYielder(source_file=source_file,
                                   allow_untyped_numbers=allow_untyped_numbers,
                                   raw_graph=raw_graph,
                                   compression_mode=compression_mode)
    else:
        return MultiTsvNtTriplesYielder(list_of_files=list_of_files,
                                        allow_untyped_numbers=allow_untyped_numbers,
                                        compression_mode=compression_mode)


def read_target_classes_from_file(file_target_classes, prefix_namespaces_dict):
    result = []
    with open(file_target_classes, "r") as in_stream:
        for a_line in in_stream:
            candidate = a_line.strip()
            if candidate != "":
                result.append(candidate)
    return tune_target_classes_if_needed(list_target_classes=result,
                                         prefix_namespaces_dict=prefix_namespaces_dict)


def _yielder_for_url_endpoint(built_remote_graph, url_endpoint, built_shape_map, shape_map_format,
                              namespaces_dict, target_classes, file_target_classes, shape_map_file,
                              shape_map_raw, instantiation_property, limit_remote_instances, all_classes_mode,
                              depth_for_building_subgraph, track_classes_for_entities_at_last_depth_level,
                              strict_syntax_with_corners, allow_untyped_numbers, inverse_paths, disable_endpoint_cache):
    sgrpah = built_remote_graph if built_remote_graph is not None else EndpointSGraph(endpoint_url=url_endpoint,
                                                                                      store_locally=not disable_endpoint_cache)

    shape_map = built_shape_map
    if built_shape_map is None:
        shape_map = produce_shape_map_according_to_input(sm_format=shape_map_format,
                                                         sgraph=sgrpah,
                                                         namespaces_prefix_dict=namespaces_dict,
                                                         target_classes=target_classes,
                                                         file_target_classes=file_target_classes,
                                                         shape_map_file=shape_map_file,
                                                         shape_map_raw=shape_map_raw,
                                                         instantiation_property=instantiation_property,
                                                         limit_remote_instances=limit_remote_instances,
                                                         all_classes_mode=all_classes_mode)
    return SgraphFromSelectorsTripleYielder(shape_map=shape_map,
                                            depth=depth_for_building_subgraph,
                                            classes_at_last_level=track_classes_for_entities_at_last_depth_level,
                                            instantiation_property=instantiation_property,
                                            strict_syntax_with_corners=strict_syntax_with_corners,
                                            allow_untyped_numbers=allow_untyped_numbers,
                                            inverse_paths=inverse_paths)


def _yielder_for_url_input(url_input, allow_untyped_numbers, raw_graph,
                           input_format, namespaces_dict, list_of_url_input):
    if url_input:
        return RdflibParserTripleYielder(source=url_input,
                                         allow_untyped_numbers=allow_untyped_numbers,
                                         raw_graph=raw_graph,
                                         input_format=input_format,
                                         namespaces_dict=namespaces_dict)
    else:  # elif list_of_url_input:
        return MultiRdfLibTripleYielder(list_of_files=list_of_url_input,
                                        allow_untyped_numbers=allow_untyped_numbers,
                                        input_format=input_format,
                                        namespaces_dict=namespaces_dict)


def _yielder_for_nt(source_file, raw_graph, allow_untyped_numbers,
                    list_of_source_files, compression_mode,
                    zip_base_archives):
    if (source_file is not None or raw_graph is not None) and zip_base_archives is None:
        return NtTriplesYielder(source_file=source_file,
                                allow_untyped_numbers=allow_untyped_numbers,
                                raw_graph=raw_graph,
                                compression_mode=compression_mode)
    elif zip_base_archives is not None:
        # return MultiNtTriplesYielder(list_of_files=list_of_zip_internal_files(zip_base_archive),
        #                              allow_untyped_numbers=allow_untyped_numbers,
        #                              compression_mode=compression_mode,
        #                              zip_base_archives=zip_base_archives)
        return _yielder_for_compressed_inputs(
            [MultiNtTriplesYielder(list_of_files=list_of_zip_internal_files(a_zip_file),
                                   allow_untyped_numbers=allow_untyped_numbers,
                                   compression_mode=compression_mode,
                                   zip_base_archive=a_zip_file) for a_zip_file in zip_base_archives])

    else:
        return MultiNtTriplesYielder(list_of_files=list_of_source_files,
                                     allow_untyped_numbers=allow_untyped_numbers,
                                     compression_mode=compression_mode)


def _get_base_zip_archive_if_needed(source_file, list_of_source_files, compression_mode):
    if compression_mode != ZIP:
        return None
    if source_file is not None:
        return [ZipFile(source_file, 'r')]
    result = []
    for a_source_file in list_of_source_files:
        result.append(ZipFile(a_source_file, 'r'))
    return result
