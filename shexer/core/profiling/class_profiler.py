from shexer.utils.target_elements import determine_original_target_nodes_if_needed
from shexer.model.property import Property
from shexer.utils.uri import remove_corners
from shexer.consts import SHAPES_DEFAULT_NAMESPACE, SHAPE_EXAMPLES, ALL_EXAMPLES
from shexer.core.profiling.consts import POS_CLASSES
from shexer.utils.log import log_msg
from shexer.utils.uri import longest_common_prefix
from shexer.core.profiling.strategy.direct_features_strategy import DirectFeaturesStrategy
from shexer.core.profiling.strategy.include_reverse_features_strategy import IncludeReverseFeaturesStrategy
from shexer.core.profiling.consts import RDF_TYPE_STR
from shexer.utils.structures.dicts import ShapeExampleFeaturesDict
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME

_MINIMAL_IRI_INIT = STARTING_CHAR_FOR_SHAPE_NAME




class ClassProfiler(object):

    def __init__(self, triples_yielder, instances_dict, instantiation_property_str=RDF_TYPE_STR,
                 remove_empty_shapes=True, original_target_classes=None, original_shape_map=None,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE, inverse_paths=False, detect_minimal_iri=False,
                 examples_mode=None):
        self._triples_yielder = triples_yielder
        self._instances_dict = instances_dict  # TODO  refactor: change name once working again
        # self._instances_shape_dict = {}
        self._shapes_namespace = shapes_namespace
        self._shape_names_dict = {}  # Will be filled during execution
        self._relevant_triples = 0
        self._instantiation_property_str = self._decide_instantiation_property(instantiation_property_str)
        self._remove_empty_shapes = remove_empty_shapes
        self._original_raw_target_classes = original_target_classes
        self._classes_shape_dict = {}  # Will be filled later
        self._class_counts = {}  # Will be filled later
        self._detect_minimal_iri = detect_minimal_iri
        self._examples_mode = examples_mode
        self._inverse_paths = inverse_paths

        self._original_target_nodes = determine_original_target_nodes_if_needed(remove_empty_shapes=remove_empty_shapes,
                                                                                original_target_classes=original_target_classes,
                                                                                original_shape_map=original_shape_map,
                                                                                shapes_namespace=shapes_namespace)

        if detect_minimal_iri or examples_mode is not None:
            self._shape_feature_examples = ShapeExampleFeaturesDict(track_inverse_features=inverse_paths)
            # This last one will be filled later if detect_minimal_iri is True
        self._strategy = DirectFeaturesStrategy(class_profiler=self) if not inverse_paths \
            else IncludeReverseFeaturesStrategy(class_profiler=self)



    def profile_classes(self, verbose):
        log_msg(verbose=verbose,
                msg="Starting class profiler...")
        self._init_class_counts_and_shape_dict()
        log_msg(verbose=verbose,
                msg="Instance counts completed. Annotating instance features...")
        self._adapt_instances_dict()
        self._build_shape_of_instances()
        log_msg(verbose=verbose,
                msg="Instance features annotated. Number of relevant triples computed: {}. "
                    "Building shape profiles...".format(self._relevant_triples))

        self._build_class_profile()
        log_msg(verbose=verbose,
                msg="Draft shape profiles built. Cleaning shape profiles...")
        self._clean_class_profile()
        log_msg(verbose=verbose,
                msg="Shape profiles done. Working with {} shapes.".format(len(self._classes_shape_dict)))
        if self._detect_minimal_iri or self._examples_mode in [SHAPE_EXAMPLES, ALL_EXAMPLES]:
            log_msg(verbose=verbose,
                    msg="Detecting example features for each shape...")
            self._init_anotation_example_method()
            self._detect_example_features()
            log_msg(verbose=verbose,
                    msg="Mimimal IRIs detected...")
        return self._classes_shape_dict, self._class_counts, \
            self._shape_feature_examples if (self._detect_minimal_iri or self._examples_mode is not None) else None

    def get_target_classes_dict(self):
        return self._instances_dict

    def _detect_example_features(self):
        self._init_class_features_dict()
        self._annotate_example_features()


    def _init_class_features_dict(self):
        for a_class_key in self._class_counts:
            self._shape_feature_examples.set_shape_min_iri(shape_id=a_class_key,
                                                           min_iri=_MINIMAL_IRI_INIT)

    def _init_anotation_example_method(self):
        if self._detect_minimal_iri and self._examples_mode in [SHAPE_EXAMPLES, ALL_EXAMPLES]:
            self._annotate_example_features = self._annotate_shape_examples_and_min_iris
        elif self._detect_minimal_iri:
            self._annotate_example_features = self._annotate_min_iris
        else:  # not minimal IRIs, but if this was called, at this point, it means that we are looking for shape examples
            self._annotate_example_features = self._annotate_shape_examples
    def _annotate_example_features(self):
        raise NotImplementedError()

    def _annotate_min_iris(self):
        for an_instance_iri in self._instances_dict:
            for a_class_key in self._instances_dict[an_instance_iri][POS_CLASSES]:
                self._update_shape_min_iri(target_shape=a_class_key,
                                           instance_iri=an_instance_iri)
    def _annotate_shape_examples(self):
        for an_instance_iri in self._instances_dict:
            for a_class_key in self._instances_dict[an_instance_iri][POS_CLASSES]:
                if self._shape_feature_examples.shape_example(shape_id=a_class_key) is None:
                    self._shape_feature_examples.set_shape_example(shape_id=a_class_key,
                                                           example_iri=an_instance_iri)

    def _annotate_shape_examples_and_min_iris(self):
        for an_instance_iri in self._instances_dict:
            for a_class_key in self._instances_dict[an_instance_iri][POS_CLASSES]:
                self._update_shape_min_iri(target_shape=a_class_key,
                                           instance_iri=an_instance_iri)
                if self._shape_feature_examples.shape_example(shape_id=a_class_key) is None:
                    self._shape_feature_examples.set_shape_example(shape_id=a_class_key,
                                                           example_iri=an_instance_iri)


    def _update_shape_min_iri(self, target_shape, instance_iri):
        curr_iri = self._shape_feature_examples.shape_min_iri(shape_id=target_shape)
        if curr_iri == _MINIMAL_IRI_INIT:
            self._shape_feature_examples.set_shape_min_iri(shape_id=target_shape,
                                                           min_iri=instance_iri)
            return

        self._shape_feature_examples.set_shape_min_iri(shape_id=target_shape,
                                                       min_iri=longest_common_prefix(uri1=instance_iri,
                                                                                     uri2=curr_iri))

    @staticmethod
    def _decide_instantiation_property(instantiation_property_str):
        if instantiation_property_str == None:
            return RDF_TYPE_STR
        if type(instantiation_property_str) == Property:
            return str(instantiation_property_str)
        if type(instantiation_property_str) == str:
            return remove_corners(a_uri=instantiation_property_str,
                                  raise_error_if_no_corners=False)
        raise ValueError("Unrecognized param type to define instantiation property")


    def _init_class_counts_and_shape_dict(self):
        """
        IMPORTANT: this method should be called before adapting the instances_dict

        :return:
        """
        self._init_original_targets()
        self._init_annotated_targets()


    def _init_annotated_targets(self):
        self._strategy.init_annotated_targets()

    def _init_original_targets(self):
        self._strategy.init_original_targets()

    def _build_class_profile(self):
        for an_instance in self._instances_dict:
            self._strategy.annotate_instance_features(an_instance)

    def _clean_class_profile(self):
        if not self._remove_empty_shapes:
            return
        shapes_to_remove = self._detect_shapes_to_remove()

        while len(shapes_to_remove) != 0:
            self._iteration_remove_empty_shapes(shapes_to_remove)
            shapes_to_remove = self._detect_shapes_to_remove()

    def _detect_shapes_to_remove(self):
        shapes_to_remove = set()
        for a_shape_key in self._classes_shape_dict:
            if not self._is_original_target_shape(a_shape_key):
                if not self._has_it_annotated_features(a_shape_key):
                    shapes_to_remove.add(a_shape_key)
        return shapes_to_remove

    def _is_original_target_shape(self, shape_label):
        return shape_label in self._original_target_nodes

    def _has_it_annotated_features(self, shape_label):
        return self._strategy.has_shape_annotated_features(shape_label)

    def _iteration_remove_empty_shapes(self, target_shapes):
        for a_shape_label_key in self._classes_shape_dict:
            for a_prop_key in self._classes_shape_dict[a_shape_label_key]:
                # print(self._classes_shape_dict[a_shape_label_key][a_prop_key])
                for a_shape_to_remove in target_shapes:
                    if a_shape_to_remove in self._classes_shape_dict[a_shape_label_key][a_prop_key]:
                        del self._classes_shape_dict[a_shape_label_key][a_prop_key][a_shape_to_remove]
        for a_shape_to_remove in target_shapes:
            if a_shape_to_remove in self._classes_shape_dict:
                del self._classes_shape_dict[a_shape_to_remove]

    def _build_shape_of_instances(self):
        for a_triple in self._yield_relevant_triples():
            self._relevant_triples += 1
            self._annotate_feature_of_target_instance(a_triple)

    def _annotate_feature_of_target_instance(self, a_triple):
        self._strategy.annotate_triple_features(a_triple)

    def _adapt_instances_dict(self):
        self._strategy.adapt_instances_dict()

    def _adapt_entry_dict_if_needed(self, str_subj):
        if type(self._instances_dict[str_subj]) == list:
            self._instances_dict[str_subj] = (self._instances_dict[str_subj], {})

    def _yield_relevant_triples(self):
        for a_triple in self._triples_yielder.yield_triples():
            if self._strategy.is_a_relevant_triple(a_triple):
                yield a_triple

    # def _set_anotation_instance_methods(self):
    #     # MIN IRIS
    #     if self._detect_minimal_iri:
    #         self._update_shape_min_iri = self._update_shape_min_iri_active
    #     else:
    #         self._update_shape_min_iri = self._update_shape_min_iri_inactive
    #
    #     # EXAMPLE FEATURES
    #     if self._examples_mode is None:
    #         self._update_shape_examples = self._update_shape_examples_inactive
    #     elif self._examples_mode == SHAPE_EXAMPLES:
    #         self._update_shape_examples = self._update_shape_examples_only_shapes
    #     elif self._examples_mode == CONSTRAINT_EXAMPLES:
    #         self._update_shape_examples = self._update_shape_examples_only_constraints
    #     elif self._examples_mode == ALL_EXAMPLES:
    #         self._update_shape_examples = self._update_shape_examples_shapes_and_constraints
    #     else:
    #         raise ValueError("Unrecognized mode for getting shape examples. Choose one between the values offered in shexer.const, section # EXAMPLES")


    #
    # def _update_shape_examples_only_constraints(self, instance_id, shape_id):
    #     self._strategy.look_for_example_features(instance_id=instance_id,
    #                                              shape_id=shape_id)
    #
    # def _update_shape_examples_shapes_and_constraints(self, instance_id, shape_id):
    #     self._update_shape_examples_only_shapes(instance_id, shape_id)
    #     self._update_shape_examples_only_constraints(instance_id, shape_id)
    #
    # def _update_shape_examples(self, instance_id, shape_id):
    #     raise NotImplementedError()
    #
    # def _update_shape_examples_inactive(self, instance_id, shape_id):
    #     pass  # This is OK, do nothing
    #




