"""
LawBridge AI — InLegalBERT Fine-tuning Pipeline
================================================
Fine-tunes InLegalBERT (pre-trained on Indian legal text)
for clause risk classification.

InLegalBERT paper: https://arxiv.org/abs/2209.06049
Model: law-ai/InLegalBERT (HuggingFace)

Why InLegalBERT over vanilla BERT:
- Pre-trained on Indian Supreme Court + High Court judgments
- Understands Indian legal terminology natively
- 12 layers, 768 hidden, 12 attention heads
- Significantly better than BERT-base on Indian legal tasks

Run:
  pip install transformers torch datasets scikit-learn
  python -m app.ml.bert.finetune

Requirements:
  - 8GB+ RAM recommended
  - GPU optional (CPU works, slower)
  - ~2-4 hours on CPU, ~20 min on GPU
"""

import os
import json
import logging
import numpy as np
from typing import List, Dict, Tuple
from dataclasses import dataclass
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ── Training Data ─────────────────────────────────────────────────────────────
# Expanded synthetic dataset for fine-tuning
# In production: replace with real labeled clauses from IndiaKanoon/JUDIS

LABELED_CLAUSES = [
    # ─── CRITICAL ───────────────────────────────────────────────────────────
    ("The landlord may file criminal complaint and FIR against the tenant for any default in payment", "critical"),
    ("Failure to vacate premises will result in police complaint and criminal proceedings under IPC", "critical"),
    ("Company may initiate criminal action under Section 420 IPC for breach of this agreement", "critical"),
    ("Arrest warrant shall be sought immediately upon violation of this confidentiality clause", "critical"),
    ("Criminal liability under Indian Penal Code shall apply for unauthorized disclosure of information", "critical"),
    ("Borrower shall face criminal prosecution under Section 138 Negotiable Instruments Act for default", "critical"),
    ("Criminal complaint will be filed against employee for violation of non-compete provisions", "critical"),
    ("Police action shall be initiated without notice upon breach of payment obligations", "critical"),
    ("FIR shall be registered under relevant IPC sections for any misappropriation of funds", "critical"),
    ("Criminal proceedings under PMLA may be initiated for suspicious transactions by borrower", "critical"),

    # ─── HIGH ───────────────────────────────────────────────────────────────
    ("The employer may terminate employment without cause or prior notice at any time whatsoever", "high"),
    ("Employee shall not engage in any competing business for 3 years after leaving the company", "high"),
    ("Employee must pay bond amount of Rs 5 lakh if leaving within 2 years of joining", "high"),
    ("Landlord may evict tenant immediately without any notice period or court order", "high"),
    ("Confidentiality obligation shall remain perpetual and indefinite with no time limit", "high"),
    ("Employee shall not moonlight or take up any outside employment during tenure with company", "high"),
    ("All intellectual property created during employment belongs exclusively to company forever", "high"),
    ("Guarantor shall be personally liable for all outstanding loan amounts upon borrower default", "high"),
    ("Prepayment penalty of 5% of outstanding amount applies if loan is repaid before maturity", "high"),
    ("Cross default clause applies if borrower defaults on any other financial obligation with any lender", "high"),
    ("Tenant must vacate premises within 24 hours upon landlord verbal or written demand", "high"),
    ("Non-solicitation clause prevents employee from contacting any company clients for 2 years after exit", "high"),
    ("Company may terminate employment with immediate effect for any policy violation without hearing", "high"),
    ("Service bond amount of Rs 2 lakh shall be recovered if employee leaves before 18 months", "high"),
    ("Employee agrees not to join any competitor company for 24 months post resignation or termination", "high"),
    ("Lender may seize and sell collateral property without court order upon single payment default", "high"),
    ("Company owns all inventions, source code, designs created by employee including on personal time", "high"),
    ("Employer can terminate without severance pay or any compensation for alleged policy violations", "high"),
    ("Tenant forfeits entire security deposit without deduction for any breach of agreement terms", "high"),
    ("Employee waives right to severance, notice pay, or any compensation upon termination for cause", "high"),
    ("Loan may be called back in full within 7 days notice if any covenant is breached by borrower", "high"),
    ("Non-disclosure obligation applies to all information ever shared regardless of marking as confidential", "high"),
    ("Employee IP assignment covers all work done during employment including evenings and weekends", "high"),
    ("Liquidated damages of Rs 10 lakh apply for breach of exclusivity provisions by service provider", "high"),
    ("At-will termination clause allows employer to dismiss employee without reason or compensation", "high"),
    ("Unlimited personal liability of director applies for all company debts under this guarantee", "high"),
    ("Employee shall not publish any research, paper, or article without prior written company approval", "high"),
    ("Automatic forfeiture of all unvested stock options upon resignation regardless of tenure", "high"),
    ("Borrower grants irrevocable power of attorney to lender to sell assets upon default", "high"),
    ("Restraint of trade clause prevents employee from working in same industry for 3 years nationally", "high"),

    # ─── MEDIUM ─────────────────────────────────────────────────────────────
    ("Lock-in period of 11 months applies from commencement of tenancy under this agreement", "medium"),
    ("Rent shall be increased by 10% annually on each anniversary date of this rental agreement", "medium"),
    ("Notice period of 90 days required before termination of employment by either party", "medium"),
    ("All disputes under this agreement shall be resolved through arbitration in Mumbai", "medium"),
    ("Employee may be transferred to any company location at employer discretion without consent", "medium"),
    ("Probation period of 6 months during which termination without detailed cause is permitted", "medium"),
    ("Confidential information includes all business data shared during the engagement period", "medium"),
    ("Tenant shall be responsible for all maintenance charges including major structural repairs", "medium"),
    ("Interest rate of 18% per annum shall apply on all delayed EMI payments after due date", "medium"),
    ("Security deposit of 3 months rent to be paid before taking occupancy of the premises", "medium"),
    ("Non-disclosure obligation covers all information received during the entire project engagement", "medium"),
    ("Jurisdiction for all disputes under this agreement shall be courts in specified city only", "medium"),
    ("Employee cannot take any leave during probation period without prior written management approval", "medium"),
    ("Escalation clause allows rent increase up to 15% at each renewal period of this agreement", "medium"),
    ("Employee salary structure may be revised at company discretion during annual appraisal cycle", "medium"),
    ("Painting and repainting costs of the entire flat shall be borne by tenant upon vacation", "medium"),
    ("Service provider cannot subcontract work to third parties without prior written client approval", "medium"),
    ("Loan processing fee of 2% of sanctioned amount is non-refundable upon application approval", "medium"),
    ("Notice period of 60 days applies if employment is terminated by employer during probation period", "medium"),
    ("Monthly maintenance charges shall be paid by tenant in addition to monthly rent amount", "medium"),
    ("Employee bonus is discretionary and shall be paid at sole discretion of management without obligation", "medium"),
    ("Brokerage fee equivalent to one month rent shall be paid by tenant to agent upon signing", "medium"),
    ("Employer can change employee designation, role, and reporting structure without prior notice", "medium"),
    ("Arbitration fee shall be shared equally by both parties for disputes under this agreement", "medium"),
    ("Interest rate may be revised by lender with 30 days notice during loan tenure", "medium"),
    ("Tenant shall obtain police verification certificate within 15 days of taking occupancy", "medium"),
    ("Performance improvement plan may be initiated at company discretion affecting bonus eligibility", "medium"),
    ("Stamp duty and registration charges for this agreement shall be borne equally by both parties", "medium"),
    ("Service provider shall maintain professional indemnity insurance throughout project duration", "medium"),
    ("EMI date may be changed by lender with 15 days notice to borrower", "medium"),

    # ─── LOW ────────────────────────────────────────────────────────────────
    ("This agreement shall be governed by the laws of India and Indian courts shall have jurisdiction", "low"),
    ("Force majeure clause applies for acts beyond reasonable control including natural disasters", "low"),
    ("Agreement may be renewed upon mutual written consent of both contracting parties before expiry", "low"),
    ("All notices shall be sent by registered post to the addresses mentioned in this agreement", "low"),
    ("This agreement constitutes the entire understanding between both parties superseding all prior discussions", "low"),
    ("Any amendments to this agreement must be made in writing and signed by authorized representatives", "low"),
    ("Tenant shall maintain the rented property in good and clean condition throughout tenancy period", "low"),
    ("Employee agrees to maintain confidentiality of company information during period of employment", "low"),
    ("Payment shall be made within 30 days of invoice receipt as mutually agreed between parties", "low"),
    ("Either party may terminate this agreement by giving 30 days written notice to the other party", "low"),
    ("Landlord shall provide proper receipts for all payments received from tenant upon request", "low"),
    ("Employee is entitled to all statutory leaves as applicable under relevant labour law in India", "low"),
    ("Service provider shall deliver all agreed work as per the mutually agreed project timeline", "low"),
    ("Parties agree to attempt resolution of all disputes through mutual discussion before arbitration", "low"),
    ("Both parties have read, understood, and voluntarily agreed to all terms of this agreement", "low"),
    ("Governing law of this agreement shall be the laws of India applicable to contracts generally", "low"),
    ("Confidentiality clause survives termination of this agreement for period specified in schedule", "low"),
    ("Both parties agree to maintain proper records and documentation as required by applicable law", "low"),
    ("Service charges and applicable taxes shall be paid by client as per government regulations", "low"),
    ("Agreement shall automatically renew for successive one year terms unless terminated by either party", "low"),
    ("Notices under this agreement deemed served 48 hours after posting by registered post", "low"),
    ("Dispute resolution through Lok Adalat available as alternative to arbitration for parties", "low"),
    ("Employee shall return all company property including laptop and access cards on last working day", "low"),
    ("Borrower must maintain insurance on mortgaged property for full replacement value throughout tenure", "low"),
    ("Both parties confirm they have authority to enter into and perform obligations under this agreement", "low"),
    ("Headings in this agreement are for convenience only and shall not affect interpretation of clauses", "low"),
    ("Waiver of any right by either party shall not be deemed waiver of future rights under agreement", "low"),
    ("If any provision of this agreement is found invalid, remaining provisions shall continue in force", "low"),
    ("Agreement may be executed in counterparts each of which shall constitute an original document", "low"),
    ("Time is of the essence for all obligations and deadlines specified in this agreement", "low"),
]


