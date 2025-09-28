from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import \
    BaseFrequencyStrategy
from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, ANNOTATION_BEGIN
from shexer.utils.uri import prefixize_uri_if_possible, add_corners_if_it_is_an_uri


class AbsFreqSerializer(BaseFrequencyStrategy):

    def __init__(self, frequency_ratio_property, frequency_absolute_property, namespaces_dict):
        super().__init__(frequency_ratio_property, frequency_absolute_property, namespaces_dict)

    def serialize_frequency(self, statement):
        return str(statement.n_occurences) + " instance{}.".format(
            "" if statement.n_occurences == 1
            else "s"
        )

    def annotations_for_frequency(self, statement):
        freq_annotation = SPACES_GAP_BETWEEN_TOKENS.join((ANNOTATION_BEGIN,
                                                          add_corners_if_it_is_an_uri(prefixize_uri_if_possible(
                                                              target_uri=self._frequency_absolute_property,
                                                              namespaces_prefix_dict=self._namespaces_dict,
                                                              corners=False)),
                                                          str(statement.n_occurences)
                                                          ))
        return [freq_annotation]
