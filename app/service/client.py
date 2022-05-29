from elasticsearch import Elasticsearch, AuthenticationException
from pydantic import AnyHttpUrl
from app.domain.exceptions import ElasticClientException
import re
from app.domain.index import Index
from typing import Dict


class ElasticClient:

    def __init__(self, host: AnyHttpUrl):
        self._client = Elasticsearch(hosts=host)

    def mappings_for_codename(self, codename: str, prev: bool = False) -> Dict[str, Index]:
        """
        :param codename: codename of the version
        :param prev: look for indices with .prev suffix
        Returns all found indices for the version with given codename.
        """
        index_name_template = f"{codename}-tracardi-*" if codename else "tracardi-*"
        if prev is True:
            index_name_template += ".prev"

        try:
            indices_names = self._client.indices.get(index=index_name_template)
            if prev is False:
                indices_names = [index_name for index_name in indices_names if not index_name.endswith(".prev")]

            result = {}
            for index_name in indices_names:
                result.update(**self._client.indices.get_mapping(index=index_name).body)

            if codename:
                result = {key.split(codename)[1][1:]: result[key] for key in result}

            result = {
                re.split(r"-[0-9]{4}-[0-9]{1,2}", key)[0]: Index(
                    name=re.split(r"-[0-9]{4}-[0-9]{1,2}", key)[0],
                    multi=bool(re.findall(r"-[0-9]{4}-[0-9]{1,2}", key)),
                    mapping=Index.standardize_mapping(result[key]["mappings"]["properties"])
                ) for key in result
            }

            return result

        except AuthenticationException as e:
            print("Invalid Elasticsearch authentication credentials provided.")
            raise ElasticClientException(str(e))

    def close(self):
        self._client.close()