@dataclass
class TrainingConfig:
    model_name: str = "law-ai/InLegalBERT"
    fallback_model: str = "bert-base-uncased"
    max_length: int = 256
    batch_size: int = 8
    num_epochs: int = 5
    learning_rate: float = 2e-5
    warmup_ratio: float = 0.1
    weight_decay: float = 0.01
    output_dir: str = "app/ml/models/bert"
    test_size: float = 0.2
    seed: int = 42


def check_dependencies() -> bool:
    """Check if required packages are installed."""
    missing = []
    for pkg in ['torch', 'transformers', 'datasets']:
        try:
            __import__(pkg)
        except ImportError:
            missing.append(pkg)
    if missing:
        print(f"\n❌ Missing packages: {', '.join(missing)}")
        print(f"Install with: pip install {' '.join(missing)}")
        return False
    return True


def prepare_dataset(data: List[Tuple[str, str]], config: TrainingConfig):
    """Prepare dataset for BERT fine-tuning."""
    from datasets import Dataset

    texts = [d[0] for d in data]
    labels_str = [d[1] for d in data]

    le = LabelEncoder()
    labels = le.fit_transform(labels_str).tolist()

    X_train, X_test, y_train, y_test = train_test_split(
        texts, labels, test_size=config.test_size,
        random_state=config.seed, stratify=labels
    )

    train_dataset = Dataset.from_dict({"text": X_train, "label": y_train})
    test_dataset = Dataset.from_dict({"text": X_test, "label": y_test})

    return train_dataset, test_dataset, le


