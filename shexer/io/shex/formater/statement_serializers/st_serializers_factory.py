from shexer.io.shex.formater.statement_serializers.frequency_strategy.abs_freq_serializer import AbsFreqSerializer
from shexer.io.shex.formater.statement_serializers.frequency_strategy.ratio_freq_serializer import RatioFreqSerializer
from shexer.io.shex.formater.statement_serializers.frequency_strategy.mixed_frequency_strategy import MixedFrequencyStrategy
from shexer.io.shex.formater.statement_serializers.base_statement_serializer import BaseStatementSerializer
from shexer.io.shex.formater.statement_serializers.fixed_prop_choice_statement_serializer import FixedPropChoiceStatementSerializer
from shexer.consts import RATIO_INSTANCES, ABSOLUTE_INSTANCES, MIXED_INSTANCES

class StSerializerFactory(object):
    """
    This factory offers public method with Singletons*. They are not really singletons, as a battery
    of objects are always initialized, no matter which calls the factory receives.

    But the point here is that there is only one isntance of each type of serializer.

    """

    def __init__(self, freq_mode, decimals, instantiation_property_str, disable_comments, frequency_property,
                 namespaces_dict, comments_to_annotations, extra_info_property, absolute_count_property):
        self._freq_serializer = self._build_freq_serializer(freq_mode=freq_mode,
                                                            decimals=decimals,
                                                            freq_prop=frequency_property,
                                                            abs_prop=absolute_count_property,
                                                            namespaces_dict=namespaces_dict)

        self._direct_base = BaseStatementSerializer(
                instantiation_property_str=instantiation_property_str,
                disable_comments=disable_comments,
                is_inverse=False,
                frequency_serializer=self._freq_serializer,
                frequency_property=frequency_property,
                namespaces_dict=namespaces_dict,
                comments_to_annotations=comments_to_annotations,
                extra_info_prop=extra_info_property,
                absolute_count_prop=absolute_count_property)
        self._inverse_base = BaseStatementSerializer(
                instantiation_property_str=instantiation_property_str,
                disable_comments=disable_comments,
                is_inverse=True,
                frequency_serializer=self._freq_serializer,
                frequency_property=frequency_property,
                namespaces_dict=namespaces_dict,
                comments_to_annotations=comments_to_annotations,
                extra_info_prop=extra_info_property,
                absolute_count_prop=absolute_count_property)
        self._direct_choice = FixedPropChoiceStatementSerializer(
                instantiation_property_str=instantiation_property_str,
                disable_comments=disable_comments,
                is_inverse=False,
                frequency_serializer=self._freq_serializer,
                frequency_property=frequency_property,
                namespaces_dict=namespaces_dict,
                comments_to_annotations=comments_to_annotations,
                extra_info_prop=extra_info_property,
                absolute_count_prop=absolute_count_property)
        self._inverse_choice = FixedPropChoiceStatementSerializer(
                instantiation_property_str=instantiation_property_str,
                disable_comments=disable_comments,
                is_inverse=True,
                frequency_serializer=self._freq_serializer,
                frequency_property=frequency_property,
                namespaces_dict=namespaces_dict,
                comments_to_annotations=comments_to_annotations,
                extra_info_prop=extra_info_property,
                absolute_count_prop=absolute_count_property)

    def get_base_serializer(self, is_inverse):
        return self._direct_base if not is_inverse else self._inverse_base

    def get_choice_serializer(self, is_inverse):
        return self._direct_choice if not is_inverse else self._inverse_choice

    def _build_freq_serializer(self, freq_mode, decimals, namespaces_dict, freq_prop, abs_prop):
        if freq_mode == RATIO_INSTANCES:
            return RatioFreqSerializer(decimals=decimals,
                                       namespaces_dict=namespaces_dict,
                                       frequency_ratio_property=freq_prop,
                                       frequency_absolute_property=abs_prop)
        elif freq_mode == ABSOLUTE_INSTANCES:
            return AbsFreqSerializer(namespaces_dict=namespaces_dict,
                                     frequency_ratio_property=freq_prop,
                                     frequency_absolute_property=abs_prop)
        elif freq_mode == MIXED_INSTANCES:
            return MixedFrequencyStrategy(decimals=decimals,
                                          namespaces_dict=namespaces_dict,
                                          frequency_ratio_property=freq_prop,
                                          frequency_absolute_property=abs_prop
                                          )
        else:
            raise ValueError("Unrecognized frequency strategy for serialization. "
                             "Check you used a valid value in the instances_report_mode param")
