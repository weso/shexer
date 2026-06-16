import unittest
from shexer.shaper import Shaper
from test.const import G1, BASE_FILES, default_namespaces, G1_ALL_CLASSES_NO_COMMENTS
from test.t_utils import file_vs_str_tunned_comparison
import os.path as pth

from shexer.consts import TURTLE_ITER, GZ, ZIP, XZ, N3, TURTLE, RDF_XML, TSV_SPO, NT, JSON_LD



_BASE_DIR = BASE_FILES + "compression" + pth.sep


class TestCompressionMode(unittest.TestCase):

    ######################### GZ

    def test_ttl_iter_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_n3_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.n3.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=N3,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_json_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.json.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=JSON_LD,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_ttl_rdflib_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_xml_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.xml.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=RDF_XML,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_tsv_spo_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.tsv.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TSV_SPO,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_nt_gz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.nt.gz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True,
            compression_mode=GZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    ############# zip

    def test_ttl_iter_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_n3_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.n3.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=N3,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_ttl_rdflib_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_xml_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.xml.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=RDF_XML,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_tsv_spo_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.tsv.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TSV_SPO,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_nt_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.nt.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_json_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.json.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=JSON_LD,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))


    ########################  xz

    def test_ttl_iter_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE_ITER,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_n3_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.n3.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=N3,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_json_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.json.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=JSON_LD,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_ttl_rdflib_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.ttl.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TURTLE,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_xml_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.xml.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=RDF_XML,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_tsv_spo_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.tsv.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=TSV_SPO,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    def test_nt_xz(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t_graph_1.nt.xz",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True,
            compression_mode=XZ
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    ########################  Wrong params

    def test_unknown_mode(self):
        try:
            shaper = Shaper(
                graph_file_input=_BASE_DIR + "t_graph_1.json.zip",
                namespaces_dict=default_namespaces(),
                all_classes_mode=True,
                input_format=JSON_LD,
                disable_comments=True,
                compression_mode="RAR"
            )
            self.fail("It shouldn`t allow to use an unknown compression format")
        except ValueError:
            pass  # thats ok
        except:
            self.fail("The exception should be a ValueError")

    def test_remote_source(self):
        shape_map_raw = "SPARQL'select ?p where " \
                        "{ ?p <http://www.wikidata.org/prop/direct/P31> <http://www.wikidata.org/entity/Q14660> } " \
                        "LIMIT 1'@<Flag>"
        try:
            shaper = Shaper(shape_map_raw=shape_map_raw,
                            url_endpoint="https://qlever.dev/api/wikidata",
                            namespaces_dict=default_namespaces(),
                            instantiation_property="http://www.wikidata.org/prop/direct/P31",
                            disable_comments=True,
                            depth_for_building_subgraph=1,
                            track_classes_for_entities_at_last_depth_level=False,
                            all_classes_mode=False,
                            compression_mode=ZIP)
            self.fail("It should allow to use compression with a remote source")
        except ValueError:
            pass
        except:
            self.fail("The exception should be a ValueError")


    ##################### SEVERAL FILES IN ZIP

    def test_nt_zip(self):
        shaper = Shaper(
            graph_file_input=_BASE_DIR + "t1_graph_partials_1_2_3__3.nt.zip",
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))

    ##################### SEVERAL ZIPS

    def test_nt_zip(self):
        shaper = Shaper(
            graph_list_of_files_input=[_BASE_DIR + "t1_graph_partials_1_2__3.nt.zip",
                                       _BASE_DIR + "t1_graph_partials_3__3.nt.zip"],
            namespaces_dict=default_namespaces(),
            all_classes_mode=True,
            input_format=NT,
            disable_comments=True,
            compression_mode=ZIP
        )
        str_result = shaper.shex_graph(string_output=True)
        self.assertTrue(file_vs_str_tunned_comparison(file_path=G1_ALL_CLASSES_NO_COMMENTS,
                                                      str_target=str_result))