def tokenize_dataset(dataset, tokenizer, config: TrainingConfig):
    """Tokenize dataset for BERT."""
    def tokenize(batch):
        return tokenizer(
            batch["text"],
            truncation=True,
            padding="max_length",
            max_length=config.max_length
        )
    return dataset.map(tokenize, batched=True)


def compute_metrics(eval_pred):
    """Compute metrics for trainer."""
    from sklearn.metrics import accuracy_score, f1_score
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return {
        "accuracy": accuracy_score(labels, predictions),
        "f1_macro": f1_score(labels, predictions, average="macro")
    }


def finetune_inlegalbert(config: TrainingConfig = None):
    """Main fine-tuning function."""
    if not check_dependencies():
        print("\n💡 Running baseline sklearn training instead...")
        return train_sklearn_baseline()

    if config is None:
        config = TrainingConfig()

    import torch
    from transformers import (
        AutoTokenizer, AutoModelForSequenceClassification,
        TrainingArguments, Trainer, EarlyStoppingCallback
    )

    print("=" * 65)
    print("LawBridge AI — InLegalBERT Fine-tuning Pipeline")
    print("=" * 65)
    print(f"Model: {config.model_name}")
    print(f"Device: {'GPU (CUDA)' if torch.cuda.is_available() else 'CPU (slower but works)'}")
    print(f"Training samples: {len(LABELED_CLAUSES)}")
    print(f"Epochs: {config.num_epochs}")
    print(f"Max length: {config.max_length} tokens")
    print("=" * 65)

    # Prepare data
    print("\n📊 Preparing dataset...")
    train_dataset, test_dataset, le = prepare_dataset(LABELED_CLAUSES, config)
    num_labels = len(le.classes_)
    print(f"Classes: {list(le.classes_)}")
    print(f"Train: {len(train_dataset)} | Test: {len(test_dataset)}")

    # Load tokenizer + model
    print(f"\n📥 Loading {config.model_name}...")
    try:
        tokenizer = AutoTokenizer.from_pretrained(config.model_name)
        model = AutoModelForSequenceClassification.from_pretrained(
            config.model_name,
            num_labels=num_labels,
            ignore_mismatched_sizes=True
        )
        print(f"✅ Loaded InLegalBERT successfully!")
    except Exception as e:
        print(f"⚠️ Could not load InLegalBERT: {e}")
        print(f"⚠️ Falling back to: {config.fallback_model}")
        tokenizer = AutoTokenizer.from_pretrained(config.fallback_model)
        model = AutoModelForSequenceClassification.from_pretrained(
            config.fallback_model, num_labels=num_labels
        )

    # Tokenize
    print("\n🔤 Tokenizing dataset...")
    train_tok = tokenize_dataset(train_dataset, tokenizer, config)
    test_tok = tokenize_dataset(test_dataset, tokenizer, config)
    train_tok.set_format("torch", columns=["input_ids", "attention_mask", "label"])
    test_tok.set_format("torch", columns=["input_ids", "attention_mask", "label"])

    # Training args
    os.makedirs(config.output_dir, exist_ok=True)
    training_args = TrainingArguments(
        output_dir=config.output_dir,
        num_train_epochs=config.num_epochs,
        per_device_train_batch_size=config.batch_size,
        per_device_eval_batch_size=config.batch_size,
        learning_rate=config.learning_rate,
        weight_decay=config.weight_decay,
        warmup_ratio=config.warmup_ratio,
        evaluation_strategy="epoch",
        save_strategy="epoch",
        load_best_model_at_end=True,
        metric_for_best_model="f1_macro",
        logging_dir=os.path.join(config.output_dir, "logs"),
        logging_steps=10,
        seed=config.seed,
        report_to="none",
    )

    # Trainer
    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=train_tok,
        eval_dataset=test_tok,
        compute_metrics=compute_metrics,
        callbacks=[EarlyStoppingCallback(early_stopping_patience=2)]
    )

    # Train
    print("\n🚀 Starting fine-tuning...")
    print("This will take 20-60 minutes on CPU. Go grab a coffee! ☕")
    print("-" * 65)
    trainer.train()

    # Evaluate
    print("\n📊 Final Evaluation:")
    results = trainer.evaluate()
    print(f"✅ Accuracy: {results['eval_accuracy']:.2%}")
    print(f"✅ F1 Macro: {results['eval_f1_macro']:.2%}")

    # Save model
    print(f"\n💾 Saving model to {config.output_dir}...")
    trainer.save_model(config.output_dir)
    tokenizer.save_pretrained(config.output_dir)

    # Save label encoder + metadata
    import joblib
    joblib.dump(le, os.path.join(config.output_dir, "label_encoder.pkl"))

    metadata = {
        "model_name": "InLegalBERT-clause-risk",
        "base_model": config.model_name,
        "version": "1.0",
        "task": "clause_risk_classification",
        "classes": list(le.classes_),
        "accuracy": round(results['eval_accuracy'], 4),
        "f1_macro": round(results['eval_f1_macro'], 4),
        "training_samples": len(LABELED_CLAUSES),
        "epochs": config.num_epochs,
        "max_length": config.max_length,
        "note": "Fine-tuned InLegalBERT on Indian legal clause risk classification. Production needs 5000+ labeled clauses."
    }
    with open(os.path.join(config.output_dir, "metadata.json"), "w") as f:
        json.dump(metadata, f, indent=2)

    print("\n" + "=" * 65)
    print("✅ Fine-tuning Complete!")
    print("=" * 65)
    print(f"Model saved: {config.output_dir}/")
    print(f"Accuracy: {results['eval_accuracy']:.2%}")
    print(f"F1 Macro: {results['eval_f1_macro']:.2%}")
    print("\nExpected improvement over sklearn baseline:")
    print("  sklearn (55 samples):    ~58% accuracy")
    print(f"  InLegalBERT ({len(LABELED_CLAUSES)} samples): {results['eval_accuracy']:.2%} accuracy")
    return model, tokenizer, le, metadata


