from shexer.core.profiling.class_profiler import RDF_TYPE_STR

class RdfConfigSerializer(object):

    def __init__(self, target_directory, shapes_list, namespaces_dict=None, string_return=False,
                 instantiation_property_str=RDF_TYPE_STR, wikidata_annotation=False,
                 detect_minimal_iri=False, shape_example_features=None):
        self._target_file = target_directory
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._shapes_list = shapes_list
        self._string_return = string_return
        self._instantiation_property_str = instantiation_property_str
        self._wikidata_annotation = wikidata_annotation
        self._detect_minimal_iri = detect_minimal_iri
        self._shape_example_features = shape_example_features



    def serialize_shapes(self):
        pass  # TODO


