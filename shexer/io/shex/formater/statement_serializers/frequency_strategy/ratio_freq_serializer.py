from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy
from shexer.utils.uri import prefixize_uri_if_possible, add_corners_if_it_is_an_uri

from shexer.io.shex.formater.consts import SPACES_GAP_BETWEEN_TOKENS, ANNOTATION_BEGIN

_FREQUENCY_PATTERN = "{:.3f}"

class RatioFreqSerializer(BaseFrequencyStrategy):

    def __init__(self, frequency_ratio_property, frequency_absolute_property, namespaces_dict, decimals=-1):
        """

        :param decimals: it indicates the number of decimals to use to express ratios.
                        When a negative number is provided, decimals won't be controlled
        """
        super().__init__(frequency_ratio_property, frequency_absolute_property, namespaces_dict)
        self._decimals = decimals
        if decimals < 0:
            self.serialize_frequency = self._serialize_freq_unbounded
        elif decimals == 0:
            self.serialize_frequency = self._serialize_freq_int
        else:
            self.serialize_frequency = self._serialize_freq_decimals
            _FREQUENCY_PATTERN = "{:."+ str(decimals) + "f}"


    def serialize_frequency(self, statement):
        raise NotImplementedError("This function will be initialized with a callback during the __init__")


    def _serialize_freq_unbounded(self, statement):
        return str(statement.probability * 100) + " %"

    def _serialize_freq_decimals(self, statement):
        pattern = "{:." + str(self._decimals) +"f} %"
        return pattern.format(statement.probability*100)

    def _serialize_freq_int(self, statement):
        return str(int(statement.probability * 100)) + " %"

    def annotations_for_frequency(self, statement):

        freq_annotation = SPACES_GAP_BETWEEN_TOKENS.join((ANNOTATION_BEGIN,
                                                          add_corners_if_it_is_an_uri(prefixize_uri_if_possible(target_uri=self._frequency_ratio_property,
                                                                                    namespaces_prefix_dict=self._namespaces_dict,
                                                                                    corners=False)),
                                                          self._format_frequency(statement.probability)
                                                          ))
        return [freq_annotation]

    def _format_frequency(self, frequency_raw_number):
        return _FREQUENCY_PATTERN.format(frequency_raw_number)