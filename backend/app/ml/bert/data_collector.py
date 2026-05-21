"""
LawBridge AI — Indian Legal Data Collection Pipeline
=====================================================
Collects real Indian legal clauses from public sources
for model training and fine-tuning.

Sources:
1. IndiaKanoon (public judgments)
2. JUDIS (Supreme Court)
3. Legislative.gov.in (Acts and Bills)

Usage:
  python -m app.ml.bert.data_collector --source indiakanoon --limit 500
  python -m app.ml.bert.data_collector --source acts --limit 200

Output: app/ml/data/raw/clauses_raw.jsonl
"""
import os
import json
import time
import logging
import argparse
import re
from typing import List, Dict, Optional

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def extract_clauses_from_text(text: str, source_url: str = "") -> List[Dict]:
    """Extract individual clauses from a legal document text."""
    clauses = []

    # Split by common legal clause patterns
    patterns = [
        r'\n\s*(\d+[\.\)]\s+[A-Z][^.\n]{20,200}[.\n])',  # Numbered clauses
        r'\n\s*([A-Z][A-Z\s]{3,30}:\s+[^.\n]{20,200}[.\n])',  # HEADING: content
        r'(?<=[.!?])\s+(?=[A-Z][^.]{30,300}(?:shall|must|may|will|agrees|undertakes|warrants))',  # Obligation sentences
    ]

    # Simple paragraph extraction
    paragraphs = [p.strip() for p in text.split('\n\n') if len(p.strip()) > 50]

    for para in paragraphs[:50]:
        # Filter for clause-like content
        if any(kw in para.lower() for kw in [
            'shall', 'must', 'agrees', 'undertakes', 'warrants', 'represents',
            'terminate', 'notice', 'payment', 'confidential', 'liable', 'penalty'
        ]):
            clauses.append({
                "text": para[:500].strip(),
                "source": source_url,
                "labeled": False,
                "label": None
            })

    return clauses[:10]  # Max 10 clauses per document


def collect_from_sample_acts() -> List[Dict]:
    """
    Collect clauses from sample Indian Acts text.
    In production: fetch from https://legislative.gov.in/
    """
    # Sample clause text from publicly available Indian acts
    sample_clauses = [
        {
            "text": "Every employer shall pay to every employee employed by him wages at a rate not less than the minimum rate of wages fixed by the appropriate Government.",
            "source": "Minimum Wages Act, 1948",
            "labeled": True,
            "label": "low"
        },
        {
            "text": "No employer shall permit any worker to work in any factory for more than forty-eight hours in any week.",
            "source": "Factories Act, 1948",
            "labeled": True,
            "label": "low"
        },
        {
            "text": "An employer who fails to comply with any provision of this Act shall be punishable with imprisonment for a term which may extend to six months, or with fine which may extend to five hundred rupees, or with both.",
            "source": "Minimum Wages Act, 1948",
            "labeled": True,
            "label": "high"
        },
        {
            "text": "Where a gratuity becomes payable under this Act, the employer shall, whether an application has been made or not, determine the amount of gratuity and give notice thereof.",
            "source": "Payment of Gratuity Act, 1972",
            "labeled": True,
            "label": "medium"
        },
        {
            "text": "No person shall publish or cause to be published or arrange to be published, any information that is false or misleading in a material particular.",
            "source": "Consumer Protection Act, 2019",
            "labeled": True,
            "label": "high"
        },
        {
            "text": "Every establishment to which this Act applies shall maintain registers and records giving particulars of employees employed therein.",
            "source": "Shops and Establishments Act",
            "labeled": True,
            "label": "low"
        },
        {
            "text": "If any dispute arises between an employer and employee regarding any matter under this agreement, the parties shall first attempt to resolve the dispute through mutual negotiation.",
            "source": "Standard Employment Agreement",
            "labeled": True,
            "label": "low"
        },
        {
            "text": "The employee shall not, during the term of employment and for a period of two years thereafter, directly or indirectly solicit, induce, or attempt to induce any employee of the company to leave.",
            "source": "Sample Employment Contract",
            "labeled": True,
            "label": "high"
        },
        {
            "text": "In the event of non-payment of rent for a period exceeding two months, the landlord shall be entitled to terminate this agreement forthwith without any further notice.",
            "source": "Sample Rental Agreement",
            "labeled": True,
            "label": "high"
        },
        {
            "text": "The tenant shall use the premises only for residential purposes and shall not carry on any trade, business or profession therefrom.",
            "source": "Sample Rental Agreement",
            "labeled": True,
            "label": "medium"
        },
    ]
    return sample_clauses


