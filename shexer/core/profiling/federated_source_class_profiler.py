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
                 examples_mode=None, list_of_federated_objects=None):
        super().__init__(triples_yielder, instances_dict, instantiation_property_str, remove_empty_shapes,
                         original_target_classes, original_shape_map, shapes_namespace, inverse_paths,
                         detect_minimal_iri, examples_mode)

        self._list_of_federated_objects = list_of_federated_objects


    # TODO CHECK ENTIRE PRIFILING PROCESS. maybe there is only need to redefine the yield_triples as it's already done.
    # def profile_classes(self, verbose):
        # log_msg(verbose=verbose,
        #         msg="Starting class profiler...")
        # self._init_class_counts_and_shape_dict()
        # log_msg(verbose=verbose,
        #         msg="Instance counts completed. Annotating instance features...")
        # self._adapt_instances_dict()
        # self._build_shape_of_instances()
        # log_msg(verbose=verbose,
        #         msg="Instance features annotated. Number of relevant triples computed: {}. "
        #             "Building shape profiles...".format(self._relevant_triples))
        #
        # self._build_class_profile()
        # log_msg(verbose=verbose,
        #         msg="Draft shape profiles built. Cleaning shape profiles...")
        # self._clean_class_profile()
        # log_msg(verbose=verbose,
        #         msg="Shape profiles done. Working with {} shapes.".format(len(self._classes_shape_dict)))
        # if self._detect_minimal_iri or self._examples_mode in [SHAPE_EXAMPLES, ALL_EXAMPLES]:
        #     log_msg(verbose=verbose,
        #             msg="Detecting example features for each shape...")
        #     self._init_anotation_example_method()
        #     self._detect_example_features()
        #     log_msg(verbose=verbose,
        #             msg="Mimimal IRIs detected...")
        # return self._classes_shape_dict, self._class_counts, \
        #     self._shape_feature_examples if (self._detect_minimal_iri or self._examples_mode is not None) else None




    # def _complete_class_counts_with_fed_sources(self):
    #     # There whould not be any new class, shape, as they are all mentioned in the base dict.
    #     # All we have to do here is to add class counts wlaking the fed_instance_dicts
    #     for a_fed_source in self._list_of_federated_objects:
    #         self._complete_class_count_of_fed_source(a_fed_source)
    #
    # def _complete_class_count_of_fed_source(self, federated_source_obj):
    #     for an_instance, class_list in federated_source_obj.instances_dict.items():
    #         for a_class in class_list:
    #             # if a_class not in self._c_shapes_dict:
    #             #     self._c_shapes_dict[a_class] = {}
    #             #     self._c_counts[a_class] = 0
    #             self._c_counts[a_class] += 1
    #
    # def _complete_instance_dict_adaptation(self):
    #     for a_fed_source in self._list_of_federated_objects:
    #         if not self._inverse_paths:
    #             self._adapt_i_dict_direct_of_a_


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
