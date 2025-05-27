from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.utils.uri import remove_corners, unprefixize_uri_mandatory
from shexer.utils.literal import find_next_unescaped_quotes
from shexer.utils.triple_yielders import tune_subj, tune_prop, tune_token
import re

_OTHER_BLANKS = re.compile("[\r\n\t]")
_SEVERAL_BLANKS = re.compile("  +")
_QUOTES_FOR_LITERALS = re.compile('[^\\\]"')
_INIT_INLINE_COMMENT = re.compile(" #")
_RDF_TYPE_CONTRACTED = ["a", "rdf:type"]
_RDF_TYPE_URI = "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>"
_BOOLEANS = ["true", "false"]
_INI_BASE_URIS = ["/", "#"]
_CLOSURES = [",", ";", "."]
_SPECIAL_CHARS_AFTER_QUOTES = ["^","@"]
_S = 0
_P = 1
_O = 2

_WAITING_FOR_SUBJ = 0
_WAITING_FOR_PRED = 1
_WAITING_FOR_OBJ = 2
_NOT_WAITING = 4

"""
TTL parser that yield triples (model objects) without loading the whole graph content in 
main memory.

WARNING: This parser works with some frequent structural assumptions of turtle files that
are not part of the standard. You may get unexpected errors or unexpected results dealing
with files containing lines which represent more than one triple. Also, we assume a totally
wel--formated input. Bad-formatted may remain undetected and produce wrong triples.

Please, in case you do not need to parse huge files that do not fit in the main memory
of your computer, use RdflifTriplesYielder instead
"""


