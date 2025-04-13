from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker
from shexer.core.instances.pconsts import _S, _P, _O, FEDERATION_TAG_MARK
from shexer.io.sparql.query import query_endpoint_single_variable

_VARIABLE_NAME_QUERYING_REMOTE_SYNONYMS = "var"
_QUERY_SYNONYMS_ORIGIN_SUBJECT = "select ?s where {{ <{origin_node}> <{synonym_prop}> ?var .  }}"
_QUERY_SYNONYMS_ORIGIN_OBJECT = "select ?s where {{ ?var  <{synonym_prop}>  <{origin_node}> .  }}"

class FederatedSourceInstanceTracker(AbstractInstanceTracker):

    def __init__(self, instance_tracker, federated_source_objs):
        self._instance_tracker = instance_tracker
        self._federated_source_objs = federated_source_objs
        self._instances_dict_in_origin = None
        self._origin_triple_yielder = None
        self._query_to_find_synonyms = None  # may be changed later


    def track_instances(self, verbose=False):
        # TODO We have to do here a loop, walking through, potentially, several instances of federated sources.
        # Then, integrate all dicts into the origin_dict one.
        self._instances_dict_in_origin = self._instance_tracker.track_instances()
        self._origin_triple_yielder = self._instance_tracker._triples_yielder  # YES, let it be
        fed_dicts = []
        for a_fed_source in self._federated_source_objs:
            instances_dict_federated = self._build_fed_instances_dict(a_fed_source)
            # self._integrate_dicts(instances_dict_federated)
            a_fed_source.set_of_instances = set(instances_dict_federated.keys())
            fed_dicts.append(instances_dict_federated)
        for a_fed_dict in fed_dicts:
            self._integrate_dicts(a_fed_dict)
        return self._instances_dict_in_origin

    def _integrate_dicts(self, fed_source_dict):
        for a_key in fed_source_dict:
            self._instances_dict_in_origin[a_key] = fed_source_dict[a_key]

    def _build_fed_instances_dict(self, a_fed_source):
        fed_source_dict = {}
        for an_instance, a_synonym in self._find_synonyms(a_fed_source=a_fed_source, fed_source_dict=fed_source_dict):
            self._add_synonym_to_dicts(origin_instance=an_instance,
                                       synonym=a_synonym,
                                       fed_source_dict=fed_source_dict,
                                       a_fed_source=a_fed_source)
        return fed_source_dict

    def _add_synonym_to_dicts(self, origin_instance, synonym, fed_source_dict, a_fed_source):
        shape_labels = [self._adapted_shape_label(original_class=a_class,
                                                  fed_source=a_fed_source) for a_class in self._instances_dict_in_origin[origin_instance] if FEDERATION_TAG_MARK not in a_class]
        if synonym not in fed_source_dict:
            fed_source_dict[synonym] = []
        fed_source_dict[synonym].extend(shape_labels)
        self._instances_dict_in_origin[origin_instance].extend(shape_labels)

    def _adapted_shape_label(self, original_class, fed_source):
        return original_class + FEDERATION_TAG_MARK + fed_source.alias


    def _find_synonyms(self, a_fed_source, fed_source_dict):
        if not a_fed_source.link_in_federated_source:
            for an_instance_synonym_pair in self._find_synonyms_in_origin(a_fed_source):
                yield an_instance_synonym_pair
        else:
            for an_instance_synonym_pair in self._find_synonyms_in_fed_source(a_fed_source, fed_source_dict):
                yield an_instance_synonym_pair

    def _find_synonyms_in_fed_source(self, a_fed_source):
        self._query_to_find_synonyms = _QUERY_SYNONYMS_ORIGIN_SUBJECT \
            if a_fed_source.origin_position_in_triple == _S \
            else _QUERY_SYNONYMS_ORIGIN_OBJECT
        keys = self._instances_dict_in_origin.keys()
        for an_instance in keys:
            for a_synonym in self._query_remote_synonyms(target_instance=an_instance,
                                                         fed_source=a_fed_source):
                yield an_instance, a_synonym

    def _query_remote_synonyms(self, target_instance, fed_source):
        return query_endpoint_single_variable(endpoint_url=fed_source.endpoint_url,
                                              str_query=self._query_to_find_synonyms.format(origin_node=target_instance,
                                                                                            synonym_prop=fed_source.property_link),
                                              variable_id=_VARIABLE_NAME_QUERYING_REMOTE_SYNONYMS)

    def _find_synonyms_in_origin(self, a_fed_source):
        """
        It yields 2-tuples where where:
        - 0, instance (origin source)
        - 1, synonym (federated source)
        """
        instance_position = a_fed_source.origin_position_in_triple
        synonym_position = _S if a_fed_source.origin_position_in_triple == _O else _O
        for a_triple in self._origin_triple_yielder.yield_triples():
            if a_triple[_P].iri == a_fed_source.property_link:
                if a_triple[instance_position].iri in self._instances_dict_in_origin:
                    yield a_triple[instance_position].iri, a_triple[synonym_position].iri

