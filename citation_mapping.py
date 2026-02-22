from citationmappingmodule import CitationMapper


def process_citations(doc_id="manual_doc", text="", reference_list=None):
    """REST API uyumluluğu için atıf işleme yardımcı fonksiyonu."""
    mapper = CitationMapper()

    if reference_list is None:
        reference_list = []

    citations = mapper.extract_references(text) if text else []
    citation_map = mapper.map_citations_to_references(citations, reference_list)

    if text:
        mapper.save_citation_map_to_sqlite(doc_id, citation_map, text)
        mapper.save_citation_map_to_chromadb(doc_id, citation_map, text)
        mapper.save_citation_map_to_redis(doc_id, citation_map, text)

    return citation_map
