from app.domain.exceptions import ElasticClientException
from app.service.config import config
from app.service.client import ElasticClient
from pprint import pprint
from app.domain.index_difference import IndexDifference
from app.service.compare_mappings import compare_mappings


def main():

    client = ElasticClient(config.elastic_host)
    new_codename = input("Provide a codename of your current Tracardi version:\n")
    old_codename = input("Provide a codename of your old Tracardi version:\n")

    try:
        old_indices = client.mappings_for_codename(old_codename, new_codename == old_codename)
        new_indices = client.mappings_for_codename(new_codename)
        client.close()

        diffs = [
            IndexDifference(
                name=key,
                difference=compare_mappings(old_indices[key].mapping, new_indices[key].mapping),
                multi=old_indices[key].multi and new_indices[key].multi,
            )
            for key in set(new_indices.keys()).intersection(old_indices.keys())
        ]

        for index_diff in diffs:
            print(index_diff.difference)

    except ElasticClientException as e:
        client.close()
        print(f"Error info: {str(e)}")
        return


if __name__ == "__main__":
    main()
