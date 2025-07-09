from shexer.core.shexing.strategy.abstract_shexing_strategy import AbstractShexingStrategy
from shexer.model.statement import Statement
from shexer.model.shape import Shape

class DirectShexingStrategy(AbstractShexingStrategy):

    def __init__(self, class_shexer):
        super().__init__(class_shexer)
        self._class_profile_dict = self._class_shexer._class_profile_dict
        self._shapes_namespace = self._class_shexer._shapes_namespace
        self._class_counts_dict = self._class_shexer._class_counts_dict

    def remove_statements_to_gone_shapes(self, shape, shape_names_to_remove):
        shape.direct_statements = self._statements_without_shapes_to_remove(original_statements=shape.direct_statements,
                                                                            shape_names_to_remove=shape_names_to_remove)

    def set_valid_shape_constraints(self, shape):
        valid_statements = self._select_valid_statements_of_shape(shape.direct_statements)
        self._tune_list_of_valid_statements(valid_statements=valid_statements)
        shape.statements = valid_statements


    def _yield_base_shapes_direction_aware(self, acceptance_threshold):
        for a_class_key in self._class_profile_dict:
            name = self._shape_name(a_class_key)
            number_of_instances = float(self._class_counts_dict[a_class_key])
            statements = []
            for a_prop_key in self._class_profile_dict[a_class_key]:
                for a_type_key in self._class_profile_dict[a_class_key][a_prop_key]:
                    for a_cardinality in self._class_profile_dict[a_class_key][a_prop_key][a_type_key]:
                        n_occurences = self._class_profile_dict[a_class_key][a_prop_key][a_type_key][a_cardinality]
                        frequency = self._compute_frequency(number_of_instances,
                                                            n_occurences)
                        if frequency >= acceptance_threshold:
                            statements.append(Statement(st_property=a_prop_key,
                                                        st_type=a_type_key,
                                                        cardinality=a_cardinality,
                                                        probability=frequency,
                                                        n_occurences=n_occurences))

            yield Shape(name=name,
                        class_uri=a_class_key,
                        statements=statements,
                        n_instances=int(number_of_instances))

