from shexer.utils.obj_references import check_just_one_not_none

from shexer.consts import SHEXC, SHACL_TURTLE, NT, TSV_SPO, N3, TURTLE, TURTLE_ITER, \
    RDF_XML, FIXED_SHAPE_MAP, JSON_LD, RDF_TYPE, SHAPES_DEFAULT_NAMESPACE, ZIP, GZ, XZ, \
    ALL_EXAMPLES, CONSTRAINT_EXAMPLES, SHAPE_EXAMPLES
from shexer.utils.factories.class_profiler_factory import get_class_profiler
from shexer.utils.factories.instance_tracker_factory import get_instance_tracker
from shexer.utils.factories.class_shexer_factory import get_class_shexer
from shexer.utils.factories.remote_graph_factory import get_remote_graph_if_needed
from shexer.utils.factories.shape_map_factory import get_shape_map_if_needed
from shexer.io.profile.formater.abstract_profile_serializer import AbstractProfileSerializer
from shexer.utils.factories.shape_serializer_factory import get_shape_serializer, get_uml_serializer
from shexer.utils.namespaces import find_adequate_prefix_for_shapes_namespaces
from shexer.utils.log import log_msg
from shexer.utils.uri import unprefixize_uri_if_possible
from shexer.utils.dict import reverse_keys_and_values
from shexer.consts import RATIO_INSTANCES