def label_clause_interactively(clause: Dict) -> Dict:
    """Interactive labeling tool for legal clauses."""
    print("\n" + "=" * 60)
    print("CLAUSE TO LABEL:")
    print("-" * 60)
    print(clause['text'])
    print("-" * 60)
    print("Source:", clause.get('source', 'Unknown'))
    print("\nLabel options:")
    print("  1 = critical (criminal action, FIR, arrest)")
    print("  2 = high (termination without cause, non-compete, bond)")
    print("  3 = medium (lock-in, notice period, arbitration)")
    print("  4 = low (standard terms, renewal, governing law)")
    print("  s = skip this clause")
    print("  q = quit labeling")

    while True:
        choice = input("\nYour label (1/2/3/4/s/q): ").strip().lower()
        if choice == '1':
            clause['label'] = 'critical'
            clause['labeled'] = True
            break
        elif choice == '2':
            clause['label'] = 'high'
            clause['labeled'] = True
            break
        elif choice == '3':
            clause['label'] = 'medium'
            clause['labeled'] = True
            break
        elif choice == '4':
            clause['label'] = 'low'
            clause['labeled'] = True
            break
        elif choice == 's':
            break
        elif choice == 'q':
            clause['label'] = 'QUIT'
            break
        else:
            print("Invalid choice. Enter 1, 2, 3, 4, s, or q")

    return clause


def save_clauses(clauses: List[Dict], output_path: str):
    """Save collected clauses to JSONL file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        for clause in clauses:
            f.write(json.dumps(clause, ensure_ascii=False) + '\n')
    logger.info(f"Saved {len(clauses)} clauses to {output_path}")


def load_clauses(input_path: str) -> List[Dict]:
    """Load clauses from JSONL file."""
    clauses = []
    if not os.path.exists(input_path):
        return clauses
    with open(input_path) as f:
        for line in f:
            if line.strip():
                clauses.append(json.loads(line))
    return clauses


def run_labeling_session(input_path: str, output_path: str):
    """Run interactive labeling session on collected clauses."""
    clauses = load_clauses(input_path)
    unlabeled = [c for c in clauses if not c.get('labeled')]

    print(f"\n📋 Labeling Session")
    print(f"Total clauses: {len(clauses)}")
    print(f"Already labeled: {len(clauses) - len(unlabeled)}")
    print(f"To label: {len(unlabeled)}")
    print("\nPress Enter to start labeling...")
    input()

    labeled_count = 0
    for clause in unlabeled:
        clause = label_clause_interactively(clause)
        if clause.get('label') == 'QUIT':
            break
        if clause.get('labeled'):
            labeled_count += 1

    all_labeled = [c for c in clauses if c.get('labeled')]
    save_clauses(clauses, output_path)
    print(f"\n✅ Labeled {labeled_count} new clauses")
    print(f"Total labeled clauses: {len(all_labeled)}")

    # Show distribution
    from collections import Counter
    labels = [c['label'] for c in all_labeled]
    dist = Counter(labels)
    print("\nLabel distribution:")
    for label, count in dist.most_common():
        print(f"  {label}: {count}")


def generate_training_file(labeled_path: str, output_path: str):
    """Convert labeled JSONL to Python training data format."""
    clauses = [c for c in load_clauses(labeled_path) if c.get('labeled') and c.get('label')]

    print(f"\n📊 Generating training file from {len(clauses)} labeled clauses...")

    training_lines = ['LABELED_CLAUSES = [']
    for c in clauses:
        text = c['text'].replace('"', '\\"').replace('\n', ' ')
        training_lines.append(f'    ("{text}", "{c["label"]}"),')
    training_lines.append(']')

    with open(output_path, 'w') as f:
        f.write('\n'.join(training_lines))

    print(f"✅ Training data saved to {output_path}")
    print(f"💡 Copy LABELED_CLAUSES into finetune.py and retrain!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="LawBridge AI Data Collection")
    parser.add_argument("--action", choices=["collect", "label", "export"],
                        default="collect", help="Action to perform")
    parser.add_argument("--limit", type=int, default=100, help="Max clauses to collect")
    args = parser.parse_args()

    RAW_PATH = "app/ml/data/raw/clauses_raw.jsonl"
    LABELED_PATH = "app/ml/data/labeled/clauses_labeled.jsonl"
    EXPORT_PATH = "app/ml/data/processed/training_data.py"

    if args.action == "collect":
        print("📥 Collecting sample Indian legal clauses...")
        clauses = collect_from_sample_acts()
        save_clauses(clauses, RAW_PATH)
        print(f"✅ Collected {len(clauses)} clauses")
        print(f"📁 Saved to: {RAW_PATH}")
        print(f"\n💡 Next steps:")
        print(f"  1. Run with --action label to label unlabeled clauses")
        print(f"  2. Add more clauses from IndiaKanoon manually")
        print(f"  3. Run with --action export to generate training data")

    elif args.action == "label":
        import shutil
        if not os.path.exists(RAW_PATH):
            print("No raw clauses found. Run --action collect first.")
        else:
            if not os.path.exists(LABELED_PATH):
                shutil.copy(RAW_PATH, LABELED_PATH)
            run_labeling_session(LABELED_PATH, LABELED_PATH)

    elif args.action == "export":
        if not os.path.exists(LABELED_PATH):
            print("No labeled clauses found. Run --action label first.")
        else:
            generate_training_file(LABELED_PATH, EXPORT_PATH)
