from shexer.model.annotation import Annotation

POSITIVE_CLOSURE = "+"
KLEENE_CLOSURE = "*"
OPT_CARDINALITY = "?"



class Statement(object):

    def __init__(self, st_property, st_type, cardinality, n_occurences,
                 probability, comments=None, serializer_object=None,
                 is_inverse=False, annotations=None):
        self._st_property = st_property
        self._st_type = st_type
        self._cardinality = cardinality
        self._n_occurences = n_occurences
        self._probability = probability
        self._serializer_object = serializer_object
        self._comments = [] if comments is None else comments
        self._is_inverse = is_inverse
        self._annotations = [] if annotations is None else annotations

    def get_tuples_to_serialize_line_indent_level(self, is_last_statement_of_shape, namespaces_dict):
        return self._serializer_object.\
            serialize_statement_with_indent_level(a_statement=self,
                                                  is_last_statement_of_shape= is_last_statement_of_shape)

    def probability_representation(self):
        return self._serializer_object.probability_representation(self)

    def cardinality_representation(self):
        return self._serializer_object.cardinality_representation(self)

    def comment_representation(self, namespaces_dict):
        return self._serializer_object.turn_statement_into_comment(self, namespaces_dict=namespaces_dict)

    def add_comment(self, comment, insert_first=False):
        if not insert_first:
            self._comments.append(comment)
        else:
            self._comments.insert(0, comment)

    def remove_comments(self):
        self._comments = []

    def add_annotation(self, predicate, obj, insert_first=False):
        annon = Annotation(predicate=predicate,
                           obj=obj)
        if not insert_first:
            self._annotations.append(annon)
        else:
            self._annotations.insert(0, annon)


    @property
    def st_property(self):
        return self._st_property

    @property
    def st_type(self):
        return self._st_type

    @property
    def cardinality(self):
        return self._cardinality

    @cardinality.setter
    def cardinality(self, value):
        self._cardinality = value

    @property
    def probability(self):
        return self._probability

    @property
    def n_occurences(self):
        return self._n_occurences

    @probability.setter
    def probability(self, value):
        self._probability = value

    @property
    def comments(self):
        return self._comments

    @property
    def annotations(self):
        return self._annotations

    @property
    def serializer_object(self):
        return self._serializer_object

    @serializer_object.setter
    def serializer_object(self, value):
        self._serializer_object = value

    @property
    def is_inverse(self):
        return self._is_inverse

    @is_inverse.setter
    def is_inverse(self, value):
        self._is_inverse = value
