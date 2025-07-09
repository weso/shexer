from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.core.profiling.strategy.abstract_feature_direction_strategy import AbstractFeatureDirectionStrategy
from shexer.core.profiling.consts import _S, _P, _O, POS_CLASSES



class DirectFeaturesStrategy(AbstractFeatureDirectionStrategy):

    def __init__(self, class_profiler):
        super().__init__(class_profiler)
        self._set_annotation_methods()


    def adapt_instances_dict(self):
        for a_subj_key in self._i_dict:
            self._i_dict[a_subj_key] = \
                (self._i_dict[a_subj_key], {})

    def is_a_relevant_triple(self, a_triple):
        return self._is_relevant_instance(a_triple[_S])

    def _annotate_triple_features(self, a_triple):
        raise NotImplementedError()


    def annotate_instance_features(self, an_instance):
        self._annotate_direct_instance_features(an_instance)


    def init_annotated_targets(self):
        self._init_annotated_direct_features()

    def init_original_targets(self):
        if self._original_raw_target_classes:
            for a_class in self._original_raw_target_classes:
                self._c_shapes_dict[a_class] = {}
                self._c_counts[a_class] = 0
                self._shape_names_dict[a_class] = \
                    build_shapes_name_for_class_uri(class_uri=a_class,
                                                    shapes_namespace=self._class_profiler._shapes_namespace,
                                                    shape_names_dict=self._shape_names_dict,
                                                    namespace_prefix_dict=self._namespaces_dict)

    def has_shape_annotated_features(self, shape_label):
        if shape_label not in self._c_shapes_dict:
            return False
        return len(self._c_shapes_dict[shape_label]) > 0

    def _set_annotation_methods(self):
        if self._examples_mode is None:
            self.annotate_triple_features = self._annotate_triple_features_no_examples
        else:
            self.annotate_triple_features = self._annotate_triple_features_with_examples


    def _annotate_triple_features_with_examples(self, a_triple):
        self._annotate_target_subject(a_triple)
        self._annotate_example_no_inverse(a_triple=a_triple)

    def _annotate_triple_features_no_examples(self, a_triple):
        self._annotate_target_subject(a_triple)

    def _annotate_example_no_inverse(self, a_triple):
        for a_class_key in self._i_dict[str(a_triple[_S])][POS_CLASSES]:
            if not self._shape_feature_examples.has_constraint_example(shape_id=a_class_key,
                                                                       prop_id=str(a_triple[_P])):
                self._shape_feature_examples.set_constraint_example(shape_id=a_class_key,
                                                                    prop_id=str(a_triple[_P]),
                                                                    example=str(a_triple[_O]))





