"""
LawBridge AI — Real ML Training Pipeline
Trains clause risk classifier + document type classifier
on synthetic Indian legal data.

Run: python -m app.ml.training.train
"""
import os
import json
import joblib
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import LabelEncoder

TRAINING_DATA = [
    # CRITICAL
    ("The landlord may file criminal complaint and FIR against tenant for any default", "critical"),
    ("Failure to vacate will result in police complaint and criminal proceedings against tenant", "critical"),
    ("Company may initiate criminal action under IPC for breach of this agreement", "critical"),
    ("Immediate arrest warrant may be sought upon violation of this clause by employee", "critical"),
    ("Criminal liability shall apply for any unauthorized disclosure of confidential information", "critical"),
    ("Borrower shall face criminal prosecution under Section 138 NI Act for default", "critical"),

    # HIGH
    ("The employer may terminate employment without cause or prior notice at any time", "high"),
    ("Employee shall not engage in any competing business for 3 years after leaving", "high"),
    ("Employee must pay bond amount of Rs 5 lakh if leaving within 2 years of joining", "high"),
    ("Landlord may evict tenant immediately without any notice period or court order", "high"),
    ("Confidentiality obligation shall remain perpetual and indefinite with no time limit", "high"),
    ("Employee shall not moonlight or take up any outside employment during tenure", "high"),
    ("All intellectual property created during employment belongs exclusively to company forever", "high"),
    ("Guarantor shall be personally liable for all loan amounts upon borrower default", "high"),
    ("Prepayment penalty of 5% applies if loan is repaid before maturity date", "high"),
    ("Cross default clause applies if borrower defaults on any other financial obligation", "high"),
    ("Tenant must vacate premises within 24 hours upon landlord verbal demand", "high"),
    ("Non-solicitation clause prevents employee from contacting any company clients for 2 years", "high"),
    ("Company may terminate with immediate effect for any policy violation whatsoever", "high"),
    ("Bond amount of Rs 2 lakh shall be recovered if employee leaves before 18 months", "high"),
    ("Employee agrees not to join any competitor company for 24 months after resignation", "high"),
    ("Lender may seize collateral property without court order upon single payment default", "high"),
    ("Company owns all inventions, designs, code created by employee including personal projects", "high"),
    ("Employer can terminate without severance pay or any compensation for policy violations", "high"),
    ("Tenant forfeits entire security deposit for any breach of agreement terms", "high"),

    # MEDIUM
    ("Lock-in period of 11 months applies from commencement of tenancy agreement", "medium"),
    ("Rent shall be increased by 10% annually on each anniversary date of agreement", "medium"),
    ("Notice period of 90 days required before termination of employment by either party", "medium"),
    ("Arbitration clause applies for all disputes under this agreement in Mumbai", "medium"),
    ("Employee may be transferred to any location at employer discretion without consent", "medium"),
    ("Probation period of 6 months during which termination without detailed cause is permitted", "medium"),
    ("Confidential information includes all business data shared during the engagement period", "medium"),
    ("Tenant responsible for all maintenance charges including major structural repairs", "medium"),
    ("Interest rate of 18% per annum applies on delayed EMI payments", "medium"),
    ("Security deposit of 3 months rent to be paid before taking occupancy of flat", "medium"),
    ("Non-disclosure obligation covers all information received during project period", "medium"),
    ("Jurisdiction for all disputes shall be courts in specified city only", "medium"),
    ("Employee cannot take leave during probation period without prior written approval", "medium"),
    ("Escalation clause allows rent increase up to 15% at each renewal period", "medium"),
    ("Employee salary may be restructured at company discretion during appraisal cycle", "medium"),

    # LOW
    ("This agreement shall be governed by the laws of India and Indian courts", "low"),
    ("Force majeure clause applies for acts of god beyond reasonable control of parties", "low"),
    ("Agreement may be renewed upon mutual written consent of both contracting parties", "low"),
    ("Notice shall be sent by registered post to the addresses mentioned in this agreement", "low"),
    ("This agreement constitutes the entire understanding between both parties", "low"),
    ("Amendments to this agreement must be made in writing and signed by both parties", "low"),
    ("Tenant shall maintain the property in good condition throughout tenancy period", "low"),
    ("Employee agrees to maintain confidentiality of company information during employment", "low"),
    ("Payment shall be made within 30 days of invoice date as agreed by parties", "low"),
    ("Either party may terminate this agreement with 30 days written notice to other party", "low"),
    ("Landlord shall provide receipts for all payments made by tenant upon request", "low"),
    ("Employee is entitled to statutory leaves as per applicable labour law in India", "low"),
    ("Service provider shall deliver work as per mutually agreed project timeline", "low"),
    ("Parties agree to resolve disputes through mutual discussion before legal action", "low"),
    ("Both parties have read and understood the terms of this agreement fully", "low"),
]

