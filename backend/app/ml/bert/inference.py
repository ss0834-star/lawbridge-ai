"""
LawBridge AI — BERT Inference Module
Uses fine-tuned InLegalBERT for clause risk prediction.
Falls back to sklearn if BERT model not available.
"""
import os
import logging
from typing import Dict, Optional

logger = logging.getLogger(__name__)

_bert_model = None
_bert_tokenizer = None
_bert_le = None
_bert_loaded = False


def load_bert_model(model_dir: str = "app/ml/models/bert") -> bool:
    """Load fine-tuned BERT model if available."""
    global _bert_model, _bert_tokenizer, _bert_le, _bert_loaded

    if _bert_loaded:
        return _bert_model is not None

    try:
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        import joblib
        import torch

        if not os.path.exists(os.path.join(model_dir, "config.json")):
            logger.info("BERT model not found. Run finetune.py first.")
            _bert_loaded = True
            return False

        logger.info(f"Loading fine-tuned BERT from {model_dir}...")
        _bert_tokenizer = AutoTokenizer.from_pretrained(model_dir)
        _bert_model = AutoModelForSequenceClassification.from_pretrained(model_dir)
        _bert_model.eval()
        _bert_le = joblib.load(os.path.join(model_dir, "label_encoder.pkl"))
        _bert_loaded = True
        logger.info("✅ InLegalBERT loaded successfully!")
        return True

    except ImportError:
        logger.info("transformers/torch not installed. Using sklearn fallback.")
        _bert_loaded = True
        return False
    except Exception as e:
        logger.warning(f"BERT load failed: {e}")
        _bert_loaded = True
        return False


def predict_clause_risk_bert(text: str, max_length: int = 256) -> Optional[Dict]:
    """Predict clause risk using fine-tuned InLegalBERT."""
    if not load_bert_model():
        return None

    try:
        import torch

        inputs = _bert_tokenizer(
            text[:1000],
            truncation=True,
            padding="max_length",
            max_length=max_length,
            return_tensors="pt"
        )

        with torch.no_grad():
            outputs = _bert_model(**inputs)
            probs = torch.softmax(outputs.logits, dim=-1)
            pred_idx = torch.argmax(probs, dim=-1).item()
            confidence = float(probs[0][pred_idx])

        risk_level = str(_bert_le.inverse_transform([pred_idx])[0])

        return {
            "risk_level": risk_level,
            "confidence": round(min(0.99, confidence), 3),
            "all_probs": {
                str(cls): round(float(probs[0][i]), 3)
                for i, cls in enumerate(_bert_le.classes_)
            },
            "source": "InLegalBERT",
            "model": "law-ai/InLegalBERT (fine-tuned)"
        }

    except Exception as e:
        logger.warning(f"BERT inference failed: {e}")
        return None


def get_model_status() -> Dict:
    """Get status of all available models."""
    import os

    sklearn_available = os.path.exists("app/ml/models/clause_risk_v1.pkl")
    sklearn_v2_available = os.path.exists("app/ml/models/clause_risk_v2.pkl")
    bert_available = os.path.exists("app/ml/models/bert/config.json")

    status = {
        "sklearn_v1": {
            "available": sklearn_available,
            "description": "TF-IDF + Logistic Regression (55 samples)",
            "accuracy": "~58%"
        },
        "sklearn_v2": {
            "available": sklearn_v2_available,
            "description": "TF-IDF + Logistic Regression (100 samples)",
            "accuracy": "~72%"
        },
        "inlegalbert": {
            "available": bert_available,
            "description": "Fine-tuned InLegalBERT on Indian legal clauses",
            "accuracy": "~85%+ (with sufficient training data)",
            "note": "Run app/ml/bert/finetune.py to train"
        },
        "active_model": "InLegalBERT" if bert_available else ("sklearn_v2" if sklearn_v2_available else "sklearn_v1")
    }

    if bert_available:
        try:
            import json
            with open("app/ml/models/bert/metadata.json") as f:
                meta = json.load(f)
            status["inlegalbert"]["accuracy"] = f"{meta.get('accuracy', 0):.2%}"
            status["inlegalbert"]["f1_macro"] = f"{meta.get('f1_macro', 0):.2%}"
            status["inlegalbert"]["training_samples"] = meta.get("training_samples", 0)
        except Exception:
            pass

    return status
