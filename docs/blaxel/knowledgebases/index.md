Module blaxel.knowledgebases
============================

Sub-modules
-----------
* blaxel.knowledgebases.chroma
* blaxel.knowledgebases.embeddings
* blaxel.knowledgebases.factory
* blaxel.knowledgebases.pinecone
* blaxel.knowledgebases.qdrant
* blaxel.knowledgebases.types

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
:   

`KnowledgebaseFactory()`
:   

    ### Static methods

    `create(config: blaxel.knowledgebases.factory.KnowledgebaseConfig) ‑> blaxel.knowledgebases.types.KnowledgebaseClass`
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