from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.io.graph.yielder.multifile_base_triples_yielder import MultifileBaseTripleYielder
from shexer.utils.triple_yielders import tune_subj, tune_prop, tune_token
from shexer.utils.uri import remove_corners
import tempfile
from pathlib import Path
import re
from shexer.utils.exception import ParseError

WHITESPACES= re.compile(r"\s+")

import lightrdf


class LightTurtleTriplesYielder(BaseTriplesYielder):

    def __init__(self, source_file, raw_graph, namespaces_dict):
        super().__init__()
        self._prefixes = {}
        self._source_file = source_file
        self._raw_graph = raw_graph
        self._namespaces_dict = namespaces_dict if namespaces_dict is not None else {}
        self._yielded_triples = 0

    def _yield_triples(self):
        self._extract_prefixes()
        parser = lightrdf.turtle.Parser()
        try:
            for s, p, o in parser.parse(self._source_file, base_iri=None):
                yield (
                    tune_subj(s),
                    tune_prop(p),
                    tune_token(o)
                )
                self._yielded_triples += 1
        except BaseException as e:
            raise ParseError(f"Error while parsing: {e}") from e

    def yield_triples(self):
        if self._raw_graph is not None:
            with tempfile.TemporaryDirectory() as tmpdir:
                self._source_file = Path(tmpdir) / "data.nt"
                self._source_file.write_text(self._raw_graph, encoding="utf-8")
                self._source_file = str(self._source_file)
                for a_triple in self._yield_triples():
                    yield a_triple
        else:
            for a_triple in self._yield_triples():
                yield a_triple

    @property
    def yielded_triples(self):
        return self._yielded_triples

    @property
    def error_triples(self):  # No error triples in this parser, it crashes when finding an error
        return 0

    def _extract_prefixes(self):
        with open(self._source_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                line = WHITESPACES.sub(" ", line)
                if line.startswith("@prefix"):
                    self._process_prefix_line(line)
                else:  # if declarations are not consecutive and at the beginning, it will not work
                    break

    def _process_prefix_line(self, line):
        pieces = line.split(" ")
        prefix = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        base_url = remove_corners(pieces[2])
        if base_url not in self._namespaces_dict:
            self._namespaces_dict[base_url] = prefix

class MultiLightTurtleTriplesYielder(MultifileBaseTripleYielder):
    def __init__(self, list_of_files, namespaces_dict):
        super(MultiLightTurtleTriplesYielder, self).__init__(
            list_of_files=list_of_files,
            namespaces_to_ignore=None,
            allow_untyped_numbers=False,
            compression_mode=None,
            zip_base_archive=None)
        self._namespaces_dict = namespaces_dict

    def _constructor_file_yielder(self, a_source_file, parse_namespaces=False):
        return LightTurtleTriplesYielder(source_file=a_source_file,
                                         namespaces_dict=self._namespaces_dict,
                                         raw_graph=None)

