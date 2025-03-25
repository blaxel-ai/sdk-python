Module blaxel.knowledgebases.embeddings
=======================================

Classes
-------

`EmbeddingModel(model: str, model_type: str, client: blaxel.client.Client)`
:   

    ### Methods

    `embed(self, query: str) ‑> List[float]`
    :

    `handle_error(self, error: blaxel.common.error.HTTPError) ‑> blaxel.common.error.HTTPError`
    :

    `openai_embed(self, query: str) ‑> List[float]`
    :