from shexer.core.profiling.class_profiler import RDF_TYPE_STR
from shexer.utils.file import load_whole_file_content
from shexer.utils.uri import prefixize_uri_if_possible, get_prefix_of_namespace_if_it_exists
from shexer.model.shape import STARTING_CHAR_FOR_SHAPE_NAME
import os

_MODEL_FILE_NAME = "model.yaml"
_PREFIX_FILE_NAME = "prefix.yaml"
_ENDPOINT_FILE_NAME = "endpoint.yaml"

_SHAPE_INDENT_LEVEL = 0
_PROPERTY_INDENT_LEVEL = 1
_CONSTRAINT_INDENT_LEVEL = 2


class RdfConfigSerializer(object):

    def __init__(self, target_directory, shapes_list, endpoint_url, namespaces_dict=None, string_return=False,
                 instantiation_property_str=RDF_TYPE_STR, shape_example_features=None, inverse_paths=False):
        self._target_directory = target_directory
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._shapes_list = shapes_list
        self._string_return = string_return
        self._instantiation_property_str = instantiation_property_str
        self._shape_example_features = shape_example_features
        self._inverse_paths = inverse_paths

        self._prefixes_file = self._generate_proper_path(_PREFIX_FILE_NAME)
        self._model_file = self._generate_proper_path(_MODEL_FILE_NAME)
        self._endpoint_file = self._generate_proper_path(_ENDPOINT_FILE_NAME)
        self._endpoint_url = endpoint_url

        self._subjects_dict = {}
        self._variables_used = set()
        self._shape_names_used = set()
        self._shapes_stream = None  # It will be initialized later, io_stream to write shapes

    def serialize_shapes(self):
        self._create_dir_if_necessary()
        self._serialize_prefixes()
        self._serialize_endpoint()
        self._serialize_shapes()
        return self._compose_output_files_in_str()

    def _serialize_shapes(self):
        self._shapes_stream = open(self._generate_proper_path(_MODEL_FILE_NAME), "w")
        for a_shape in self._shapes_list:
            self._serialize_shape(a_shape)
            self._shapes_stream.write("\n")
        self._shapes_stream.close()

    def _serialize_shape(self, shape):
        self._serialize_shape_header(shape)
        for a_constraint in shape.direct_statements:
            self._serialize_constraint(shape=shape,
                                       constraint=a_constraint)

    def _variable_property_name(self, st_property, st_type, shape_uri):
        candidate = self._create_var_name_for_property(st_property, shape_uri)  # TODO improve
        if candidate in self._variables_used:
            candidate += self._add_type_tag_to_var_name(st_type)
            tmp = candidate
            counter = 1
            while candidate in self._variables_used:
                candidate = tmp + str(counter)
                counter += 1
        self._variables_used.add(candidate)
        return candidate

    def _add_type_tag_to_var_name(self, st_type):
        st_type.replace("_", "")
        st_property = st_type.lower()
        candidate = ""
        for i in range(len(st_property) - 1, -1, -1):  # Locate suffix
            if st_property[i] in ["/", "#"]:
               return st_property[i + 1:]
        return candidate

    def _create_var_name_for_property(self, st_property, shape_uri):
        st_property.replace("_", "")
        st_property = st_property.lower()
        candidate = ""
        for i in range(len(st_property) - 1, -1, -1):  # Locate suffix
            if st_property[i] in ["/", "#"]:
                candidate = st_property[i + 1:]
                break
        if candidate != "":  # Try to locate prefixed namespace
            prefix = get_prefix_of_namespace_if_it_exists(target_uri=st_property,
                                                          namespaces_prefix_dict=self._namespaces_dict,
                                                          corners=False)
            if prefix is not None:
                candidate = prefix + "_" + candidate
        else: # if there is no suffix, get letters and numbers
            for char in st_property:
                if not char.isalnum():
                    candidate += char
        shape_tag = self._shape_tag_for_var_name(shape_uri)
        return f"{candidate}_of_{shape_tag}".lower()

        # return "var_name"
    def _shape_tag_for_var_name(self, class_uri):
        last_piece = class_uri
        if "#" in last_piece and last_piece[-1] != "#":
            last_piece = last_piece[last_piece.rfind("#") + 1:]
        if "/" in last_piece:
            if last_piece[-1] != "/":
                last_piece = last_piece[last_piece.rfind("/") + 1:]
            else:
                last_piece = last_piece[last_piece[:-1].rfind("/") + 1:]
        return last_piece

    def _create_subject_name_for_shape(self, shape_uri):
        shape_uri.replace("_", "")
        shape_uri.replace("-", "")
        for i in range(len(shape_uri) - 1, -1, -1):
            if not shape_uri[i].isalnum():
                return "Shape" + shape_uri[i + 1:].capitalize()
        return "SubjectName"

    def _shape_subject_name(self, shape_uri):
        if shape_uri not in self._subjects_dict:
            origin = self._create_subject_name_for_shape(shape_uri)
            candidate = origin
            counter = 1
            while candidate in self._shape_names_used:
                counter += 1
                candidate = origin + str(counter)
            self._shape_names_used.add(candidate)
            self._subjects_dict[shape_uri] = candidate
        return self._subjects_dict[shape_uri]

    def _write_shape_line(self, content, indentation):
        indentation_str = ' ' * 2 * indentation
        self._shapes_stream.write(f"{indentation_str}- {content}\n")

    def _serialize_shape_header(self, shape):
        shape_example = self._shape_example_features.shape_example(shape_id=shape.class_uri)
        if not shape_example:
            shape_example = ""
        elif shape_example.startswith("http://") or shape_example.startswith("https://"):
            shape_example = f"<{shape_example}>"
            shape_example = prefixize_uri_if_possible(target_uri=shape_example,
                                                      namespaces_prefix_dict=self._namespaces_dict,
                                                      corners=True)
        self._write_shape_line(content=f"{self._shape_subject_name(shape.name[2:-1])} {shape_example}:",
                               indentation=_SHAPE_INDENT_LEVEL)

    def _serialize_constraint(self, shape, constraint):
        st_property = self._nice_uri(constraint.st_property)
        if constraint.st_property == self._instantiation_property_str:
            st_type = self._nice_uri(constraint.st_type)
            self._write_shape_line(indentation=_PROPERTY_INDENT_LEVEL,
                                   content=f"{st_property}: {st_type}")
        else:
            if self._inverse_paths:
                example_cons = self._shape_example_features.get_constraint_example(shape_id=shape.class_uri,
                                                                                   prop=constraint.st_property,
                                                                                   inverse=False)
            else:
                example_cons = self._shape_example_features.get_constraint_example(shape_id=shape.class_uri,
                                                                                   prop=constraint.st_property)
            if constraint.st_type.startswith(STARTING_CHAR_FOR_SHAPE_NAME):
                example_cons = self._shape_subject_name(constraint.st_type[2:-1])
            elif example_cons is None:
                example_cons = ""
            elif example_cons.startswith("http://") or example_cons.startswith("https://"):
                example_cons = self._nice_uri(example_cons)
            elif not example_cons.isnumeric():
                if example_cons.startswith('"') and "@" in example_cons:  # This must be a lang string
                    example_cons = example_cons[:example_cons.find("@")]
                elif not example_cons.startswith('"'):
                    example_cons = f'"{example_cons}"'
            if len(example_cons) >= 2:
                # example_cons =  example_cons[0] +  example_cons[1:-1].replace('"', '\\"') + example_cons[-1]
                example_cons = example_cons[0] + example_cons[1:-1] + example_cons[-1]
            self._write_shape_line(indentation=_PROPERTY_INDENT_LEVEL,
                                   content=f"{st_property}:")
            self._write_shape_line(indentation=_CONSTRAINT_INDENT_LEVEL,
                                   content="{}: {}".format(self._variable_property_name(
                                       st_property=constraint.st_property,
                                       st_type=constraint.st_type,
                                       shape_uri=shape.class_uri),
                                                           example_cons))



    def _serialize_prefixes(self):
        with open(self._prefixes_file, "w") as out_stream:
            for a_namespace, a_prefix in self._namespaces_dict.items():
                out_stream.write(f"{a_prefix}: <{a_namespace}>\n")

    def _serialize_endpoint(self):
        if self._endpoint_url is not None:
            with open(self._endpoint_file, "w") as out_stream:
                out_stream.write(f"endpoint:\n  - {self._endpoint_url}")

    def _generate_proper_path(self, file_name):
        return self._target_directory + (
            "" if self._target_directory.endswith(os.path.sep) else os.path.sep) + file_name

    def _compose_output_files_in_str(self):
        return f"{self._header(_ENDPOINT_FILE_NAME)}\n" \
               f"{load_whole_file_content(self._endpoint_file) if self._endpoint_url is not None else 'Endpoint not provided'}\n" \
               f"{self._header(_PREFIX_FILE_NAME)}\n" \
               f"{load_whole_file_content(self._prefixes_file)}\n" \
               f"{self._header(_MODEL_FILE_NAME)}\n" \
               f"{load_whole_file_content(self._model_file)}"

    def _header(self, file_name):
        return f"##################  {file_name}  ##################"

    def _create_dir_if_necessary(self):
        if not os.path.exists(self._target_directory):
            os.makedirs(self._target_directory)

    def _nice_uri(self, target_uri):
        result = f"<{target_uri}>"
        return prefixize_uri_if_possible(target_uri=result,
                                         namespaces_prefix_dict=self._namespaces_dict,
                                         corners=True)
