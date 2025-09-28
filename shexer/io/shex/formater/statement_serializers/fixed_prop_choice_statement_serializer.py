from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, KLEENE_CLOSURE, OPT_CARDINALITY
from shexer.consts import FREQ_PROP, ABSOLUTE_COUNT_PROP, EXTRA_INFO_PROP


class FixedPropChoiceStatementSerializer(BaseStatementSerializer):

    def __init__(self, instantiation_property_str, frequency_serializer, disable_comments=False, is_inverse=False,
                 frequency_property=FREQ_PROP, namespaces_dict=None, comments_to_annotations=False,
                 extra_info_prop=EXTRA_INFO_PROP, absolute_count_prop=ABSOLUTE_COUNT_PROP):
        super(FixedPropChoiceStatementSerializer, self).__init__(instantiation_property_str=instantiation_property_str,
                                                                 disable_comments=disable_comments,
                                                                 is_inverse=is_inverse,
                                                                 frequency_serializer=frequency_serializer,
                                                                 frequency_property=frequency_property,
                                                                 namespaces_dict=namespaces_dict,
                                                                 comments_to_annotations=comments_to_annotations,
                                                                 extra_info_prop=extra_info_prop,
                                                                 absolute_count_prop=absolute_count_prop)

    def serialize_statement_with_indent_level(self, a_statement, is_last_statement_of_shape):
        tuples_line_indent = []
        st_property = BaseStatementSerializer.tune_token(a_statement.st_property, self._namespaces_dict)
        st_target_elements = []
        for a_type in a_statement.st_types:
            st_target_elements.append(self.str_of_target_element(target_element=a_type,
                                                                 st_property=a_statement.st_property))

        content_line = st_property + SPACES_GAP_BETWEEN_TOKENS
        content_line += (SPACES_GAP_BETWEEN_TOKENS + "OR" + SPACES_GAP_BETWEEN_TOKENS).join(st_target_elements)
        content_line += SPACES_GAP_BETWEEN_TOKENS + BaseStatementSerializer.cardinality_representation(
            statement=a_statement,
            out_of_comment=True)
        if self._comments_to_annotations:
            content_line += self._build_constraint_annotations(a_statement)
        content_line += ";" if not is_last_statement_of_shape else ""
        tuples_line_indent.append((content_line, 1))

        if not self._comments_to_annotations:
            for a_comment in a_statement.comments:
                tuples_line_indent.append((a_comment, 4))
        return tuples_line_indent


    @staticmethod
    def turn_statement_into_comment(statement, namespaces_dict):
        return statement.probability_representation() + \
               " with cardinality " + statement.cardinality_representation()
