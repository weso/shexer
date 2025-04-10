from shexer.core.profiling.class_profiler import ClassProfiler

from shexer.consts import SHAPES_DEFAULT_NAMESPACE
from shexer.core.profiling.consts import RDF_TYPE_STR

class FederatedSourceClassProfiler(ClassProfiler):

    def __init__(self, triples_yielder, instances_dict, instantiation_property_str=RDF_TYPE_STR,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE, inverse_paths=False, detect_minimal_iri=False,
                 examples_mode=None, list_of_federated_entry_points=None):
        super().__init__(triples_yielder, instances_dict, instantiation_property_str, remove_empty_shapes,
                         original_target_classes, original_shape_map, shapes_namespace, inverse_paths,
                         detect_minimal_iri, examples_mode)

        self._list_of_federated_entrypoints = list_of_federated_entry_points
