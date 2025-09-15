
import argparse

from shexer.consts import DEFAULT_NAMESPACES, SHACL_TURTLE, NT
from shexer.shaper import Shaper


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_kg_path", required=False, help="Input path to the KG")
    parser.add_argument("-o", "--output_shapes_path", required=False, help="Output path for the generated shapes in Turtle")
    parser.add_argument("-f", "--format", required=False,
                        help="KG input format. Values: nt/tsv_spo/turtle/turtle_iter/xml/n3/json-ld (NT default)")
    parser.add_argument("-t", "--target_classes_file", required=False, help="Input path to a file containing target_classes to extract a shape from. One class URI per line")
    parser.add_argument("-I", "--input_kg_paths_file", required=False, help="Input path to a file containing paths to local rdf files to be used as input. One path per line")
    parser.add_argument("-u", "--input_kg_remote", required=False, help="Url to a file containing the input graph")
    parser.add_argument("-U", "--input_kg_remote_file", required=False, help="Input path to a file containing URLs to remote rdf files to be used as input. One URL per line")
    parser.add_argument("-n", "--namespaces_file", required=False, help="Path to JSON file containing a dictionary of namespaces-prefix pairs. These namespaces will be used for the outputs")
    parser.add_argument("-p", "--instantiation_property", required=False, help="URI of the property used to express instance-class relation (rdf:type default)")


    return parser

# target_classes=None,
#                  file_target_classes=None,      DONE
#                  input_format=NT,               DONE
#                  instances_file_input=None,     SKIP
#                  graph_file_input=None,         DONE, MERGED WITH NEXT ONE
#                  graph_list_of_files_input=None,   DONE, MERGED WITH PREVIOUS ONE
#                  raw_graph=None,                SKIP
#                  url_graph_input=None,          DONE
#                  rdflib_graph=None,             SKIP
#                  list_of_url_input=None,        DONE
#                  namespaces_dict=None,          DONE
#                  instantiation_property=RDF_TYPE,      DONE
#                  namespaces_to_ignore=None,
#                  infer_numeric_types_for_untyped_literals=True,
#                  discard_useless_constraints_with_positive_closure=True,
#                  all_instances_are_compliant_mode=True,
#                  keep_less_specific=True,
#                  all_classes_mode=False,
#                  shape_map_file=None,
#                  shape_map_raw=None,
#                  depth_for_building_subgraph=1,
#                  track_classes_for_entities_at_last_depth_level=False,
#                  strict_syntax_with_corners=False,
#                  url_endpoint=None,
#                  shape_map_format=FIXED_SHAPE_MAP,
#                  shape_qualifiers_mode=False,
#                  namespaces_for_qualifier_props=None,
#                  remove_empty_shapes=True,
#                  disable_comments=False,
#                  disable_or_statements=True,
#                  allow_opt_cardinality=True,
#                  disable_exact_cardinality=False,
#                  shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
#                  limit_remote_instances=-1,
#                  wikidata_annotation=False,
#                  inverse_paths=False,
#                  compression_mode=None,
#                  decimals=-1,
#                  instances_report_mode=RATIO_INSTANCES,
#                  disable_endpoint_cache=False,
#                  detect_minimal_iri=False,
#                  allow_redundant_or=False,
#                  instances_cap=-1,
#                  examples_mode=None,
#                  federated_sources=None  # could be a list


def main():
    args = define_args().parse_args()
    if args.format:
        kg_format = args.format
    else:
        kg_format = NT

    shaper = Shaper(
        graph_file_input=args.input_kg_path,
        namespaces_dict=DEFAULT_NAMESPACES,
        all_classes_mode=True,
        input_format=kg_format)
    shaper.shex_graph(output_file=args.output_shapes_path, output_format=SHACL_TURTLE)