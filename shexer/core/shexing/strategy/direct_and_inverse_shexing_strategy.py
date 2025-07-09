from shexer.core.shexing.strategy.abstract_shexing_strategy import AbstractShexingStrategy
from shexer.model.statement import Statement
from shexer.model.shape import Shape

_POS_FEATURES_DIRECT = 0
_POS_FEATURES_INVERSE = 1


class DirectAndInverseShexingStrategy(AbstractShexingStrategy):

    def __init__(self, class_shexer):
        super().__init__(class_shexer)
        self._class_profile_dict = self._class_shexer._class_profile_dict
        self._shapes_namespace = self._class_shexer._shapes_namespace
        self._class_counts_dict = self._class_shexer._class_counts_dict
        self._namespaces_dict = self._class_shexer._namespaces_dict

    def remove_statements_to_gone_shapes(self, shape, shape_names_to_remove):
        shape.direct_statements = self._statements_without_shapes_to_remove(
            original_statements=shape.direct_statements,
            shape_names_to_remove=shape_names_to_remove)
        shape.inverse_statements = self._statements_without_shapes_to_remove(
            original_statements=shape.inverse_statements,
            shape_names_to_remove=shape_names_to_remove)

    def _yield_base_shapes_direction_aware(self, acceptance_threshold):
        for a_class_key in self._class_profile_dict:
            name = self._shape_name(a_class_key)
            number_of_instances = float(self._class_counts_dict[a_class_key])

            direct_statements = self._build_base_direct_statements(acceptance_threshold, a_class_key,
                                                                   number_of_instances)
            inverse_statements = self._build_base_inverse_statements(acceptance_threshold=acceptance_threshold,
                                                                     class_key=a_class_key,
                                                                     number_of_instances=number_of_instances)
            yield Shape(name=name,
                        class_uri=a_class_key,
                        statements=direct_statements + inverse_statements,
                        n_instances=int(number_of_instances))

    def set_valid_shape_constraints(self, shape):
        valid_statements = self._select_valid_statements_of_shape(shape.direct_statements)
        valid_statements += self._select_valid_statements_of_shape(shape.inverse_statements)
        self._tune_list_of_valid_statements(valid_statements=valid_statements)
        shape.statements = valid_statements

    def _build_base_inverse_statements(self, acceptance_threshold, class_key, number_of_instances):
        result = []
        for a_prop_key in self._class_profile_dict[class_key][_POS_FEATURES_INVERSE]:
            for a_type_key in self._class_profile_dict[class_key][_POS_FEATURES_INVERSE][a_prop_key]:
                for a_cardinality in self._class_profile_dict[class_key][_POS_FEATURES_INVERSE][a_prop_key][a_type_key]:
                    n_occurences = self._class_profile_dict[class_key][_POS_FEATURES_INVERSE][a_prop_key][a_type_key][a_cardinality]
                    frequency = self._compute_frequency(number_of_instances,
                                                        n_occurences)
                    if frequency >= acceptance_threshold:
                        result.append(Statement(st_property=a_prop_key,
                                                st_type=a_type_key,
                                                cardinality=a_cardinality,
                                                probability=frequency,
                                                n_occurences=n_occurences,
                                                is_inverse=True))
        return result

    def _build_base_direct_statements(self, acceptance_threshold, class_key, number_of_instances):
        result = []
        for a_prop_key in self._class_profile_dict[class_key][_POS_FEATURES_DIRECT]:
            for a_type_key in self._class_profile_dict[class_key][_POS_FEATURES_DIRECT][a_prop_key]:
                for a_cardinality in self._class_profile_dict[class_key][_POS_FEATURES_DIRECT][a_prop_key][a_type_key]:
                    n_occurences = self._class_profile_dict[class_key][_POS_FEATURES_DIRECT][a_prop_key][a_type_key][a_cardinality]
                    frequency = self._compute_frequency(number_of_instances,
                                                        n_occurences)
                    if frequency >= acceptance_threshold:
                        result.append(Statement(st_property=a_prop_key,
                                                st_type=a_type_key,
                                                cardinality=a_cardinality,
                                                probability=frequency,
                                                is_inverse=False,
                                                n_occurences=n_occurences))
        return result

    # def _set_serializer_object_for_statements(self, statement):
    #     statement.serializer_object = BaseStatementSerializer(
    #         instantiation_property_str=self._instantiation_property_str,
    #         disable_comments=self._disable_comments,
    #         is_inverse=statement.is_inverse)
    #
    # def _get_serializer_for_choice_statement(self):
    #     return FixedPropChoiceStatementSerializer(
    #         instantiation_property_str=self._instantiation_property_str,
    #         disable_comments=self._disable_comments,
    #         is_inverse=statement.is_inverse)
