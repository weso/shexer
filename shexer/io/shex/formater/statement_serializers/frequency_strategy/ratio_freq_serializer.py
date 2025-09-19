from shexer.io.shex.formater.statement_serializers.frequency_strategy.base_frequency_strategy import BaseFrequencyStrategy

class RatioFreqSerializer(BaseFrequencyStrategy):

    def __init__(self, decimals=-1):
        """

        :param decimals: it indicates the number of decimals to use to express ratios.
                        When a negative number is provided, decimals won't be controlled
        """
        self._decimals = decimals
        if decimals < 0:
            self.serialize_frequency = self._serialize_freq_unbounded
        elif decimals == 0:
            self.serialize_frequency = self._serialize_freq_int
        else:
            self.serialize_frequency = self._serialize_freq_decimals


    def serialize_frequency(self, statement):
        raise NotImplementedError("This function will be initialized with a callback during the __init__")

    def _serialize_freq_unbounded(self, statement):
        return str(statement.probability * 100) + " %"

    def _serialize_freq_decimals(self, statement):
        pattern = "{:." + str(self._decimals) +"f} %"
        return pattern.format(statement.probability*100)

    def _serialize_freq_int(self, statement):
        return str(int(statement.probability * 100)) + " %"
