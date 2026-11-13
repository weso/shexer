from shexer.model.statement import POSITIVE_CLOSURE, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.model.const_elem_types import NONLITERAL_ELEM_TYPE, BNODE_ELEM_TYPE, IRI_ELEM_TYPE, UNSHAPED_ELEM_TYPE
from shexer.model.fixed_prop_choice_statement import FixedPropChoiceStatement
from shexer.model.statement import Statement
from shexer.io.shex.formater.statement_serializers.st_serializers_factory import StSerializerFactory
from shexer.core.shexing.strategy.minimal_iri_strategy.annotate_min_iri_strategy import AnnotateMinIriStrategy
from shexer.core.shexing.strategy.minimal_iri_strategy.ignore_min_iri_strategy import IgnoreMinIriStrategy
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME


_DIRECT_ST_SERIALIZER = 0
_INVERSE_ST_SERIALIZER = 1
_NODE_KIND_COUNTERS = (NONLITERAL_ELEM_TYPE, UNSHAPED_ELEM_TYPE)


class AbstractShexingStrategy(object):

    def __init__(self, class_shexer):
        self._class_shexer = class_shexer
        self._namespaces_dict = class_shexer._namespaces_dict
        self._allow_opt_cardinality = class_shexer._allow_opt_cardinality
        self._disable_comments = self._class_shexer._disable_comments
        self._instantiation_property_str = self._class_shexer._instantiation_property_str
        self._keep_less_specific = self._class_shexer._keep_less_specific
        self._discard_useless_positive_closures = self._class_shexer._discard_useless_positive_closures
        self._tolerance = self._class_shexer._tolerance
        self._disable_or_statements = self._class_shexer._disable_or_statements
        self._all_compliant_mode = self._class_shexer._all_compliant_mode
        self._disable_exact_cardinality = self._class_shexer._disable_exact_cardinality
        self._allow_redundant_or = self._class_shexer._allow_redundant_or
        self._shape_names_dict = self._class_shexer._shape_names_dict

        self._strategy_min_iri = AnnotateMinIriStrategy(class_shexer._class_min_iris_dict) \
            if class_shexer._detect_minimal_iri \
            else IgnoreMinIriStrategy()

        self._statement_serializer_factory = StSerializerFactory(freq_mode=class_shexer._instances_report_mode,
                                                                 decimals=class_shexer._decimals,
                                                                 instantiation_property_str=self._instantiation_property_str,
                                                                 disable_comments=self._disable_comments,
                                                                 frequency_property=self._class_shexer._frequency_property,
                                                                 namespaces_dict=self._namespaces_dict,
                                                                 comments_to_annotations=class_shexer._comments_to_annotations,
                                                                 extra_info_property=self._class_shexer._extra_info_property,
                                                                 absolute_count_property=self._class_shexer._absolute_count_property)


    def yield_base_shapes(self, acceptance_threshold):
        for a_shape in self._yield_base_shapes_direction_aware(acceptance_threshold=acceptance_threshold):
            self._strategy_min_iri.annotate_shape_iri(a_shape)
            yield a_shape

    def _yield_base_shapes_direction_aware(self, acceptance_threshold):
        raise NotImplementedError()

    def set_valid_shape_constraints(self, shape):
        raise NotImplementedError()

    def remove_statements_to_gone_shapes(self, shape, shape_names_to_remove):
        raise NotImplementedError()

    def _tune_list_of_valid_statements(self, valid_statements):
        """
        This method modifies the statements objects received --> no return needed
        :param valid_statements:
        :return:
        """
        if not len(valid_statements) == 0:
            valid_statements.sort(reverse=True, key=lambda x: x.probability)  # Restoring order completely
                                                                              # before changing cardinalities

            if self._all_compliant_mode:
                self._modify_cardinalities_of_statements_non_compliant_with_all_instances(valid_statements)

            if self._disable_exact_cardinality:
                self._generalize_exact_cardinalities(valid_statements)

            if self._disable_comments:
                self._remove_comments_from_statements(valid_statements)

    def _select_valid_statements_of_shape(self, original_statements):
        if len(original_statements) == 0:
            return []

        for a_statement in original_statements:  # TODO Refactor!!! This is not the place to set the serializer
            self._set_serializer_object_for_statements(a_statement)

        histograms = self._cardinality_histograms(original_statements)
        result = self._group_constraints_with_same_prop_and_obj(original_statements)
        result = self._group_node_constraints(result, histograms)

        return result

    @staticmethod
    def _cardinality_histograms(statements):
        result = {}
        for a_statement in statements:
            if type(a_statement.cardinality) == int:
                key = (a_statement.st_property, a_statement.is_inverse, a_statement.st_type)
                result.setdefault(key, {})[a_statement.cardinality] = a_statement.n_occurences
        return result

    def _compute_frequency(self, number_of_instances, n_ocurrences_statement):
        return float(n_ocurrences_statement) / number_of_instances

    def _modify_cardinalities_of_statements_non_compliant_with_all_instances(self, statements):
        for a_statement in statements:
            if a_statement.probability != 1:
                self._change_statement_cardinality_to_all_compliant(a_statement)

    def _change_statement_cardinality_to_all_compliant(self, statement):
        comment_for_current_sentence = self._turn_statement_into_comment(statement, self._namespaces_dict)
        statement.add_comment(comment=comment_for_current_sentence,
                              insert_first=True)
        statement.cardinality = OPT_CARDINALITY if \
            self._allow_opt_cardinality and statement.cardinality == 1 \
            else KLEENE_CLOSURE
        # statement.probability = 1


    @staticmethod
    def _turn_statement_into_comment(a_statement, namespaces_dict):
        return a_statement.comment_representation(namespaces_dict=namespaces_dict)

    def _generalize_exact_cardinalities(self, statements):
        for a_statement in statements:
            if type(a_statement.cardinality) == int and a_statement.cardinality > 1:
                a_statement.cardinality = POSITIVE_CLOSURE

    def _remove_comments_from_statements(self, valid_statements):
        for a_statement in valid_statements:
            a_statement.remove_comments()

    def _set_serializer_object_for_statements(self, statement):
        statement.serializer_object = self._statement_serializer_factory.get_base_serializer(
            is_inverse=statement.is_inverse
        )

    def _group_constraints_with_same_prop_and_obj(self, candidate_statements):  # TODO REFACTORING
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement not in already_visited:
                already_visited.add(a_statement)
                group_to_decide = MergeableConstraints(a_statement)  # TODO
                for j in range(i + 1, len(candidate_statements)):
                    if self._statements_have_same_tokens(a_statement,
                                                         candidate_statements[j]):
                        group_to_decide.add_constraint(candidate_statements[j])
                        already_visited.add(candidate_statements[j])
                if len(group_to_decide) == 1:
                    result.append(a_statement)
                else:
                    result.append(self._decide_best_statement_with_cardinalities_in_comments(group_to_decide))
        return result

    def _statements_have_same_tokens(self, st1, st2):
        if st1.st_property == st2.st_property and st1.st_type == st2.st_type:
            return True
        return False

    def _decide_best_statement_with_cardinalities_in_comments(self, mergeable_constraints):  # TODO REFACTORING
        if self._discard_useless_positive_closures:
            if self._is_a_group_of_statements_with_useless_positive_closure(mergeable_constraints):
                return self._statement_for_a_group_with_a_useless_positive_closure(mergeable_constraints)
        mergeable_constraints.sort()
        result = None
        if self._keep_less_specific \
                or self._all_compliant_mode and self._has_several_exact_cardinalities(mergeable_constraints):
            for a_statement in mergeable_constraints.constraints():
                if a_statement.cardinality == POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = mergeable_constraints.get(0)
        else:
            for a_statement in mergeable_constraints.constraints():
                if a_statement.cardinality != POSITIVE_CLOSURE:
                    result = a_statement
                    break
            if result is None:
                result = mergeable_constraints.get(0)

        for a_statement in mergeable_constraints.constraints():
            if a_statement.cardinality != result.cardinality:
                result.add_comment(self._turn_statement_into_comment(a_statement, self._namespaces_dict))
        return result

    @staticmethod
    def _has_several_exact_cardinalities(mergeable_constraints):
        return len([a_statement for a_statement in mergeable_constraints.constraints()
                    if a_statement.cardinality != POSITIVE_CLOSURE]) > 1

    def _is_a_group_of_statements_with_useless_positive_closure(self, list_of_candidate_sentences):  # todo during refactor
        if len(list_of_candidate_sentences) != 2:
            return False
        if abs(list_of_candidate_sentences.get(0).probability - list_of_candidate_sentences.get(1).probability) > self._tolerance:
            return False
        one_if_there_is_a_single_positive_closure = -1
        for a_statement in list_of_candidate_sentences.constraints():
            if POSITIVE_CLOSURE == a_statement.cardinality:
                one_if_there_is_a_single_positive_closure *= -1
        if one_if_there_is_a_single_positive_closure == 1:
            return True
        return False

    def _statement_for_a_group_with_a_useless_positive_closure(self, group_of_candidate_statements):  # TODO DURING REFACTOR
        for a_statement in group_of_candidate_statements.constraints():
            if a_statement.cardinality != POSITIVE_CLOSURE:
                return a_statement
        raise ValueError("The received group does not contain any statement with positive closure")

    def _group_node_constraints(self, candidate_statements, histograms):
        node_kind_counters = {(a_statement.st_property, a_statement.is_inverse, a_statement.st_type): a_statement
                              for a_statement in candidate_statements
                              if a_statement.st_type in _NODE_KIND_COUNTERS}
        result = []
        already_visited = set()
        for i in range(0, len(candidate_statements)):
            a_statement = candidate_statements[i]
            if a_statement.st_type in _NODE_KIND_COUNTERS:
                continue
            if a_statement.st_property == self._instantiation_property_str or self._is_a_literal(a_statement.st_type):
                result.append(a_statement)
                already_visited.add(a_statement)
            else:  # a_statement.st_property != self._instantiation_property_str and it is not a literal obj
                if a_statement not in already_visited:
                    already_visited.add(a_statement)
                    group_to_decide = MergeableConstraints(initial_constraint=a_statement,
                                                           statement_serializer_factory=self._statement_serializer_factory,
                                                           namespaces_dict=self._namespaces_dict,
                                                           histograms=histograms,
                                                           node_kind_counters=node_kind_counters)

                    result.append(self._find_and_merge_potentially_swapped_constraints(
                        mergeable_constraints=group_to_decide,
                        already_visited=already_visited,
                        all_original_statements=candidate_statements,
                        target_index_original_statements=i+1,
                    ))
        return result

    def _find_and_merge_potentially_swapped_constraints(self, mergeable_constraints,
                                                        already_visited,
                                                        all_original_statements,
                                                        target_index_original_statements):
        self._find_all_candidates_to_merge_swapped_constraints_at_node_level(
            mergeable_constraints=mergeable_constraints,
            already_visited=already_visited,
            all_original_statements=all_original_statements,
            target_index_original_statements=target_index_original_statements
        )
        return self._merge_swapped_constraints_at_node_level(  # TODO
            group_to_merge=mergeable_constraints
        )

    def _find_all_candidates_to_merge_swapped_constraints_at_node_level(self,
                                                                        mergeable_constraints,
                                                                        already_visited,
                                                                        all_original_statements,
                                                                        target_index_original_statements):
        for j in range(target_index_original_statements, len(all_original_statements)):
            if self._statements_have_same_prop_and_are_node_type(mergeable_constraints.get(0),  # todo check have_same_prop_behaviour
                                                                 all_original_statements[j]):
                mergeable_constraints.add_constraint(all_original_statements[j])
                already_visited.add(all_original_statements[j])
        # No need to return anything, modifying the received parameters.

    def _statements_have_same_prop_and_are_node_type(self, original_sentence,
                                                           target_sentence):
        # In this context, we can assume that the original one does not point to a literal
        if target_sentence.st_type in [IRI_ELEM_TYPE, BNODE_ELEM_TYPE] or target_sentence.st_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME):
            return original_sentence.st_property == target_sentence.st_property
        return False

    def _merge_swapped_constraints_at_node_level(self, group_to_merge):
        if len(group_to_merge) == 1:
            return group_to_merge.get(0)
        group_to_merge.sort()
        return group_to_merge.merge_group(disable_or=self._disable_or_statements,
                                          redundant_or_allowed=self._allow_redundant_or)



    def _statements_without_shapes_to_remove(self, original_statements, shape_names_to_remove):
        new_statements = []
        for a_statement in original_statements:
            if not a_statement.st_type in shape_names_to_remove:
                new_statements.append(a_statement)
        return new_statements

    def _is_a_literal(self, node_kind_str):
        if node_kind_str.startswith(STARTING_CHAR_FOR_SHAPE_NAME):
            return False
        if node_kind_str in [IRI_ELEM_TYPE, BNODE_ELEM_TYPE]:
            return False
        return True


    def _shape_name(self, class_key):
        if class_key.startswith("<"):
            return STARTING_CHAR_FOR_SHAPE_NAME + class_key
        return f"{STARTING_CHAR_FOR_SHAPE_NAME}<{self._shape_names_dict[class_key]}>"

