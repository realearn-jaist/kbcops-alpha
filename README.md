# kbcops-alpha

Report Fixed on Owl2vec\* Library

1.  Change to

    ```
    self.model* = Word2Vec(
    sentences,
    vector_size=self.vector_size,
    window=self.window,
    workers=self.n_jobs,
    sg=self.sg,
    epochs=self.max_iter,
    negative=self.negative,
    min_count=self.min_count,
    seed=42,)
    ```

    from

    ```
    self.model* = Word2Vec(
    sentences,
    size=self.vector_size,
    window=self.window,
    workers=self.n_jobs,
    sg=self.sg,
    iter=self.max_iter,
    negative=self.negative,
    min_count=self.min_count,
    seed=42,
    )
    ```

    in \kbcops-alpha\backend\owl2vec_star\rdf2vec\embed.py

2.  Change to
    ```
    def get_rdf2vec_embed(onto_file, walker_type, walk_depth, embed_size, classes):
    kg, walker = construct_kg_walker(
    onto_file=onto_file, walker_type=walker_type, walk_depth=walk_depth
    )
    transformer = RDF2VecTransformer(walkers=[walker], vector_size=embed_size)
    instances = [rdflib.URIRef(c) for c in classes]
    walk_embeddings = transformer.fit_transform(graph=kg, instances=instances)
    return np.array(walk_embeddings), transformer
    ```
    from
    ```
    def get_rdf2vec_embed(onto_file, walker_type, walk_depth, embed_size, classes):
    kg, walker = construct_kg_walker(
    onto_file=onto_file, walker_type=walker_type, walk_depth=walk_depth
    )
    transformer = RDF2VecTransformer(walkers=[walker], vector_size=embed_size)
    instances = [rdflib.URIRef(c) for c in classes]
    walk_embeddings = transformer.fit_transform(graph=kg, instances=instances)
    return np.array(walk_embeddings)
    ```
    in \kbcops-alpha\backend\owl2vec_star\RDF2Vec_Embed.py
