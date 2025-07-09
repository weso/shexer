from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.core.profiling.strategy.abstract_feature_direction_strategy import AbstractFeatureDirectionStrategy
from shexer.core.profiling.consts import _S, _P, _O, POS_FEATURES_INVERSE, POS_CLASSES
from shexer.model.IRI import IRI_ELEM_TYPE

_C_MAP_POS_DIRECT = 0
_C_MAP_POS_INVERSE = 1


class IncludeReverseFeaturesStrategy(AbstractFeatureDirectionStrategy):



    def __init__(self, class_profiler):
        super().__init__(class_profiler)
        self._set_annotation_methods()


    def adapt_instances_dict(self):
        for a_subj_key in self._i_dict:
            self._i_dict[a_subj_key] = (self._i_dict[a_subj_key], {}, {})


    def is_a_relevant_triple(self, a_triple):
        target_elems = (a_triple[_S], a_triple[_O])
        for elem in target_elems:
            if self._is_relevant_instance(elem):
                return True
        return False


    def annotate_triple_features(self, a_triple):
        raise NotImplementedError()


    def init_annotated_targets(self):
        for an_instance, class_list in self._i_dict.items():
            for a_class in class_list:
                if a_class not in self._c_shapes_dict:
                    self._c_shapes_dict[a_class] = ({}, {})
                    self._c_counts[a_class] = 0
                self._c_counts[a_class] += 1
                if a_class not in self._shape_names_dict:
                    self._shape_names_dict[a_class] = \
                        build_shapes_name_for_class_uri(class_uri=a_class,
                                                        shapes_namespace=self._class_profiler._shapes_namespace,
                                                        shape_names_dict=self._shape_names_dict,
                                                        namespace_prefix_dict=self._namespaces_dict)

    def init_original_targets(self):
        if self._original_raw_target_classes:
            for a_class in self._original_raw_target_classes:
                self._c_shapes_dict[a_class] = ({}, {})
                self._c_counts[a_class] = 0

    def annotate_instance_features(self, an_instance):
        self._annotate_2d_direct_instance_features(an_instance)
        self._annotate_2d_inverse_instance_features(an_instance)

    def has_shape_annotated_features(self, shape_label):
        if shape_label not in self._c_shapes_dict:
            return False
        return len(self._c_shapes_dict[shape_label][_C_MAP_POS_DIRECT]) > 0 or \
               len(self._c_shapes_dict[shape_label][_C_MAP_POS_INVERSE]) > 0

    def _annotate_2d_direct_instance_features(self, an_instance):
        direct_feautres_3tuple = self._infer_direct_3tuple_features(an_instance)
        for a_class in self._i_dict[an_instance][POS_CLASSES]:
            self._annotate_2d_direct_instance_features_for_class(a_class, direct_feautres_3tuple)

    def _annotate_2d_inverse_instance_features(self, an_instance):
        inverse_feautres_3tuple = self._infer_inverse_3tuple_features(an_instance)
        for a_class in self._i_dict[an_instance][POS_CLASSES]:
            self._annotate_2d_inverse_instance_features_for_class(a_class, inverse_feautres_3tuple)

    def _infer_inverse_3tuple_features(self, an_instance):
        result = []
        for a_prop in self._i_dict[an_instance][POS_FEATURES_INVERSE]:
            for a_type in self._i_dict[an_instance][POS_FEATURES_INVERSE][a_prop]:
                for a_valid_cardinality in self._infer_valid_cardinalities(a_prop,
                                                                           self._i_dict[an_instance][POS_FEATURES_INVERSE][a_prop][a_type]):
                    result.append( (a_prop, a_type, a_valid_cardinality) )
        return result

    def _annotate_2d_direct_instance_features_for_class(self, a_class, features_3tuple):
        for a_feature_3tuple in features_3tuple:
            self._introduce_needed_direct_elements_in_2d_shape_classes_dict(a_class, a_feature_3tuple)
            # 3tuple: 0->str_prop, 1->str_type, 2->cardinality
            self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][a_feature_3tuple[0]][a_feature_3tuple[1]][a_feature_3tuple[2]] += 1

    def _annotate_2d_inverse_instance_features_for_class(self, a_class, features_3tuple):
        for a_feature_3tuple in features_3tuple:
            self._introduce_needed_inverse_elements_in_2d_shape_classes_dict(a_class, a_feature_3tuple)
            # 3tuple: 0->str_prop, 1->str_type, 2->cardinality
            self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][a_feature_3tuple[0]][a_feature_3tuple[1]][a_feature_3tuple[2]] += 1

    def _introduce_needed_direct_elements_in_2d_shape_classes_dict(self, a_class, a_feature_3tuple):
        str_prop = a_feature_3tuple[0]
        str_type = a_feature_3tuple[1]
        cardinality = a_feature_3tuple[2]
        if str_prop not in self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT]:
            self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][str_prop] = {}
        if str_type not in self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][str_prop]:
            self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][str_prop][str_type] = {}
        if cardinality not in self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][str_prop][str_type]:
            self._c_shapes_dict[a_class][_C_MAP_POS_DIRECT][str_prop][str_type][cardinality] = 0

    def _introduce_needed_inverse_elements_in_2d_shape_classes_dict(self, a_class, a_feature_3tuple):
        str_prop = a_feature_3tuple[0]
        str_type = a_feature_3tuple[1]
        cardinality = a_feature_3tuple[2]
        if str_prop not in self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE]:
            self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][str_prop] = {}
        if str_type not in self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][str_prop]:
            self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][str_prop][str_type] = {}
        if cardinality not in self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][str_prop][str_type]:
            self._c_shapes_dict[a_class][_C_MAP_POS_INVERSE][str_prop][str_type][cardinality] = 0


    def _annotate_target_object(self, a_triple):  # TODO: refactor here, place this in superclass and parametrize positions
        str_obj = a_triple[_O].iri
        str_prop = a_triple[_P].iri
        type_subj = self._decide_type_elem(a_triple[_S], str_prop)

        subj_shapes = [] if type_subj != IRI_ELEM_TYPE else self._decide_shapes_elem(a_triple[_S].iri)

        self._introduce_needed_elements_in_shape_instances_dict_for_obj(str_obj=str_obj,
                                                                        str_prop=str_prop,
                                                                        type_subj=type_subj,
                                                                        subj_shapes=subj_shapes)
        self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop][type_subj] += 1
        for a_shape in subj_shapes:
            self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop][a_shape] += 1

    def _introduce_needed_elements_in_shape_instances_dict_for_obj(self, str_obj, str_prop, type_subj, subj_shapes):
        if str_prop not in self._i_dict[str_obj][POS_FEATURES_INVERSE]:
            self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop] = {}
        if type_subj not in self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop]:
            self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop][type_subj] = 0
        for a_shape in subj_shapes:
            if a_shape not in self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop]:
                self._i_dict[str_obj][POS_FEATURES_INVERSE][str_prop][a_shape] = 0

    def _set_annotation_methods(self):
        if not self._examples_mode:
            self.annotate_triple_features = self._annotate_triple_features_no_examples
        else:
            self.annotate_triple_features = self._annotate_triple_features_with_examples

    def _annotate_triple_features_with_examples(self, a_triple):
        if self._is_relevant_instance(a_triple[_S]):
            self._annotate_target_subject(a_triple)
            self._annotate_example_subject_inverse_paths(a_triple)
        if self._is_relevant_instance(a_triple[_O]):
            self._annotate_target_object(a_triple)
            self._annotate_example_object_inverse_paths(a_triple)

    def _annotate_triple_features_no_examples(self, a_triple):
        if self._is_relevant_instance(a_triple[_S]):
            self._annotate_target_subject(a_triple)
        if self._is_relevant_instance(a_triple[_O]):
            self._annotate_target_object(a_triple)

    def _annotate_example_subject_inverse_paths(self, a_triple):
        for a_class_key in self._i_dict[str(a_triple[_S])][POS_CLASSES]:
            if not self._shape_feature_examples.has_constraint_example(shape_id=a_class_key,
                                                                       prop_id=str(a_triple[_P]),
                                                                       inverse=False):
                self._shape_feature_examples.set_constraint_example(shape_id=a_class_key,
                                                                    prop_id=str(a_triple[_P]),
                                                                    example=str(a_triple[_O]),
                                                                    inverse=False)

    def _annotate_example_object_inverse_paths(self, a_triple):
        for a_class_key in self._i_dict[str(a_triple[_O])][POS_CLASSES]:
            if not self._shape_feature_examples.has_constraint_example(shape_id=a_class_key,
                                                                       prop_id=str(a_triple[_P]),
                                                                       inverse=True):
                self._shape_feature_examples.set_constraint_example(shape_id=a_class_key,
                                                                    prop_id=str(a_triple[_P]),
                                                                    example=str(a_triple[_S]),
                                                                    inverse=True)