class Shaper(object):

    def __init__(self, target_classes=None,
                 file_target_classes=None,
                 input_format=NT,
                 instances_file_input=None,
                 graph_file_input=None,
                 graph_list_of_files_input=None,
                 raw_graph=None,
                 url_graph_input=None,
                 rdflib_graph=None,
                 list_of_url_input=None,
                 namespaces_dict=None,
                 # namespaces_dict_file=None,
                 instantiation_property=RDF_TYPE,
                 namespaces_to_ignore=None,
                 infer_numeric_types_for_untyped_literals=True,
                 discard_useless_constraints_with_positive_closure=True,
                 all_instances_are_compliant_mode=True,
                 keep_less_specific=True,
                 all_classes_mode=False,
                 shape_map_file=None,
                 shape_map_raw=None,
                 depth_for_building_subgraph=1,
                 track_classes_for_entities_at_last_depth_level=False,
                 strict_syntax_with_corners=False,
                 url_endpoint=None,
                 shape_map_format=FIXED_SHAPE_MAP,
                 shape_qualifiers_mode=False,
                 namespaces_for_qualifier_props=None,
                 remove_empty_shapes=True,
                 disable_comments=False,
                 disable_or_statements=True,
                 allow_opt_cardinality=True,
                 disable_exact_cardinality=False,
                 shapes_namespace=SHAPES_DEFAULT_NAMESPACE,
                 limit_remote_instances=-1,
                 wikidata_annotation=False,
                 inverse_paths=False,
                 compression_mode=None,
                 decimals=-1,
                 instances_report_mode=RATIO_INSTANCES,
                 disable_endpoint_cache=False,
                 detect_minimal_iri=False,
                 allow_redundant_or=False,
                 instances_cap=-1,
                 examples_mode=None,
                 federated_sources=None  # could be a list
                 ):
        """

        :param target_classes:
        :param file_target_classes:
        :param input_format:
        :param instances_file_input:
        :param graph_file_input:
        :param graph_list_of_files_input:
        :param raw_graph:
        :param url_graph_input:
        :param rdflib_graph:
        :param list_of_url_input:
        :param namespaces_dict:
        :param instantiation_property:
        :param namespaces_to_ignore:
        :param infer_numeric_types_for_untyped_literals:
        :param discard_useless_constraints_with_positive_closure:
        :param all_instances_are_compliant_mode:
        :param keep_less_specific:
        :param all_classes_mode:
        :param shape_map_file:
        :param shape_map_raw:
        :param depth_for_building_subgraph:
        :param track_classes_for_entities_at_last_depth_level:
        :param strict_syntax_with_corners:
        :param url_endpoint:
        :param shape_map_format:
        :param shape_qualifiers_mode:
        :param namespaces_for_qualifier_props:
        :param remove_empty_shapes:
        :param disable_comments:
        :param disable_or_statements:
        :param allow_opt_cardinality:
        :param disable_exact_cardinality:
        :param shapes_namespace:
        :param limit_remote_instances:
        :param wikidata_annotation:
        :param inverse_paths:
        :param compression_mode:
        :param decimals:
        :param instances_report_mode:
        :param disable_endpoint_cache:
        :param detect_minimal_iri:
        :param allow_redundant_or:
        :param instances_cap:
        :param examples_mode:
        :param federated_sources
        """

        check_just_one_not_none((graph_file_input, "graph_file_input"),
                                (graph_list_of_files_input, "graph_list_of_files_input"),
                                (raw_graph, "raw_graph"),
                                (url_graph_input, "url_input"),
                                (list_of_url_input, "list_of_url_input"),
                                (url_endpoint, "url_endpoint"),
                                (rdflib_graph, "rdflib_graph")
                                )

        # check_one_or_zero_not_none((namespaces_dict, "namespaces_dict"),
        #                            (namespaces_dict_file, "namespaces_dict_file"))

        self._check_target_classes(target_classes=target_classes,
                                   file_target_classes=file_target_classes,
                                   all_classes_mode=all_classes_mode,
                                   shape_map_raw=shape_map_raw,
                                   shape_map_file=shape_map_file)

        self._check_or_config(or_disabled=disable_or_statements,
                              enable_redundant=allow_redundant_or)

        #TODO ---> Param check of shape_map and graph_via_shape_map

        self._check_input_format(input_format)

        self._check_compression_mode(compression_mode, url_endpoint, url_graph_input, list_of_url_input)

        self._check_examples_mode(examples_mode)

        self._target_classes = target_classes
        self._file_target_classes = file_target_classes
        self._input_format = input_format
        self._instances_file_input = instances_file_input
        self._graph_file_input = graph_file_input
        self._graph_list_of_files_input = graph_list_of_files_input
        self._url_graph_input = url_graph_input
        self._list_of_url_input = list_of_url_input
        self._rdflib_graph = rdflib_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._instantiation_property = \
            unprefixize_uri_if_possible(instantiation_property,
                                        include_corners=False,
                                        prefix_namespaces_dict=reverse_keys_and_values(self._namespaces_dict))
        self._namespaces_to_ignore = namespaces_to_ignore
        self._infer_numeric_types_for_untyped_literals = infer_numeric_types_for_untyped_literals
        self._discard_useles_constraints_with_positive_closure = discard_useless_constraints_with_positive_closure
        self._all_compliant_mode = all_instances_are_compliant_mode
        self._keep_less_specific = keep_less_specific
        self._raw_graph = raw_graph
        self._all_classes_mode = all_classes_mode
        self._shape_map_file = shape_map_file
        self._shape_map_raw = shape_map_raw
        self._decimals = decimals
        self._instances_report_mode = instances_report_mode
        self._disable_endpoint_cache=disable_endpoint_cache
        self._allow_redundant_or = allow_redundant_or
        self._instances_cap = instances_cap

        self._remove_empty_shapes=remove_empty_shapes
        self._disable_comments = disable_comments
        self._disable_or_statements = disable_or_statements
        self._allow_opt_cardinality = allow_opt_cardinality
        self._disable_exact_cardinality = disable_exact_cardinality
        # TODO: REMOVE THE _limit_remote_instances PARAMETER IN FUTURE RELEASES
        self._limit_remote_instances = limit_remote_instances if instances_cap==-1 else instances_cap
        self._wikidata_annotation = wikidata_annotation
        self._inverse_paths = inverse_paths
        self._detect_minimal_iri = detect_minimal_iri
        self._examples_mode = examples_mode
        self._federated_sources = federated_sources

        self._compression_mode = compression_mode

        self._depth_for_building_subgraph = depth_for_building_subgraph
        self._track_classes_for_entities_at_last_depth_level = track_classes_for_entities_at_last_depth_level
        self._url_endpoint = url_endpoint
        self._strict_syntax_with_corners = strict_syntax_with_corners
        self._shape_map_format = shape_map_format
        self._shape_qualifiers_mode = shape_qualifiers_mode
        self._namespaces_for_qualifier_props = namespaces_for_qualifier_props
        self._shapes_namespace = shapes_namespace

        self._add_shapes_namespaces_to_namespaces_dict()


        #The following two atts are used for optimizations
        self._built_remote_graph = get_remote_graph_if_needed(endpoint_url=url_endpoint,
                                                              store_locally=not disable_endpoint_cache)
        self._built_shape_map = get_shape_map_if_needed(sm_format=self._shape_map_format,
                                                        remote_sgraph=self._built_remote_graph,
                                                        namespaces_prefix_dict=self._namespaces_dict,
                                                        target_classes=self._target_classes,
                                                        file_target_classes=self._file_target_classes,
                                                        shape_map_file=self._shape_map_file,
                                                        shape_map_raw=self._shape_map_raw,
                                                        instantiation_property=self._instantiation_property,
                                                        shape_map_already_built=None,
                                                        rdflib_graph=self._rdflib_graph,
                                                        raw_graph=self._raw_graph,
                                                        input_format=self._input_format,
                                                        source_file_graph=self._graph_file_input,
                                                        limit_remote_instances=self._limit_remote_instances)



        self._instance_tracker = None
        self._target_classes_dict = None
        self._class_profiler = None
        self._profile = None
        self._class_counts = None
        self._class_min_iris = None
        self._class_shexer = None
        self._shape_list = None

    def profile_graph(self, string_output=False, output_file=None, verbose=False):
        self._check_correct_output_params(string_output, output_file)
        if self._target_classes_dict is None:
            self._launch_instance_tracker(verbose=verbose)
        if self._profile is None:
            self._launch_class_profiler(verbose=verbose)
        log_msg(verbose=verbose,
                msg="Building_output...")
        if string_output:
            return AbstractProfileSerializer(self._profile).get_string_representation()
        return AbstractProfileSerializer(self._profile).write_profile_to_file(target_file=output_file)

    def shex_graph(self, string_output=False,
                   output_file=None,
                   output_format=SHEXC,
                   acceptance_threshold=0,
                   verbose=False,
                   to_uml_path=None):
        """
        :param string_output:
        :param output_file:
        :param output_format:
        :param acceptance_threshold:
        :param verbose:
        :param to_uml_path:
        :return:
        """
        self._check_correct_output_params(string_output, output_file, to_uml_path)
        self._check_output_format(output_format)
        self._check_aceptance_threshold(acceptance_threshold)
        if self._target_classes_dict is None:
            self._launch_instance_tracker(verbose=verbose)
        if self._profile is None:
            self._launch_class_profiler(verbose=verbose)
        if self._shape_list is None:
            self._launch_class_shexer(acceptance_threshold=acceptance_threshold,
                                      verbose=verbose)
        log_msg(verbose=verbose,
                msg="Building_output...")

        if to_uml_path is not None:
            log_msg(verbose=verbose,
                    msg="Trying to generat UML diagram...")
            try:
                self._generate_uml_diagram(to_uml_path)
                log_msg(verbose=verbose,
                        msg="UML diagram generated...")
            except ResourceWarning as e:  # I think this is related to UMLPlant and I can't close the connection from here
                pass

        if string_output or output_file is not None:
            log_msg(verbose=verbose,
                    msg="Generating text serialization...")
            serializer = self._build_shapes_serializer(target_file=output_file,
                                                       string_return=string_output,
                                                       output_format=output_format)

            return serializer.serialize_shapes()  # If string return is active, returns string.


    def _generate_uml_diagram(self, to_uml_path):
        serializer = get_uml_serializer(shapes_list=self._shape_list,
                                        image_path=to_uml_path,
                                        namespaces_dict=self._namespaces_dict)
        serializer.serialize_shapes()




    def _add_shapes_namespaces_to_namespaces_dict(self):
        self._namespaces_dict[self._shapes_namespace] = \
            find_adequate_prefix_for_shapes_namespaces(self._namespaces_dict)

    def _launch_class_profiler(self, verbose=False):
        if self._class_profiler is None:
            self._class_profiler = self._build_class_profiler()
        self._profile, self._class_counts, self._class_min_iris = self._class_profiler.profile_classes(verbose=verbose)

    def _launch_class_shexer(self, acceptance_threshold, verbose=False):
        if self._class_shexer is None:
            self._class_shexer = self._build_class_shexer()
        self._shape_list = self._class_shexer.shex_classes(acceptance_threshold=acceptance_threshold,
                                                           verbose=verbose)

    def _launch_instance_tracker(self, verbose=False):
        if self._instance_tracker is None:
            self._instance_tracker = self._build_instance_tracker()
        self._target_classes_dict = self._instance_tracker.track_instances(verbose=verbose)

    def _build_class_shexer(self):
        return get_class_shexer(class_counts=self._class_counts,
                                class_profile_dict=self._profile,
                                original_target_classes=self._target_classes,
                                original_shape_map=self._built_shape_map,
                                remove_empty_shapes=self._remove_empty_shapes,
                                discard_useless_constraints_with_positive_closure=
                                self._discard_useles_constraints_with_positive_closure,
                                keep_less_specific=self._keep_less_specific,
                                all_compliant_mode=self._all_compliant_mode,
                                instantiation_property=self._instantiation_property,
                                disable_or_statements=self._disable_or_statements,
                                disable_comments=self._disable_comments,
                                namespaces_dict=self._namespaces_dict,
                                allow_opt_cardinality=self._allow_opt_cardinality,
                                disable_exact_cardinality=self._disable_exact_cardinality,
                                shapes_namespace=self._shapes_namespace,
                                inverse_paths=self._inverse_paths,
                                decimals=self._decimals,
                                instances_report_mode=self._instances_report_mode,
                                detect_minimal_iri=self._detect_minimal_iri,
                                class_min_iris=self._class_min_iris,
                                allow_redundant_or=self._allow_redundant_or,
                                federated_sources=self._federated_sources)

    def _build_shapes_serializer(self, target_file, string_return, output_format):
        return get_shape_serializer(shapes_list=self._shape_list,
                                    target_file=target_file,
                                    string_return=string_return,
                                    namespaces_dict=self._namespaces_dict,
                                    output_format=output_format,
                                    instantiation_property=self._instantiation_property,
                                    disable_comments=self._disable_comments,
                                    wikidata_annotation=self._wikidata_annotation,
                                    instances_report_mode=self._instances_report_mode,
                                    detect_minimal_iri=self._detect_minimal_iri,
                                    shape_features_examples=self._class_min_iris,
                                    examples_mode=self._examples_mode,
                                    inverse_paths=self._inverse_paths)

    def _build_class_profiler(self):
        return get_class_profiler(target_classes_dict=self._target_classes_dict,
                                  source_file=self._graph_file_input,
                                  list_of_source_files=self._graph_list_of_files_input,
                                  input_format=self._input_format,
                                  instantiation_property_str=self._instantiation_property,
                                  namespaces_to_ignore=self._namespaces_to_ignore,
                                  infer_numeric_types_for_untyped_literals=self._infer_numeric_types_for_untyped_literals,
                                  raw_graph=self._raw_graph,
                                  namespaces_dict=self._namespaces_dict,
                                  url_input=self._url_graph_input,
                                  list_of_url_input=self._list_of_url_input,
                                  rdflib_graph=self._rdflib_graph,
                                  shape_map_file=self._shape_map_file,
                                  shape_map_raw=self._shape_map_raw,
                                  track_classes_for_entities_at_last_depth_level=self._track_classes_for_entities_at_last_depth_level,
                                  depth_for_building_subgraph=self._depth_for_building_subgraph,
                                  url_endpoint=self._url_endpoint,
                                  strict_syntax_with_corners=self._strict_syntax_with_corners,
                                  target_classes=self._target_classes,
                                  file_target_classes=self._file_target_classes,
                                  built_remote_graph=self._built_remote_graph,
                                  built_shape_map=self._built_shape_map,
                                  remove_empty_shapes=self._remove_empty_shapes,
                                  limit_remote_instances=self._limit_remote_instances,
                                  inverse_paths=self._inverse_paths,
                                  all_classes_mode=self._all_classes_mode,
                                  compression_mode=self._compression_mode,
                                  disable_endpoint_cache=self._disable_endpoint_cache,
                                  detect_minimal_iri=self._detect_minimal_iri,
                                  examples_mode=self._examples_mode,
                                  federated_sources=self._federated_sources) # TODO IMPL.


    def _build_instance_tracker(self):
        return get_instance_tracker(instances_file_input=self._instances_file_input,
                                    graph_file_input=self._graph_file_input,
                                    graph_list_of_files_input=self._graph_list_of_files_input,
                                    target_classes=self._target_classes,
                                    file_target_classes=self._file_target_classes,
                                    input_format=self._input_format,
                                    instantiation_property=self._instantiation_property,
                                    infer_numeric_types_for_untyped_literals=self._infer_numeric_types_for_untyped_literals,
                                    raw_graph=self._raw_graph,
                                    all_classes_mode=self._all_classes_mode,
                                    namespaces_dict=self._namespaces_dict,
                                    url_input=self._url_graph_input,
                                    list_of_url_input=self._list_of_url_input,
                                    rdflib_graph=self._rdflib_graph,
                                    shape_map_file=self._shape_map_file,
                                    shape_map_raw=self._shape_map_raw,
                                    track_classes_for_entities_at_last_depth_level=self._track_classes_for_entities_at_last_depth_level,
                                    depth_for_building_subgraph=self._depth_for_building_subgraph,
                                    url_endpoint=self._url_endpoint,
                                    strict_syntax_with_corners=self._strict_syntax_with_corners,
                                    shape_map_format=self._shape_map_format,
                                    namespaces_for_qualifier_props=self._namespaces_for_qualifier_props,
                                    shape_qualifiers_mode=self._shape_qualifiers_mode,
                                    built_remote_graph=self._built_remote_graph,
                                    built_shape_map=self._built_shape_map,
                                    shapes_namespace=self._shapes_namespace,
                                    limit_remote_instances=self._limit_remote_instances,
                                    inverse_paths=self._inverse_paths,
                                    compression_mode=self._compression_mode,
                                    disable_endpoint_cache=self._disable_endpoint_cache,
                                    instances_cap=self._instances_cap,
                                    federates_sources=self._federated_sources)


    @staticmethod
    def _check_correct_output_params(string_output, target_file, to_uml_path):
        if not string_output and target_file is None and to_uml_path is None:
            raise ValueError("You must provide a target path , set string output to True and/or give a value to to_uml_path")

    @staticmethod
    def _check_input_format(input_format):
        if input_format not in [NT, TSV_SPO, N3, TURTLE, RDF_XML, JSON_LD, TURTLE_ITER]:
            raise ValueError("Currently unsupported input format: " + input_format)

    @staticmethod
    def _check_compression_mode(compression_mode, url_endpoint, url_graph_input, list_of_url_input):
        if compression_mode not in [ZIP, GZ, XZ, None]:
            raise ValueError("Unknownk compression mode: {}. "
                             "The currently supported compression formats are {}.".format(
                compression_mode,
                ", ".join([ZIP, GZ, XZ])))
        if compression_mode is not None and (url_endpoint is not None or url_graph_input is not None or list_of_url_input is not None):
            raise ValueError("You've chosed some compression mode ({}) to work with remote sources."
                             "Currently, sheXer can only parse compressed local files".format(compression_mode))


    @staticmethod
    def _check_target_classes(target_classes, file_target_classes, all_classes_mode, shape_map_file, shape_map_raw):
        if not all_classes_mode:
            check_just_one_not_none((target_classes, "target_classes"),
                                    (file_target_classes, "file_target_classes"),
                                    (shape_map_file, "shape_map_file"),
                                    (shape_map_raw, "shape_map_raw")
                                    )
        else:
            if target_classes is not None or file_target_classes is not None:
                raise ValueError("You must provide a list of target classes XOR set all_classes_mode to True")
            # But all_classes mode is compatible with shape_map_selectors. Setting all_classes_mode = True and
            # providing some selectros will cause shexer to shex both the shapes specified in the selectors
            # and to create a shape for eahc element with an instance in the target graph

    @staticmethod
    def _check_output_format(output_format):
        if output_format not in [SHEXC, SHACL_TURTLE]:
            raise ValueError("Currently unsupported output format: " + output_format)

    @staticmethod
    def _check_or_config(or_disabled, enable_redundant):
        if or_disabled and enable_redundant:
            raise ValueError("You are indicating that you'd like to have disjunction constraints including the macro "
                             "IRI, but also that you do not want to have or constraints. Please, check your configuration"
                             "of the disable_or_statements and allow_redundant_or paremeters")

    @staticmethod
    def _check_aceptance_threshold(aceptance_threshold):
        if aceptance_threshold < 0 or aceptance_threshold > 1:
            raise ValueError("The acceptance threshold must be a value in [0,1]")

    @staticmethod
    def _check_examples_mode(examples_mode):
        if examples_mode not in [None, ALL_EXAMPLES, CONSTRAINT_EXAMPLES, SHAPE_EXAMPLES]:
            raise ValueError("The examples mode param should be set to None or using one of the values in shexer.const, section \"EXAMPLES\" ")