class BigTtlTriplesYielder(BaseTriplesYielder):

    def __init__(self, source_file=None, allow_untyped_numbers=True, raw_graph=None,
                 compression_mode=None, zip_base_archive=None):

        super(BigTtlTriplesYielder, self).__init__()
        self._source_file = source_file
        self._raw_graph = raw_graph
        self._triples_count = 0
        self._error_triples = 0
        self._allow_untyped_numbers = allow_untyped_numbers
        self._compression_mode = compression_mode
        self._line_reader = self._decide_line_reader(source_file=source_file,
                                                     raw_graph=raw_graph,
                                                     compression_mode=compression_mode,
                                                     zip_base_archive=zip_base_archive)
        # Support
        self._prefixes = {}
        self._base = None

        # To be used while parsing
        self._state = _WAITING_FOR_SUBJ
        self._tmp_s = None
        self._tmp_p = None
        self._tmp_o = None
        self._last_triple_jump = None

        self._triple_ready = False

    def yield_triples(self):
        self._reset_parsing()
        for a_line in self._read_normalized_lines():
            for a_triple in self._process_line(a_line):
                self._triples_count += 1
                yield (
                    tune_subj(a_triple[_S],
                              raise_error_if_no_corners=False),
                    tune_prop(a_triple[_P],
                              raise_error_if_no_corners=False),
                    tune_token(a_triple[_O],
                               base_namespace=self._base,
                               allow_untyped_numbers=self._allow_untyped_numbers,
                               raise_error_if_no_corners=False)
                )

    def _clean_line(self, str_line):
        result = _OTHER_BLANKS.sub(" ", str_line)
        result = _SEVERAL_BLANKS.sub(" ", result)
        result = result.strip()
        return result if " #" not in result else self._remove_comments_if_needed(result)

    def _remove_comments_if_needed(self, str_line):
        """Remove comments in the middle of the line.
        Lines starting with # won't be erased
        """
        if '"' not in str_line:  # Comment mark and no literals, trivial case
            return str_line[:str_line.find(" #")]
        # We need to find the begining and end of the literal to avoid erasing
        # comments within literals (actual content)
        quotes_indexes = []
        count_down_quotes = 2
        for a_match in _QUOTES_FOR_LITERALS.finditer(str_line):
            quotes_indexes.append(a_match.start(0))
            count_down_quotes -= 1
            if count_down_quotes == 0:
                break
        for a_match in _INIT_INLINE_COMMENT.finditer(str_line):
            if a_match.start(0) < quotes_indexes[0] or a_match.start(0) > quotes_indexes[1]:
                return str_line[:a_match.start(0)]
        return str_line  # If this point is reached, it means that the potential comments
                         # are actual content of a string literal

    def _process_line(self, str_line):
        str_line = self._clean_line(str_line)
        if str_line == "":
            self._process_empty_line(str_line)
        elif str_line.startswith("@prefix"):
            self._process_prefix_line(str_line)
        elif str_line.startswith("@base"):
            self._process_base_line(str_line)
        elif str_line.startswith("#"):
            self._process_comment_line(str_line)
        else:
            for a_triple in self._process_line_with_potential_triples(str_line):
                yield a_triple

    def _process_line_with_potential_triples(self, a_line):
        next_token, next_index = self._next_line_token(a_line, 0)
        while next_token != None:
            if next_token == ",":
                yield self._current_triple()
                self._state = _WAITING_FOR_OBJ
            elif next_token == ";":
                yield self._current_triple()
                self._state = _WAITING_FOR_PRED
            elif next_token == ".":
                yield self._current_triple()
                self._state = _WAITING_FOR_SUBJ
            else:
                self._assing_tmp_element_and_promote_state(next_token)
            next_token, next_index = self._next_line_token(a_line, next_index)

    def _current_triple(self):
        return self._tmp_s, self._tmp_p, self._tmp_o

    def _assing_tmp_element_and_promote_state(self, token):
        if self._state == _WAITING_FOR_SUBJ:
            self._tmp_s = self._parse_elem(token)
            self._state = _WAITING_FOR_PRED
        elif self._state == _WAITING_FOR_PRED:
            self._tmp_p = self._parse_elem(token)
            self._state = _WAITING_FOR_OBJ
        elif self._state == _WAITING_FOR_OBJ:
            self._tmp_o = self._parse_elem(token)
            if self._tmp_o.startswith('"'):
                self._tmp_o = self._tmp_o.replace('\\\\"','\\"')
            self._state = _NOT_WAITING
        else:
            raise ValueError("Malformed file. Processing an unexpected token: " + token)


    def _next_line_token(self, a_line, start_index):
        while(start_index < len(a_line) and a_line[start_index] == " "):
            start_index += 1
        if start_index >= len(a_line):
            return None, None
        if a_line[start_index] in _CLOSURES:
            return a_line[start_index], start_index + 1
        elif a_line[start_index] == "<":
            end_index = a_line.find(">", start_index)
            return self._parse_cornered_element(cornered_element=a_line[start_index:end_index+1]), end_index + 1
        elif a_line[start_index] == '"':
            end_index = self._find_next_quoted_literal_ending(a_line, start_index)
            return a_line[start_index:end_index+1], end_index + 1
        else:  # could be a prefixed element, a bnode, a non-string literal... find the next blank anyway
            end_index = self._find_next_blank(a_line, start_index)
            return a_line[start_index:end_index], end_index + 1


    def _find_next_blank(self, target_str, start_index):
        pos = target_str.find(" ", start_index)
        return len(target_str)-1 if pos == -1 else pos

    def _find_next_quoted_literal_ending(self, target_str, start_index):
        next_quotes = find_next_unescaped_quotes(target_str=target_str,
                                                 start_index=start_index+1)
        if next_quotes +1 > len(target_str) or target_str[next_quotes + 1] == " ":
            return next_quotes
        elif target_str[next_quotes + 1] in _SPECIAL_CHARS_AFTER_QUOTES:
            return self._find_next_blank(target_str, next_quotes) - 1
        else:
            raise ValueError("Malformed literal? It seems like there is a problem of unmatching quotes: " + target_str)

    def _process_prefix_line(self, line):
        pieces = line.split(" ")
        prefix = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        base_url = remove_corners(pieces[2])
        self._prefixes[prefix] = base_url

    def _process_base_line(self, line):
        pieces = line.split(" ")
        # base_url = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        # base_url = remove_corners(pieces[2])
        self._base = remove_corners(pieces[1])

    def _process_comment_line(self, line):
        pass  # At this point, just ignore it.

    def _process_empty_line(self, line):
        pass  # At this point, just ignore it.

    def _process_unknown_line(self, line):
        self._error_triples += 1


    def _process_multi_triple_line_commas(self, line):
        pieces = line.split(" ")
        index_first_comma = 0
        for i in range(0, len(pieces)):
            if pieces[i] == ",":
                index_first_comma = i
                break
        if index_first_comma == 3:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])
        elif index_first_comma == 2:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif index_first_comma == 1:
            self._tmp_o = self._parse_elem(pieces[0])
        # else impossible?
        self._decide_current_triple()

        for i in range(index_first_comma + 2, len(pieces), 2):
            self._tmp_o = self._parse_elem(pieces[i - 1])
            self._decide_current_triple()

    def _process_single_triple_line(self, line):
        pieces = line.split(" ")
        if len(pieces) == 4:
            self._tmp_s = self._parse_elem(pieces[0])
            self._tmp_p = self._parse_elem(pieces[1])
            self._tmp_o = self._parse_elem(pieces[2])

        elif len(pieces) == 3:
            self._tmp_p = self._parse_elem(pieces[0])
            self._tmp_o = self._parse_elem(pieces[1])
        elif len(pieces) == 2:
            self._tmp_o = self._parse_elem(pieces[0])
        self._decide_current_triple()

    def _process_isolated_subject(self, line):
        # No split. Line is expected to contain a line with no blanks (isolated subject)
        self._tmp_s = self._parse_elem(line)
        # No need to decide triple now, incomplete element

    def _decide_current_triple(self):
        # if self._is_bnode(self._tmp_s):
        #     self._ignored_triples += 1
        # elif self._is_bnode(self._tmp_o):
        #     self._ignored_triples += 1
        # elif self._is_num_literal(self._tmp_o):
        #     self._ignored_triples += 1
        # elif self._is_boolean(self._tmp_o):
        #     self._ignored_triples += 1
        # else:
        self._triple_ready = True

    def _is_boolean(self, raw_element):
        return True if raw_element in _BOOLEANS else False

    def _is_bnode(self, a_elem):
        if a_elem[0] == "_":
            return True
        return False

    def _is_num_literal(self, elem):
        try:
            float(elem)
            return True
        except ValueError:
            return False

    def _parse_elem(self, raw_elem):
        if raw_elem[0] == "<":
            return self._parse_cornered_element(raw_elem)
        elif raw_elem in _RDF_TYPE_CONTRACTED:
            return _RDF_TYPE_URI
        elif raw_elem.startswith('"'):  # it's a literal, will be better parsed later
            return raw_elem
        elif ":" in raw_elem:
            if raw_elem.startswith("_:"):
                return raw_elem
            return unprefixize_uri_mandatory(target_uri=raw_elem,
                                             prefix_namespaces_dict=self._prefixes)
        elif raw_elem in _BOOLEANS or self._is_num_literal(raw_elem):
            return raw_elem
            # else?? shouldn't happen, let it break with a nullpoitner

    def _parse_cornered_element(self, cornered_element):
        if self._base is None:
            return cornered_element  # There is no base
        elif cornered_element[1] in _INI_BASE_URIS:
            return "<" + self._base + cornered_element[2:-1] + ">"
        elif not cornered_element[1:].startswith("http"):
            return "<" + self._base + cornered_element[1:-1] + ">"
        else:
            return cornered_element  # Nothing to do with base

    @property
    def yielded_triples(self):
        return self._triples_count

    @property
    def error_triples(self):
        return self._error_triples

    @property
    def ignored_triples(self):
        return self._ignored_triples

    def _reset_parsing(self):
        self._error_triples = 0
        self._triples_count = 0
        self._ignored_triples = 0
        self._state = _WAITING_FOR_SUBJ

    def _read_normalized_lines(self):
        waiting = False
        tmp = ''
        for a_line in self._line_reader.read_lines():
            if not waiting and '"""' not in a_line:
                yield a_line
            elif waiting and '"""' not in a_line:
                tmp += "\\n" + self._scape_quotes_in_normalized_line(a_line)
            elif not waiting and '"""' in a_line:
                waiting = True
                tmp = self._scape_quotes_in_normalized_line(a_line).replace('"""', '"', 1)
            elif waiting and '"""' in a_line:
                waiting = False
                yield tmp + "\\n" + self._scape_quotes_in_normalized_line(a_line).replace('"""', '"', 1)
                tmp = ''

    def _scape_quotes_in_normalized_line(self, target):
        triple_quotes = []
        normal_quotes = []

        a_char_index = 0
        while a_char_index < len(target):
            if target[a_char_index] == '"':
                if a_char_index + 2 < len(target) and target[a_char_index+1:a_char_index+3] == '""':
                    triple_quotes.append(a_char_index)
                    a_char_index += 2
                else:
                    normal_quotes.append(a_char_index)
            a_char_index += 1
        if len(triple_quotes) > 1:
            raise StringMultilineSingleLineError(target)
        if len(normal_quotes) == 0:
            return target
        normal_quotes = [0] + normal_quotes + [len(target)]

        parts = []
        target_index_in_quotes_list = 0
        while target_index_in_quotes_list < len(normal_quotes) -1:
            parts.append(target[normal_quotes[target_index_in_quotes_list]:normal_quotes[target_index_in_quotes_list+1]])
            target_index_in_quotes_list += 1
        return "\\".join(parts)



class StringMultilineSingleLineError(TypeError):

    def __init__(self, line):
        super().__init__(f"It looks like there is a multiline string with several triple quotes in the same line. "
                         "This may be valid turtle syntax though. If that's your case and you get this error, please, "
                         f"share your input and code in an issue te sheXer's repository. Conflictive line: '{line}'")


