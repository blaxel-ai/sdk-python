Module blaxel.knowledgebases.types
==================================

Classes
-------

`KnowledgebaseClass()`
:   Helper class that provides a standard way to create an ABC using
    inheritance.

    ### Ancestors (in MRO)

    * abc.ABC

    ### Descendants

    * blaxel.knowledgebases.chroma.ChromaKnowledgebase
    * blaxel.knowledgebases.pinecone.PineconeKnowledgebase
    * blaxel.knowledgebases.qdrant.QdrantKnowledgebase

    ### Methods

    `add(self, key: str, value: str, infos: Any | None = None) ‑> None`
    :

    `close(self) ‑> None`
    :

    `delete(self, key: str) ‑> None`
    :

    `search(self, query: str, filters: Any | None = None, score_threshold: float | None = None, limit: int | None = None) ‑> List[blaxel.knowledgebases.types.KnowledgebaseSearchResult]`
    :

`KnowledgebaseConfig(type: str, knowledge_base: Dict[str, Any], connection: Dict[str, Any])`
:   KnowledgebaseConfig(type: str, knowledge_base: Dict[str, Any], connection: Dict[str, Any])

    ### Instance variables

    `connection: Dict[str, Any]`
    :

    `knowledge_base: Dict[str, Any]`
    :

    `type: str`
    :

`KnowledgebaseSearchResult(key: str, value: Any, similarity: float)`
:   KnowledgebaseSearchResult(key: str, value: Any, similarity: float)

    ### Instance variables

    `key: str`
    :

    `similarity: float`
    :

    `value: Any`
    :