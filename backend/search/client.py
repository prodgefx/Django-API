from algoliasearch_django import algolia_engine


def get_client():
    return algolia_engine.client


def perform_search(query, index_name="cfe_Product", **kwargs):
    client = get_client()

    params = {}
    tags = ""

    if "tags" in kwargs:
        tags = kwargs.pop("tags") or []
        if len(tags) != 0:
            params["tagFilters"] = tags

    index_filters = [f"{k}:{v}" for k,v in kwargs.items() if v]

    if len(index_filters) != 0:
        params['facetFilters'] = index_filters

    params["query"] = query
    results = client.search_single_index(
        index_name=index_name,
        search_params=params,
    )
    print(params)
    return results.hits