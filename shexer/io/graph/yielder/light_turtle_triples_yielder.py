from shexer.io.graph.yielder.base_triples_yielder import BaseTriplesYielder
from shexer.io.graph.yielder.multifile_base_triples_yielder import MultifileBaseTripleYielder
from shexer.utils.triple_yielders import tune_subj, tune_prop, tune_token
from shexer.utils.uri import remove_corners

import lightrdf


class LightTurtleTriplesYielder(BaseTriplesYielder):

    def __init__(self, source_file):
        super().__init__()
        self._prefixes = {}
        self._source_file = source_file

    def yield_triples(self):
        parser = lightrdf.Parser()
        for s, p, o in parser.parse(self._source_file, base_iri=None):
            yield (
                tune_subj(s),
                tune_prop(p),
                tune_token(o)
            )

    def extract_prefixes(self, ttl_path):
        prefixes = {}
        with open(ttl_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("@prefix"):
                    self._process_prefix_line(line)

    def _process_prefix_line(self, line):
        pieces = line.split(" ")
        prefix = pieces[1] if not pieces[1].endswith(":") else pieces[1][: - 1]
        base_url = remove_corners(pieces[2])
        self._prefixes[prefix] = base_url

class MultiLightTurtleTriplesYielder(MultifileBaseTripleYielder):
    def __init__(self, list_of_files):
        super(MultiLightTurtleTriplesYielder, self).__init__(
            list_of_files=list_of_files,
            namespaces_to_ignore=None,
            allow_untyped_numbers=False,
            compression_mode=None,
            zip_base_archive=None)

    def _constructor_file_yielder(self, a_source_file, parse_namespaces=False):
        return LightTurtleTriplesYielder(source_file=a_source_file)
