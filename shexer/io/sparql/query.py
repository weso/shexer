from SPARQLWrapper import SPARQLWrapper, JSON
from urllib.error import HTTPError
from time import sleep
import random
from importlib.metadata import version

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from SPARQLWrapper.SPARQLExceptions import EndPointInternalError

_FAKE_USER_AGENT = "sheXer/5.0 (Platform; Security; OS-or-CPU; Localization; rv:1.4) Gecko/20030624 Netscape/7.1 (ax)"
_RESULTS_KEY = "results"
_BINDINGS_KEY = "bindings"
_VALUE_KEY = "value"
_TYPE_KEY = "type"
_URI_TYPE = "uri"

_XML_LANG_FIELD = "xml:lang"


def _add_lang_if_needed(result_dict):
    result = result_dict[_VALUE_KEY]
    if _XML_LANG_FIELD in result_dict:
        result += '"' + result + '"@' + result_dict[_XML_LANG_FIELD]
    return result


def _add_corners_if_needed(target_elem, elem_type):
    if elem_type == _URI_TYPE and not target_elem.startswith("<"):
        return "<" + target_elem + ">"
    return target_elem


def query_endpoint_single_variable(endpoint_url, str_query, variable_id, max_retries=10):
    """
    It receives an SPARQL query with a single variable and returns a list with the resulting nodes

    :param endpoint_url:
    :param str_query:
    :param variable_id:
    :return:
    """
    result_query = _query_endpoint_json_result(endpoint_url=endpoint_url,
                                               str_query=str_query,
                                               max_retries=max_retries)
    result = []
    for row in result_query[_RESULTS_KEY][_BINDINGS_KEY]:
        an_elem = row[variable_id][_VALUE_KEY]
        result.append(an_elem)
    return result


def query_endpoint_sp_of_an_o(endpoint_url, str_query, s_id, p_id, max_retries=5):
    result_query = _query_endpoint_json_result(endpoint_url=endpoint_url,
                                               str_query=str_query,
                                               max_retries=max_retries)
    result = []
    for row in result_query[_RESULTS_KEY][_BINDINGS_KEY]:
        p_value = _add_corners_if_needed(target_elem=row[p_id][_VALUE_KEY],
                                         elem_type=row[p_id][_TYPE_KEY])
        s_value = _add_corners_if_needed(target_elem=_add_lang_if_needed(row[s_id]),
                                         elem_type=row[s_id][_TYPE_KEY])
        result.append((s_value, p_value))
    return result


def query_endpoint_po_of_an_s(endpoint_url, str_query, p_id, o_id, max_retries=5):

    result_query = _query_endpoint_json_result(endpoint_url=endpoint_url,
                                               str_query=str_query,
                                               max_retries=max_retries)
    result = []
    for row in result_query[_RESULTS_KEY][_BINDINGS_KEY]:
        if p_id in row and o_id in row:
            p_value = _add_corners_if_needed(target_elem=row[p_id][_VALUE_KEY],
                                             elem_type=row[p_id][_TYPE_KEY])
            o_value = _add_corners_if_needed(target_elem=_add_lang_if_needed(row[o_id]),
                                             elem_type=row[o_id][_TYPE_KEY])
            result.append((p_value, o_value))
    return result



class SparqlQueryError(Exception):
    """Error genérico al ejecutar una consulta SPARQL."""


class SparqlRateLimitError(SparqlQueryError):
    """El endpoint ha respondido con HTTP 429."""


class SparqlMaxRetriesExceeded(SparqlQueryError):
    """Se ha alcanzado el número máximo de reintentos."""


def _compute_backoff_delay(attempt, base_delay, max_delay=60.0):
    """
    Exponential backoff with jitter.

    attempt: 0, 1, 2, ...
    """
    delay = min(base_delay * (2 ** attempt), max_delay)

    # random jitter
    return delay * (0.5 + random.random() * 0.5)


def _build_sparql_client(endpoint_url, query, user_agent):
    sparql = SPARQLWrapper(endpoint_url)
    sparql.agent = user_agent
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    return sparql

def _build_user_agent():
    return (
        f"sheXer/{version('shexer')} "
        "(https://github.com/DaniFdezAlvarez/shexer)"
    )

def _query_endpoint_json_result(endpoint_url: str, str_query: str, max_retries= 5, base_delay: float = 1.0):

    sparql = _build_sparql_client(
        endpoint_url=endpoint_url,
        query=str_query,
        user_agent=_build_user_agent(),
    )

    last_error = None

    for attempt in range(max_retries + 1):
        try:
            return sparql.query().convert()
        except HTTPError as e:
            last_error = e
            # Wikimedia recomienda respetar explícitamente el rate limit
            if e.code == 429:
                raise SparqlRateLimitError(
                    "The endpoint returned HTTP 429 (Too Many Requests)."
                ) from e
            if attempt == max_retries:
                break
            sleep(_compute_backoff_delay(attempt, base_delay))
        except EndPointInternalError as e:
            last_error = e
            if attempt == max_retries:
                break
            sleep(_compute_backoff_delay(attempt, base_delay))

    raise SparqlMaxRetriesExceeded(
        f"Maximum number of retries exceeded ({max_retries}). "
        f"Last error: {last_error}"
    ) from last_error


# def _query_endpoint_json_result(endpoint_url, str_query, max_retries=5, sleep_time=2, fake_user_agent=True):
#     first_failure = True
#     sparql = SPARQLWrapper(endpoint_url)
#     if fake_user_agent:
#         sparql.agent = _FAKE_USER_AGENT
#     sparql.setQuery(str_query)
#     sparql.setReturnFormat(JSON)
#     last_error = None
#     while max_retries > 0:
#         try:
#             return sparql.query().convert()
#         except (HTTPError, EndPointInternalError) as e:
#             max_retries -= 1
#             sleep(sleep_time)
#             last_error = e
#             if first_failure and not fake_user_agent:
#                 sparql.agent = _FAKE_USER_AGENT
#                 first_failure = not first_failure
#     last_error.msg = "Max number of attempt reached, it is not possible to perform the query. Msg:\n" + last_error.msg