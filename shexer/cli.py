
import argparse

from shexer.consts import DEFAULT_NAMESPACES, SHACL_TURTLE, NT
from shexer.shaper import Shaper


def define_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_kg_path", required=False, help="Input path to the KG")
    parser.add_argument("-o", "--output_shapes_path", required=False, help="Output path for the generated shapes")
    parser.add_argument("-f", "--format", required=False,
                        help="KG input format. Values: nt/tsv_spo/turtle/turtle_iter/xml/n3/json-ld (NT default")
    return parser


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