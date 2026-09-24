"""Small deterministic lexical retriever; no external models or downloads."""
import math
import re
from collections import Counter


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.casefold())


def chunks(text: str, limit: int = 650) -> list[str]:
    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    result = []
    current = ""
    for paragraph in paragraphs:
        # Long pasted paragraphs are split on word boundaries.
        words = paragraph.split()
        pieces, piece = [], ""
        for word in words:
            if piece and len(piece) + len(word) + 1 > limit:
                pieces.append(piece)
                piece = word
            else:
                piece = (piece + " " + word).strip()
        if piece:
            pieces.append(piece)
        for part in pieces:
            if current and len(current) + len(part) + 2 > limit:
                result.append(current)
                current = part
            else:
                current = (current + "\n\n" + part).strip()
    if current:
        result.append(current)
    return result


def retrieve(question: str, passages: list[dict], k: int = 3) -> list[dict]:
    query = set(tokens(question)) - {"the", "and", "what", "how", "does", "can", "for", "with", "is", "a", "to", "in", "of"}
    if not query:
        return []
    documents = [Counter(tokens(p["content"] + " " + p["title"])) for p in passages]
    n = len(documents)
    scored = []
    for passage, bag in zip(passages, documents):
        score = 0.0
        for term in query:
            if bag[term]:
                df = sum(term in other for other in documents)
                score += (1 + math.log(bag[term])) * (1 + math.log((n + 1) / (df + 1)))
        if score:
            scored.append((score, passage))
    scored.sort(key=lambda pair: (-pair[0], pair[1]["id"]))
    return [dict(passage, score=round(score, 3)) for score, passage in scored[:k]]