class MergeableConstraints(object):
    """
    Internal class used to handle constraints created during the voting process that should be merged into a single one.
    """
    def __init__(self, initial_constraint=None, statement_serializer_factory=None, namespaces_dict=None,
                 histograms=None, node_kind_counters=None):
        self._constraints = []
        self._bnode_constraint = None
        self._shape_constraints = None
        self._iri_constraint = None
        self._dominant_constraint = None
        self._dominant_is_shape = False
        self._disable_or = True
        self._redundant_or_enabled = False
        self._statement_serializer_factory = statement_serializer_factory
        self._namespaces_dict = namespaces_dict
        self._histograms = {} if histograms is None else histograms
        self._node_kind_counters = {} if node_kind_counters is None else node_kind_counters
        if initial_constraint is not None:
            self.add_constraint(initial_constraint)

    def add_constraint(self, statement):
        self._constraints.append(statement)
        if statement.st_type == BNODE_ELEM_TYPE:
            self._bnode_constraint = statement
        elif statement.st_type == IRI_ELEM_TYPE:
            self._iri_constraint = statement
        else:
            if self._shape_constraints is None:
                self._shape_constraints = []
            self._shape_constraints.append(statement)


    @property
    def has_bnodes(self):
        return self._bnode_constraint is not None

    @property
    def has_iri_constraint(self):
        return self._iri_constraint is not None

    @property
    def has_shape_constraints(self):
        return self._shape_constraints is not None

    def get(self, index):
        return self._constraints[index]

    def __len__(self):
        return len(self._constraints)

    def sort(self):
        self._constraints.sort(reverse=True, key=lambda x: x.probability)
        if self._shape_constraints is not None:
            self._shape_constraints.sort(reverse=True, key=lambda x: x.probability)

    def constraints(self):
        for a_constaint in self._constraints:
            yield a_constaint

    def merge_group(self, disable_or, redundant_or_allowed):
        self.sort()
        self._disable_or = disable_or
        self._redundant_or_enabled = redundant_or_allowed
        general_constraint = self._general_constraint()
        if self._a_shape_can_replace(general_constraint):
            self._dominant_constraint = self._shape_with_cardinality_of(self._shape_constraints[0], general_constraint)
            self._dominant_is_shape = True
        else:
            self._dominant_constraint = general_constraint
        self._merge_content_in_single_statement()
        return self._dominant_constraint

    def _general_constraint(self):
        if self._bnode_constraint is None:
            return self._iri_constraint
        if self._iri_constraint is None:
            return self._bnode_constraint
        return self._node_kind_counters[self._key(NONLITERAL_ELEM_TYPE)]

    def _a_shape_can_replace(self, general_constraint):
        if not self.has_shape_constraints \
                or self._shape_constraints[0].n_occurences < general_constraint.n_occurences:
            return False
        if self._histogram(self._shape_constraints[0].st_type) == self._histogram(general_constraint.st_type):
            return True
        return not self._disable_or and self._key(UNSHAPED_ELEM_TYPE) not in self._histograms

    def _histogram(self, st_type):
        return self._histograms.get(self._key(st_type))

    def _key(self, st_type):
        a_constraint = self._constraints[0]
        return a_constraint.st_property, a_constraint.is_inverse, st_type

    @staticmethod
    def _shape_with_cardinality_of(shape_constraint, general_constraint):
        return Statement(st_property=shape_constraint.st_property,
                         st_type=shape_constraint.st_type,
                         cardinality=general_constraint.cardinality,
                         n_occurences=general_constraint.n_occurences,
                         probability=general_constraint.probability,
                         comments=list(shape_constraint.comments),
                         serializer_object=shape_constraint.serializer_object,
                         is_inverse=shape_constraint.is_inverse)

    def _merge_content_in_single_statement(self):
        self._tune_dominant_constraint_wrt_or_config()
        self._feed_dominant_constraint_with_comments()

    def _feed_dominant_constraint_with_comments(self):
        if self._bnode_constraint is not None:
            self._dominant_constraint.add_comment(
                AbstractShexingStrategy._turn_statement_into_comment(self._bnode_constraint,
                                                                     self._namespaces_dict)
            )
            if self._iri_constraint is not None:  # Add IRI one only if there are both bnodes and iris.
                self._dominant_constraint.add_comment(
                    AbstractShexingStrategy._turn_statement_into_comment(self._iri_constraint,
                                                                         self._namespaces_dict)
                )
        for a_constraint in self._shape_constraints or []:
            if not self._dominant_is_shape or a_constraint is not self._shape_constraints[0]:
                self._dominant_constraint.add_comment(
                    AbstractShexingStrategy._turn_statement_into_comment(a_constraint,
                                                                         self._namespaces_dict)
                )

    def _tune_dominant_constraint_wrt_or_config(self):
        if self._disable_or:
            return
        st_types = []
        if self._redundant_or_enabled and not self._dominant_is_shape:
            st_types.append(self._dominant_constraint.st_type)
        if self._redundant_or_enabled or self._dominant_is_shape:
            st_types = st_types + [a_constraint.st_type for a_constraint in self._shape_constraints or []]
        if len(st_types) > 1:
            self._dominant_constraint = FixedPropChoiceStatement(
                st_property=self._dominant_constraint.st_property,
                st_types=st_types,
                cardinality=self._dominant_constraint.cardinality,
                probability=self._dominant_constraint.probability,
                n_occurences=self._dominant_constraint.n_occurences,
                serializer_object=self._statement_serializer_factory.get_choice_serializer(
                    is_inverse=self._dominant_constraint.is_inverse
                ),
                is_inverse=self._dominant_constraint.is_inverse)