def train_sklearn_baseline():
    """Fallback sklearn training with expanded dataset."""
    print("\n🔄 Running expanded sklearn training...")
    from sklearn.pipeline import Pipeline
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression
    from sklearn.model_selection import cross_val_score
    import joblib

    texts = [d[0] for d in LABELED_CLAUSES]
    labels = [d[1] for d in LABELED_CLAUSES]
    le = LabelEncoder()
    y = le.fit_transform(labels)

    X_train, X_test, y_train, y_test = train_test_split(
        texts, y, test_size=0.2, random_state=42, stratify=y
    )

    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=10000, min_df=1, sublinear_tf=True)),
        ('clf', LogisticRegression(max_iter=2000, C=1.0, class_weight='balanced', random_state=42))
    ])
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    cv = cross_val_score(model, texts, y, cv=5, scoring='accuracy')

    print(f"\n✅ Accuracy: {accuracy:.2%}")
    print(f"✅ CV Score: {cv.mean():.2%} ± {cv.std():.2%}")
    print("\n" + classification_report(y_test, y_pred, target_names=le.classes_))

    os.makedirs("app/ml/models", exist_ok=True)
    joblib.dump(model, "app/ml/models/clause_risk_v2.pkl")
    joblib.dump(le, "app/ml/models/label_encoder_v2.pkl")

    metadata = {
        "model_name": "clause_risk_classifier_v2",
        "algorithm": "TF-IDF + Logistic Regression (expanded dataset)",
        "training_samples": len(texts),
        "classes": list(le.classes_),
        "accuracy": round(float(accuracy), 4),
        "cv_mean": round(float(cv.mean()), 4),
        "improvement_over_v1": f"{(accuracy - 0.5455)*100:.1f}% better than v1",
        "note": "Use InLegalBERT pipeline for production-grade accuracy."
    }
    with open("app/ml/models/metadata_v2.json", "w") as f:
        json.dump(metadata, f, indent=2)

    print(f"\n💾 Saved: app/ml/models/clause_risk_v2.pkl")
    print(f"📈 Improvement: {(accuracy - 0.5455)*100:.1f}% better than v1 (55 samples)")
    return model, le, metadata


if __name__ == "__main__":
    config = TrainingConfig()
    result = finetune_inlegalbert(config)
