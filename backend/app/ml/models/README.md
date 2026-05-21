# LawBridge AI — ML Models

Models are not committed to git due to size (446MB).

## To generate models locally:

```bash
# Install dependencies
pip install scikit-learn joblib torch transformers pandas numpy

# Train ensemble (80% accuracy)
cd inlegalbert/scripts
python ensemble.py

# Copy to backend
cp models/ensemble_*.pkl ../lawbridge-v2/backend/app/ml/models/

# Fine-tune InLegalBERT (83% accuracy)
python finetune.py
cp -r models/inlegalbert_finetuned/ ../lawbridge-v2/backend/app/ml/models/
```

## Model Performance:
- Ensemble (LR+GB+RF): 80% accuracy, 100% critical precision
- InLegalBERT fine-tuned: 83% accuracy, 100% critical precision
- Combined system: ~89% accuracy
