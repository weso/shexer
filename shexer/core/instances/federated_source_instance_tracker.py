from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker
from shexer.utils.factories.triple_yielders_factory import get_triple_yielder
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.consts import FIXED_SHAPE_MAP
from shexer.core.instances.pconsts import  _S, _P, _O

_FEDERATION_TAG_NAME = "_fed_"

class FederatedSourceInstanceTracker(AbstractInstanceTracker):

    def __init__(self, instance_tracker, federated_source_obj):
        self._instance_tracker = instance_tracker
        self._federated_source_obj = federated_source_obj
        self._instances_dict_federated = {}
        self._instances_dict_in_origin = self._instance_tracker._instances_dict  # YES, let it be
        self._origin_triple_yielder = self._instance_tracker._triple_yielder # YES, let it be

        # self._base_triple_yielder = self._build_base_triple_yielder()


    def track_instances(self, verbose=False):
        self._instances_dict_federated = self._build_fed_instances_dict()
        # TODO continue here Think about what to return, instances should be there already.

    def _build_fed_instances_dict(self):
        for an_instance, a_synonym in self._find_synonyms():
            self._add_sinonym_to_dicts(origin_instance=an_instance,
                                       synonym=a_synonym)

    def _add_sinonym_to_dicts(self, origin_instance, synonym):
        shape_labels = [self._adapted_shape_class(a_class) for a_class in self._instances_dict_in_origin[origin_instance]]
        if synonym not in self._instances_dict_federated:
            self._instances_dict_federated[synonym] = []
            self._instances_dict_federated[synonym].add(shape_labels)
            self._instances_dict_federated[origin_instance].add(shape_labels)

    def _adapted_shape_label(self, original_class):
        return original_class + _FEDERATION_TAG_NAME + self._federated_source_obj.alias


    def _find_synonims(self, an_instance):
        if not self._federated_source_obj._link_in_federated_source:
            for an_instance_synonym_pair in self._find_synonims_in_origin():
                yield an_instance_synonym_pair
        else:
            for an_instance_synonym_pair in self._find_synonyms_in_fed_source():
                yield an_instance_synonym_pair
    def _find_synonims_in_origin(self):
        """
        It yields 2-tuples where where:
        - 0, instance (origin source)
        - 1, synonym (federated source)
        """
        instance_position = self._federated_source_obj._origin_position_in_triple
        synonym_position = _S if self._federated_source_obj._origin_position_in_triple == _O else _O
        for a_triple in self._triple_yielder.yield_triples():
            if a_triple[_P] == self._federated_source_obj.property_link:
                if a_triple[instance_position] in self._instances_dict_in_origin:
                    yield (a_triple[instance_position],a_triple[synonym_position])



   def _find_synonyms_in_fed_source(self):
       pass # TODO continue here. Maybe just for a remote graph, or maybe it is trivial to get
            # TODO an ad-hoc triple yielder for every case, changing the model.