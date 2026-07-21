from collections import defaultdict


def _assign_pseudonyms(text, analyzer_results):
    groups = defaultdict(set)
    for r in analyzer_results:
        val = text[r.start:r.end]
        if r.entity_type == "PERSON":
            key = val.split()[0] if val.split() else val
        else:
            key = val
        groups[(r.entity_type, key)].add(val)

    assignments = {}
    counter = defaultdict(int)
    for (entity_type, key), vals in sorted(groups.items()):
        counter[entity_type] += 1
        tag = f"<{entity_type}_{counter[entity_type]}>"
        for v in vals:
            assignments[(entity_type, v)] = tag
    return assignments


def anonymize_with_pseudonyms(text, analyzer_results, operators=None):
    assignments = _assign_pseudonyms(text, analyzer_results)

    sorted_results = sorted(analyzer_results, key=lambda r: -r.start)

    result = text
    for r in sorted_results:
        original = text[r.start:r.end]
        replacement = assignments.get((r.entity_type, original), original)
        result = result[:r.start] + replacement + result[r.end:]

    return result
