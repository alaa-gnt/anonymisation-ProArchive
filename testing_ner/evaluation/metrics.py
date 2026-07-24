"""
Evaluation metrics for NER model comparison.
"""

def ner_precision_recall_f1(ground_truth: list[dict], predictions: list[dict]) -> dict:
    """
    Compute precision, recall, F1 for NER entity detection.

    Each dict: {"text": "...", "type": "...", "start": int, "end": int}
    """
    gt_set = {(e["text"].lower(), e["type"]) for e in ground_truth}
    pred_set = {(e["text"].lower(), e["type"]) for e in predictions}

    tp = len(gt_set & pred_set)
    fp = len(pred_set - gt_set)
    fn = len(gt_set - pred_set)

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0

    return {
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "true_positives": tp,
        "false_positives": fp,
        "false_negatives": fn,
    }


def entities_to_dict(entities, text: str) -> list[dict]:
    """Convert spaCy/Stanza/Flair entities to standard dict format."""
    result = []
    for ent in entities:
        result.append({
            "text": ent.text if hasattr(ent, "text") else ent["text"],
            "type": ent.label_ if hasattr(ent, "label_") else ent["type"],
            "start": ent.start_char if hasattr(ent, "start_char") else ent.get("start", 0),
            "end": ent.end_char if hasattr(ent, "end_char") else ent.get("end", 0),
        })
    return result
