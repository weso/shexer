from shexer.consts import SHEXC, SHACL_TURTLE
from shexer.io.shex.formater.shex_serializer import ShexSerializer
from shexer.io.shacl.formater.shacl_serializer import ShaclSerializer
from shexer.io.uml.uml_serializer import UMLSerializer
from shexer.io.rdfconfig.formater.rdfconfig_serializer import RdfConfigSerializer
from shexer.consts import RATIO_INSTANCES, UML_PLANT_SERVER


def get_shape_serializer(output_format, shapes_list, instance_tracker, target_file=None, string_return=False, namespaces_dict=None,
                         instantiation_property=None, disable_comments=False, wikidata_annotation=False,
                         instances_report_mode=RATIO_INSTANCES, detect_minimal_iri=False, shape_features_examples=None,
                         examples_mode=None, inverse_paths=False, rdfconfig_directory=None, endpoint_url=None,
                         shape_map_raw=None, shape_map_file=None, verbose=False):
    if rdfconfig_directory is not None:
        return RdfConfigSerializer(target_directory=rdfconfig_directory,
                                   shapes_list=shapes_list,
                                   namespaces_dict=namespaces_dict,
                                   string_return=string_return,
                                   instantiation_property_str=instantiation_property,
                                   shape_example_features=shape_features_examples,
                                   endpoint_url=endpoint_url)
    if output_format == SHEXC:
        return ShexSerializer(target_file=target_file,
                              shapes_list=shapes_list,
                              namespaces_dict=namespaces_dict,
                              string_return=string_return,
                              instantiation_property_str=instantiation_property,
                              disable_comments=disable_comments,
                              wikidata_annotation=wikidata_annotation,
                              instances_report_mode=instances_report_mode,
                              detect_minimal_iri=detect_minimal_iri,
                              shape_example_features=shape_features_examples,
                              examples_mode=examples_mode,
                              inverse_paths=inverse_paths)
    elif output_format == SHACL_TURTLE:
        return ShaclSerializer(target_file=target_file,
                               shapes_list=shapes_list,
                               namespaces_dict=namespaces_dict,
                               string_return=string_return,
                               instantiation_property_str=instantiation_property,
                               wikidata_annotation=wikidata_annotation,
                               shape_example_features=shape_features_examples,
                               detect_minimal_iri=detect_minimal_iri,
                               verbose=verbose,
                               shape_map=None if (shape_map_file is None and shape_map_raw is None)
                                               else instance_tracker.shape_map)
    else:
        raise ValueError("Currently unsupported format in 'output_format': " + output_format)


def get_uml_serializer(shapes_list, image_path, url_server=UML_PLANT_SERVER, namespaces_dict=None, ):
    return UMLSerializer(shapes_list=shapes_list,
                         url_server=url_server,
                         image_path=image_path,
                         namespaces_dict=namespaces_dict)