DOC_TRAINING = [
    ("tenant landlord rent monthly property lease premises security deposit eviction notice period lock-in", "Rental Agreement"),
    ("rental agreement flat apartment house residential property maintenance charges painting repainting", "Rental Agreement"),
    ("lock-in period landlord tenant rent escalation painting charges police verification stamp duty", "Rental Agreement"),
    ("monthly rent security deposit landlord tenant property occupation lease period renewal", "Rental Agreement"),
    ("employee employer salary designation probation notice period compensation joining date appraisal", "Employment Contract"),
    ("employment contract designation CTC gross salary appraisal probation termination resignation", "Employment Contract"),
    ("non-compete non-solicitation moonlighting IP ownership training bond service bond notice period", "Employment Contract"),
    ("appointment letter joining date probation confirmation salary revision increment bonus", "Employment Contract"),
    ("confidential proprietary non-disclosure trade secret receiving party disclosing party information", "NDA"),
    ("NDA confidentiality agreement information protected perpetual duration exceptions mutual one-sided", "NDA"),
    ("confidentiality obligation disclosure restriction proprietary information penalty breach injunction", "NDA"),
    ("loan borrower lender interest rate EMI repayment principal collateral default recovery", "Loan Document"),
    ("credit facility disbursement prepayment penalty foreclosure guarantor personal guarantee mortgage", "Loan Document"),
    ("loan agreement repayment schedule interest principal outstanding amount default penalty", "Loan Document"),
    ("legal notice demand advocate client respond failure consequences legal action proceedings", "Legal Notice"),
    ("notice period days respond legal proceedings court action claimed amount advocate", "Legal Notice"),
    ("legal notice under section demand letter respond within days failure consequences", "Legal Notice"),
    ("service provider client deliverable milestone payment terms scope of work completion", "Service Agreement"),
    ("freelancer contractor project deliverable independent contractor payment schedule IP", "Freelance Contract"),
    ("partnership joint venture profit sharing business agreement shareholder equity stake", "Business Agreement"),
]


def train_clause_risk_classifier():
    print("🎯 Training Clause Risk Classifier...")
    texts = [d[0] for d in TRAINING_DATA]
    labels = [d[1] for d in TRAINING_DATA]
    le = LabelEncoder()
    y = le.fit_transform(labels)
    print(f"📊 Samples: {len(texts)} | Classes: {list(le.classes_)}")
    print(f"📊 Distribution: {dict(zip(le.classes_, np.bincount(y)))}")
    X_train, X_test, y_train, y_test = train_test_split(texts, y, test_size=0.2, random_state=42, stratify=y)
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 3), max_features=5000, min_df=1, sublinear_tf=True)),
        ('clf', LogisticRegression(max_iter=1000, C=1.0, class_weight='balanced', random_state=42))
    ])
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\n✅ Test Accuracy: {accuracy:.2%}")
    print("\n📋 Classification Report:")
    print(classification_report(y_test, y_pred, target_names=le.classes_))
    cv = cross_val_score(model, texts, y, cv=3, scoring='accuracy')
    print(f"🔄 Cross-validation: {cv.mean():.2%} ± {cv.std():.2%}")
    os.makedirs('app/ml/models', exist_ok=True)
    joblib.dump(model, 'app/ml/models/clause_risk_v1.pkl')
    joblib.dump(le, 'app/ml/models/label_encoder_v1.pkl')
    metadata = {
        "model_name": "clause_risk_classifier",
        "version": "1.0",
        "algorithm": "TF-IDF + Logistic Regression",
        "training_samples": len(texts),
        "classes": list(le.classes_),
        "accuracy": round(float(accuracy), 4),
        "cv_mean": round(float(cv.mean()), 4),
        "cv_std": round(float(cv.std()), 4),
        "note": "Trained on synthetic Indian legal data. Production accuracy requires real labeled data."
    }
    with open('app/ml/models/metadata_v1.json', 'w') as f:
        json.dump(metadata, f, indent=2)
    print(f"\n💾 Saved: app/ml/models/clause_risk_v1.pkl")
    return model, le, metadata


def train_document_classifier():
    print("\n🎯 Training Document Type Classifier...")
    texts = [d[0] for d in DOC_TRAINING]
    labels = [d[1] for d in DOC_TRAINING]
    le = LabelEncoder()
    y = le.fit_transform(labels)
    model = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1, 2), max_features=2000, min_df=1)),
        ('clf', LogisticRegression(max_iter=500, C=2.0, random_state=42))
    ])
    model.fit(texts, y)
    joblib.dump(model, 'app/ml/models/doc_classifier_v1.pkl')
    joblib.dump(le, 'app/ml/models/doc_label_encoder_v1.pkl')
    print(f"✅ Trained on {len(texts)} samples | Classes: {list(le.classes_)}")
    print(f"💾 Saved: app/ml/models/doc_classifier_v1.pkl")
    return model, le


if __name__ == "__main__":
    print("=" * 60)
    print("LawBridge AI — ML Training Pipeline")
    print("=" * 60)
    m1, le1, meta = train_clause_risk_classifier()
    m2, le2 = train_document_classifier()
    print("\n" + "=" * 60)
    print("✅ ALL MODELS TRAINED AND SAVED!")
    print("=" * 60)
    print("Models saved in app/ml/models/:")
    print("  clause_risk_v1.pkl")
    print("  label_encoder_v1.pkl")
    print("  doc_classifier_v1.pkl")
    print("  doc_label_encoder_v1.pkl")
    print("  metadata_v1.json")
    print(f"\nClause Risk Accuracy: {meta['accuracy']:.2%}")
    print(f"CV Score: {meta['cv_mean']:.2%} ± {meta['cv_std']:.2%}")
    print("\nNote: Production needs real labeled Indian legal documents.")
