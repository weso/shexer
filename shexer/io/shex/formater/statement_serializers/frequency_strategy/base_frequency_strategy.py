
class BaseFrequencyStrategy(object):


    def __init__(self, frequency_ratio_property, frequency_absolute_property, namespaces_dict):
        self._frequency_ratio_property = frequency_ratio_property
        self._frequency_absolute_property = frequency_absolute_property
        self._namespaces_dict = namespaces_dict

    def serialize_frequency(self, statement):
        raise NotImplementedError("This should be implemented in child classes")

    def annotations_for_frequency(self, statement):
        raise NotImplementedError("This should be implemented in child classes")