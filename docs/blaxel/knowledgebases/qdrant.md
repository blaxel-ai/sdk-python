Module blaxel.knowledgebases.qdrant
===================================

Classes
-------

`QdrantKnowledgebase(connection: Dict[str, Any], knowledge_base: Dict[str, Any])`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * blaxel.knowledgebases.types.KnowledgebaseClass
    * abc.ABC

    ### Methods

    `add(self, key: str, value: str, infos: Any | None = None) ‑> None`
    :

    `close(self)`
    :

    `delete(self, key: str) ‑> None`
    :

    `get_or_create_collection(self, embeddings: Dict[str, Any], retry: int = 0) ‑> None`
    :

    `handle_error(self, action: str, error: Exception) ‑> Exception`
    :

    `search(self, query: str, filters: Any | None = None, score_threshold: float | None = None, limit: int | None = None) ‑> List[blaxel.knowledgebases.types.KnowledgebaseSearchResult]`
    :