from shexer.core.profiling.class_profiler import ClassProfiler

from shexer.consts import SHAPES_DEFAULT_NAMESPACE
from shexer.core.profiling.consts import RDF_TYPE_STR
from shexer.utils.log import log_msg
from shexer.model.graph.endpoint_sgraph import EndpointSGraph
from shexer.utils.triple_yielders import tune_token, tune_prop
from shexer.core.instances.pconsts import _S, _P, _O

class FederatedSourceClassProfiler(ClassProfiler):

    def __init__(self, triples_yielder, instances_dict, instantiation_property_str=RDF_TYPE_STR,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE, inverse_paths=False, detect_minimal_iri=False,
                 examples_mode=None, list_of_federated_objects=None, namespaces_dict=None):
        super().__init__(triples_yielder, instances_dict, instantiation_property_str, remove_empty_shapes,
                         original_target_classes, original_shape_map, shapes_namespace, inverse_paths,
                         detect_minimal_iri, examples_mode, namespaces_dict)

        self._list_of_federated_objects = list_of_federated_objects


    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._strategy.is_a_relevant_triple(a_triple):
                yield a_triple

        for a_fed_source in self._list_of_federated_objects:
            for a_triple in self._yield_triples_of_fed_source(a_fed_source):
                yield a_triple

    def _yield_triples_of_fed_source(self, fed_source):
        end_graph = EndpointSGraph(fed_source.endpoint_url, store_locally=False)
        if not self._inverse_paths:
            triples = self._direct_target_triples_of_fed_source(end_graph, fed_source)
        else:
            triples = self._direct_and_inverse_target_triples_of_fed_source(end_graph, fed_source)
        for a_triple in triples:
            yield (
                tune_token(a_triple[_S]),
                tune_prop(a_triple[_P]),
                tune_token(a_triple[_O])
            )

    def _direct_target_triples_of_fed_source(self, end_graph, fed_source):
        triples = set()
        for a_target_node in fed_source.set_of_instances:
            for a_triple in end_graph.yield_p_o_triples_of_an_s(a_target_node):
                triples.add(a_triple)
        return triples

    def _direct_and_inverse_target_triples_of_fed_source(self, end_graph, fed_source):
        triples = set()
        for a_target_node in fed_source.set_of_instances:
            for a_triple in end_graph.yield_p_o_triples_of_an_s(a_target_node):
                triples.add(a_triple)
            for a_triple in end_graph.yield_s_p_triples_of_an_o(a_target_node):
                triples.add(a_triple)
        return triples
