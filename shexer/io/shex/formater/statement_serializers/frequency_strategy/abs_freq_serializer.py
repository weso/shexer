
from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy

class AbsFreqSerializer(BaseFrequencyStrategy):

    def __init__(self, frequency_ratio_property, frequency_absolute_property,namespaces_dict):
        super().__init__(frequency_ratio_property, frequency_absolute_property,namespaces_dict)

    def serialize_frequency(self, statement):
        return str(statement.n_occurences) + " instance{}.".format(
            "" if statement.n_occurences == 1
            else "s"
        )




