# Retrieval-augmented generation

Retrieval-augmented generation, or RAG, first finds relevant passages in a document collection. It then supplies those passages as context to a language model when producing an answer. This gives the model relevant source material, but the answer can still be wrong and should be checked against its citations.

Chunking splits longer documents into manageable passages. A simple lexical retriever scores passages based on words they share with the question. This demo uses local token-based TF-IDF scoring and does not require embedding downloads. Lexical retrieval may miss relevant passages that use different vocabulary.

If no local Ollama model is configured, this app returns the matching passages instead of fabricating a generated answer. When Ollama is configured, the prompt asks for an answer grounded in the retrieved passages and for citations using their bracketed passage numbers.
