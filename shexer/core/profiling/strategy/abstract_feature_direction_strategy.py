from shexer.utils.shapes import build_shapes_name_for_class_uri
from shexer.core.profiling.consts import POS_CLASSES, _S, _P, _O, POS_FEATURES_DIRECT, _ONE_TO_MANY
from shexer.model.IRI import IRI_ELEM_TYPE, IRI
from shexer.model.bnode import BNode, BNODE_ELEM_TYPE
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME

class AbstractFeatureDirectionStrategy(object):

    def __init__(self, class_profiler):
        self._class_profiler = class_profiler
        self._i_dict = self._class_profiler._instances_dict
        self._c_shapes_dict = self._class_profiler._classes_shape_dict
        self._c_counts = self._class_profiler._class_counts
        self._shape_names_dict = self._class_profiler._shape_names_dict
        self._original_raw_target_classes = self._class_profiler._original_raw_target_classes
        self._detect_minimal_iri = self._class_profiler._detect_minimal_iri
        self._examples_mode = self._class_profiler._examples_mode
        self._namespaces_dict = self._class_profiler._namespaces_dict
        if self._detect_minimal_iri or self._examples_mode is not None:
            self._shape_feature_examples = self._class_profiler._shape_feature_examples

    def adapt_instances_dict(self):
        raise NotImplementedError()

    def is_a_relevant_triple(self, a_triple):
        raise NotImplementedError()

    def annotate_triple_features(self, a_triple):
        raise NotImplementedError()

    def annotate_instance_features(self, an_instance):
        raise NotImplementedError()

    def init_original_targets(self):
        raise NotImplementedError()

    def init_annotated_targets(self):
        raise NotImplementedError()

    def has_shape_annotated_features(self, shape_label):
        raise NotImplementedError()
    #
    # def look_for_example_features(self, instance_id, shape_id):
    #     raise NotImplementedError()

    def _init_annotated_direct_features(self):
        for an_instance, class_list in self._i_dict.items():
            for a_class in class_list:
                if a_class not in self._c_shapes_dict:
                    self._c_shapes_dict[a_class] = {}
                    self._c_counts[a_class] = 0
                self._c_counts[a_class] += 1
                if a_class not in self._shape_names_dict:
                    self._shape_names_dict[a_class] = \
                        build_shapes_name_for_class_uri(class_uri=a_class,
                                                        shapes_namespace=self._class_profiler._shapes_namespace,
                                                        shape_names_dict=self._shape_names_dict,
                                                        namespace_prefix_dict=self._namespaces_dict)

    def _annotate_direct_instance_features(self, an_instance):
        direct_feautres_3tuple = self._infer_direct_3tuple_features(an_instance)

        for a_class in self._i_dict[an_instance][POS_CLASSES]:
            self._annotate_direct_instance_features_for_class(a_class, direct_feautres_3tuple)

    def _infer_direct_3tuple_features(self, an_instance):
        result = []
        for a_prop in self._i_dict[an_instance][POS_FEATURES_DIRECT]:
            for a_type in self._i_dict[an_instance][POS_FEATURES_DIRECT][a_prop]:
                for a_valid_cardinality in self._infer_valid_cardinalities(a_prop,
                                                                           self._i_dict[an_instance][POS_FEATURES_DIRECT][a_prop][a_type]):
                    result.append( (a_prop, a_type, a_valid_cardinality) )
        return result


    def _infer_valid_cardinalities(self, a_property, a_cardinality):
        """
        Special teratment for self._instantiation_property_str. If that's the property, we are targetting specific URIs
        instead of the type IRI.
        Cardinality will be always "1"
        :param a_property:
        :param a_cardinality:
        :return:
        """
        if a_property == self._class_profiler._instantiation_property_str:
            yield 1
        else:
            yield a_cardinality
            yield _ONE_TO_MANY

    def _annotate_direct_instance_features_for_class(self, a_class, features_3tuple):
        for a_feature_3tuple in features_3tuple:
            self._introduce_needed_elements_in_shape_classes_dict(a_class, a_feature_3tuple)
            # 3tuple: 0->str_prop, 1->str_type, 2->cardinality
            self._c_shapes_dict[a_class][a_feature_3tuple[0]][a_feature_3tuple[1]][a_feature_3tuple[2]] += 1

    def _introduce_needed_elements_in_shape_classes_dict(self, a_class, a_feature_3tuple):
        str_prop = a_feature_3tuple[0]
        str_type = a_feature_3tuple[1]
        cardinality = a_feature_3tuple[2]
        if str_prop not in self._c_shapes_dict[a_class]:
            self._c_shapes_dict[a_class][str_prop] = {}
        if str_type not in self._c_shapes_dict[a_class][str_prop]:
            self._c_shapes_dict[a_class][str_prop][str_type] = {}
        if cardinality not in self._c_shapes_dict[a_class][str_prop][str_type]:
            self._c_shapes_dict[a_class][str_prop][str_type][cardinality] = 0

    def _is_relevant_instance(self, an_instance):
        return (isinstance(an_instance, IRI) or isinstance(an_instance, BNode)) and an_instance.iri in self._i_dict

    def _decide_type_elem(self, original_elem, str_prop):
        """
        Special treatment for self._instantiation_property_str property. We look for ValueSets instead of types when this property appears.

        :param original_elem:
        :param str_prop:
        :return:
        """
        if str_prop != self._class_profiler._instantiation_property_str:
            return original_elem.elem_type
        return original_elem.iri

    def _decide_shapes_elem(self, str_elem):
        if str_elem not in self._i_dict:
            return []
        return [self._get_shape_name_for_a_class(a_class)
                for a_class in self._i_dict[str_elem][POS_CLASSES]]

    def _get_shape_name_for_a_class(self, a_class):
        # self._assign_shape_name_if_needed(a_class)
        if a_class.startswith("<"):
            return self._shape_names_dict[a_class]
        return f"{STARTING_CHAR_FOR_SHAPE_NAME}<{self._shape_names_dict[a_class]}>"

    # def _assign_shape_name_if_needed(self, a_class):
    #     if a_class in self._shape_names_dict:
    #         return
    #     self._shape_names_dict[a_class] = \
    #         build_shapes_name_for_class_uri(class_uri=a_class,
    #                                         shapes_namespace=self._class_profiler._shapes_namespace,
    #                                         shape_names_dict=self._shape_names_dict,
    #                                         namespace_prefix_dict=self._namespaces_dict)

    def _annotate_target_subject(self, a_triple):
        str_subj = a_triple[_S].iri
        str_prop = a_triple[_P].iri
        type_obj = self._decide_type_elem(a_triple[_O], str_prop)

        obj_shapes = [] if type_obj not in [IRI_ELEM_TYPE, BNODE_ELEM_TYPE] else self._decide_shapes_elem(a_triple[_O].iri)

        self._introduce_needed_elements_in_shape_instances_dict_for_subj(str_subj=str_subj,
                                                                         str_prop=str_prop,
                                                                         type_obj=type_obj,
                                                                         obj_shapes=obj_shapes)
        self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop][type_obj] += 1
        for a_shape in obj_shapes:
            self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop][a_shape] += 1


    def _introduce_needed_elements_in_shape_instances_dict_for_subj(self, str_subj, str_prop, type_obj, obj_shapes):
        if str_prop not in self._i_dict[str_subj][POS_FEATURES_DIRECT]:
            self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop] = {}
        if type_obj not in self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop]:
            self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop][type_obj] = 0
        for a_shape in obj_shapes:
            if a_shape not in self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop]:
                self._i_dict[str_subj][POS_FEATURES_DIRECT][str_prop][a_shape] = 0