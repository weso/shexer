from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker
from shexer.utils.factories.triple_yielders_factory import get_triple_yielder
from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.consts import FIXED_SHAPE_MAP

_FEDERATION_TAG_NAME = "_fed_"

class FederatedSourceInstanceTracker(AbstractInstanceTracker):

    def __init__(self, instance_tracker, federated_source_obj):
        self._instance_tracker = instance_tracker
        self._federated_source_obj = federated_source_obj
        self._instances_dict_federated = {}
        self._instances_dict_in_origin = self._instance_tracker._instances_dict  # YES, let it be

        # self._base_triple_yielder = self._build_base_triple_yielder()


    def track_instances(self, verbose=False):
        self._instances_dict_federated = self._build_fed_instances_dict()
        # TODO continue here Think about what to return, instances should be there already.

    def _build_fed_instances_dict(self):
        for an_instance in self._instances_dict_in_origin:
            for a_synonym in self._find_synonyms(an_instance):
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

    # def _build_base_triple_yielder(self):
    #     if self._federated_source_obj.link_in_federated_source:
    #         return self._triple_yielder_from_remote_source()
    #     else:
    #         return self._triple_yielder_from_origin_source()
    #
    # def _triple_yielder_from_remote_source(self):
    #     return get_triple_yielder(
    #         all_classes_mode=True,
    #         track_classes_for_entities_at_last_depth_level=False,
    #         depth_for_building_subgraph=1,
    #         url_endpoint=None,
    #         built_remote_graph=None,
    #         inverse_paths=False,
    #         compression_mode=None, disable_endpoint_cache=False
    #     )