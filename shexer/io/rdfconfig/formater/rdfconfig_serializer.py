from shexer.core.profiling.class_profiler import RDF_TYPE_STR
import os.path as pth
from shexer.utils.file import load_whole_file_content
_MODEL_FILE_NAME = "model.yaml"
_PREFIX_FILE_NAME = "prefix.yaml"

class RdfConfigSerializer(object):

    def __init__(self, target_directory, shapes_list, namespaces_dict=None, string_return=False,
                 instantiation_property_str=RDF_TYPE_STR, wikidata_annotation=False,
                 detect_minimal_iri=False, shape_example_features=None):
        self._target_directory = target_directory
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._shapes_list = shapes_list
        self._string_return = string_return
        self._instantiation_property_str = instantiation_property_str
        self._wikidata_annotation = wikidata_annotation
        self._detect_minimal_iri = detect_minimal_iri
        self._shape_example_features = shape_example_features

        self._prefixes_file = self._generate_proper_path(_PREFIX_FILE_NAME)
        self._model_file = self._generate_proper_path(_MODEL_FILE_NAME)


    def serialize_shapes(self):
        self._serialize_prefixes()
        self._serialize_shapes()
        return self._compose_output_files_in_str()


    def _serialize_shapes(self):
        pass  # TODO continue here

    def _serialize_prefixes(self):
        with open(self._prefixes_file, "w") as out_stream:
            for a_namespace, a_prefix in self._namespaces_dict.items():
                out_stream.write(f"{a_prefix}: <{a_namespace}>\n")


    def _generate_proper_path(self, file_name):
        return self._target_directory + "" if self._target_directory.enswith(pth.sep) else pth.sep + file_name

    def _compose_output_files_in_str(self):
        return f"{self._header(_PREFIX_FILE_NAME)}\n" \
               f"{load_whole_file_content(self._prefixes_file)}\n" \
               f"{self._header(_PREFIX_FILE_NAME)}\n" \
               f"{load_whole_file_content(self._model_file)}"



