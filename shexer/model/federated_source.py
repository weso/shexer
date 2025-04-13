class FederatedSource(object):
    def __init__(self, endpoint_url, property_link, link_in_federated_source, alias, origin_position_in_triple=0):
        """
        :param endpoint_url: (str) URL where the content is exposed online to be queried.
        :param property_link: (str) URI of the property used to link elements in different sources (owl:sameAs, schema:sameAs, rdfs:seeAlso...)
        :param link_in_federated_source: (bool) it indicates if the link between two entities is expected to be found in the origin source (False)
                                         or in the federated source itself (True)
        :param alias: (str) this string will be used to give proper names to extracted shapes.
        :param origin_position_in_triple: (int) it indicates where is the original node expected to be found in the linked triples. 0 means subject, 1 means object
        """
        self._endpoint_url = endpoint_url
        self._property_link = property_link
        self._link_in_federated_source = link_in_federated_source
        self._alias = alias
        self._origin_position_in_triple = origin_position_in_triple
        self._set_of_instances = None  # It will be filled whn tracking instances


    @property
    def endpoint_url(self):
        return self._endpoint_url

    @property
    def origin_position_in_triple(self):
        return self._origin_position_in_triple

    @property
    def property_link(self):
        return self._property_link

    @property
    def link_in_federated_source(self):
        return self._link_in_federated_source

    @property
    def alias(self):
        return self._alias

    @property
    def set_of_instances(self):
        return self._instances_dict

    @set_of_instances.setter
    def set_of_instances(self, a_dict):
        self._instances_dict = a_dict

