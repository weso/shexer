from shexer.core.instances.abstract_instance_tracker import AbstractInstanceTracker
from shexer.utils.log import log_msg


class ShapeMapInstanceTracker(AbstractInstanceTracker):

    def __init__(self, shape_map):
        self._shape_map = shape_map
        self._instances_dict = {}

    def track_instances(self, verbose=False):
        log_msg(verbose=verbose,
                msg="Starting instance tracker...")
        for an_item in self._shape_map.yield_items():
            self._solve_targets_of_an_item(an_item)
        log_msg(verbose=verbose,
                msg="Instance tracker finished. {} instances located".format(len(self._instances_dict)))
        return self._instances_dict

    @property
    def shape_map(self):
        return self._shape_map

    def _solve_targets_of_an_item(self, an_item):
        for a_node in an_item.node_selector.get_target_nodes():
            if a_node not in self._instances_dict:
                self._instances_dict[a_node] = []
            self._instances_dict[a_node].append(an_item.shape_label)

    def _specific_disambiguator_prefix(self):
        return "custom_"
