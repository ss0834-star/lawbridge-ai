from typing import List, Dict

INDIA_STATES = ["Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan","Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal","Delhi","Chandigarh","Puducherry"]

STATE_CHECKLISTS = {
    "Tamil Nadu": {
        "Rental Agreement": ["Register agreement if rent period > 11 months (mandatory in TN)","Stamp paper value: 1% of total rent + deposit","Police verification required in Chennai, Coimbatore","Check Model Tenancy Act 2021 provisions","Verify property tax receipts are current","Consider registered agreement for better legal protection"],
        "Employment Contract": ["Tamil Nadu Shops and Establishments Act applies to most employers","Verify PF/ESI deductions as per law","Non-compete clauses have limited enforceability in India","Check Gratuity eligibility after 5 years","Right to Form 16 for income tax purposes"],
    },
    "Maharashtra": {
        "Rental Agreement": ["E-registration mandatory for agreements > 12 months","Stamp duty: 0.25% of total annual rent","Police verification required in Mumbai/Pune","Check Maharashtra Rent Control Act applicability","Society NOC may be required","Leave and License agreement is preferred format"],
        "Employment Contract": ["Maharashtra Shops and Establishments Act applies","MLWF (Maharashtra Labour Welfare Fund) contribution required","Check Profession Tax deductions","Non-solicitation clauses are more enforceable than non-compete"],
    },
    "Karnataka": {
        "Rental Agreement": ["Registration mandatory if rent period > 12 months","Stamp duty: 0.5% of annual rent","Verify BBMP property tax clearance","Check BDA/BBMP regulations for the property","Karnataka Rent Act may apply in some areas"],
        "Employment Contract": ["Karnataka Shops and Establishments Act","Check Profession Tax slab for your salary","IT companies in Karnataka often have stricter IP clauses","Moonlighting policy may be stricter in IT sector"],
    },
    "default": {
        "Rental Agreement": ["Verify stamp paper value with local Sub-Registrar","Register agreement if period exceeds 11 months","Police verification may be required in your city","Keep original agreement in safe custody","Verify property ownership documents before signing","Clarify maintenance, utility, and parking responsibilities in writing"],
        "Employment Contract": ["Verify company is legitimately registered","Get appointment letter before joining","Understand PF/ESI deduction policy","Verify gratuity eligibility (5+ years)","Get Form 16 annually for tax","Non-compete clauses have limited enforceability in India"],
        "NDA": ["Check jurisdiction clause — prefer your local court","Ensure standard exceptions are included (publicly known info)","Request a reasonable time limit on confidentiality","Understand exactly what information is considered confidential","Data return/deletion clause is important"],
        "Legal Notice": ["Do not ignore any legal notice","Respond within the deadline specified","Consult a lawyer before responding to any legal notice","Keep a copy of the notice and any response","Send response by registered post with acknowledgment due"],
    }
}

LEGAL_AID_DATA = [
    {"name": "National Legal Services Authority (NALSA)", "resource_type": "Legal Aid Authority", "city": "New Delhi", "state": "Delhi", "address": "12/11, Jam Nagar House, Shahjahan Road, New Delhi - 110011", "phone": "011-23388922 / 15100", "website": "nalsa.gov.in", "description": "Free legal services for eligible citizens including SC/ST, women, children, persons with disabilities, industrial workmen, and those below poverty line.", "is_free": True},
    {"name": "Tamil Nadu State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Chennai", "state": "Tamil Nadu", "address": "High Court Buildings, Chennai - 600 104", "phone": "044-25213521", "website": "tnsla.tn.gov.in", "description": "Free legal aid for Tamil Nadu residents. Walk-in or call for appointment.", "is_free": True},
    {"name": "Maharashtra State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Mumbai", "state": "Maharashtra", "address": "Old Secretariat Building, Fort, Mumbai - 400 032", "phone": "022-22620711", "website": "msla.gov.in", "description": "Free legal services for eligible Maharashtra residents.", "is_free": True},
    {"name": "Karnataka State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Bengaluru", "state": "Karnataka", "address": "High Court Building, Bengaluru - 560 001", "phone": "080-22113170", "website": "kslsa.kar.nic.in", "description": "Free legal aid for Karnataka residents. District-level services available.", "is_free": True},
    {"name": "Delhi State Legal Services Authority", "resource_type": "State Legal Aid", "city": "New Delhi", "state": "Delhi", "address": "Central District, Tis Hazari Courts Complex, Delhi - 110054", "phone": "011-23917914", "website": "dslsa.org", "description": "Free legal services for Delhi residents. Multiple Lok Adalat centres.", "is_free": True},
    {"name": "Telangana State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Hyderabad", "state": "Telangana", "address": "High Court Buildings, Hyderabad - 500 001", "phone": "040-23447083", "website": "tslsa.org", "description": "Free legal aid for Telangana residents.", "is_free": True},
    {"name": "Gujarat State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Ahmedabad", "state": "Gujarat", "address": "Gujarat High Court, Sola, Ahmedabad - 380 060", "phone": "079-27560950", "website": "gujaratslsa.org", "description": "Free legal services for eligible Gujarat residents.", "is_free": True},
    {"name": "Rajasthan State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Jaipur", "state": "Rajasthan", "address": "High Court Premises, Jodhpur - 342 001", "phone": "0291-2545212", "website": "rlsa.gov.in", "description": "Free legal aid for Rajasthan residents.", "is_free": True},
]

KNOW_YOUR_RIGHTS = {
    "tenant": {
        "title": "Tenant Rights in India",
        "icon": "🏠",
        "color": "forest",
        "rights": [
            {"title": "Right to a Written Agreement", "description": "You have the right to a written rental agreement before moving in. Never pay deposit or rent without a written agreement.", "law": "Transfer of Property Act, 1882"},
            {"title": "Security Deposit Protection", "description": "Your deposit must be refunded within 30-60 days of vacating (after deducting legitimate costs). Landlord cannot withhold it without written reason.", "law": "State Rent Control Acts"},
            {"title": "Notice Before Eviction", "description": "Landlord cannot evict you without giving proper notice as specified in your agreement (typically 1-3 months). Emergency eviction without notice is illegal.", "law": "Transfer of Property Act + State Rent Control Acts"},
            {"title": "Right to Peaceful Enjoyment", "description": "Landlord cannot enter your home without prior notice except in genuine emergencies. You have the right to privacy in your rented home.", "law": "Common Law + ICA 1872"},
            {"title": "Receipt for All Payments", "description": "You are entitled to a written receipt for every rent payment, deposit, and maintenance charge paid.", "law": "Payment of Wages Act"},
            {"title": "Habitable Condition", "description": "The property must be in a reasonably habitable condition. Major structural repairs are typically the landlord's responsibility.", "law": "Transfer of Property Act, 1882"},
        ]
    },
    "employee": {
        "title": "Employee Rights in India",
        "icon": "💼",
        "color": "navy",
        "rights": [
            {"title": "Right to Written Appointment Letter", "description": "Every employee is entitled to a written appointment letter stating designation, salary, and key terms before joining.", "law": "Shops & Establishments Acts (state-wise)"},
            {"title": "Timely Salary Payment", "description": "Wages must be paid by the 7th of the following month (10th for companies with >1000 employees). Unlawful to withhold salary.", "law": "Payment of Wages Act, 1936"},
            {"title": "Notice Period Rights", "description": "Both parties must give contractual notice before termination. Employer cannot dismiss without proper notice or payment in lieu.", "law": "Industrial Disputes Act, 1947"},
            {"title": "Gratuity After 5 Years", "description": "After 5 years of continuous service, you are entitled to gratuity = 15 days salary × years of service.", "law": "Payment of Gratuity Act, 1972"},
            {"title": "PF & ESI Contributions", "description": "Employer must deposit your PF contribution + equal employer contribution. ESI for employees earning below threshold.", "law": "EPF Act 1952 + ESI Act 1948"},
            {"title": "Maternity Leave", "description": "26 weeks paid maternity leave for first two children. 12 weeks for third child onwards. Applies to establishments with 10+ employees.", "law": "Maternity Benefit Act, 1961 (amended 2017)"},
            {"title": "Protection from Harassment", "description": "Right to a safe workplace free from sexual harassment. Every employer with 10+ employees must have an Internal Complaints Committee.", "law": "POSH Act, 2013"},
        ]
    },
    "consumer": {
        "title": "Consumer Rights in India",
        "icon": "🛒",
        "color": "gold",
        "rights": [
            {"title": "Right to Safety", "description": "Protection against goods and services that are hazardous to life and property. You can demand compensation for any harm caused.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Information", "description": "Right to complete information about the quality, quantity, potency, purity, standard, and price of goods or services.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Choose", "description": "Access to a variety of goods/services at competitive prices. Monopolistic trade practices are illegal.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to be Heard", "description": "Your complaints must be considered by consumer forums. You can file against any seller, service provider, or e-commerce platform.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Seek Redressal", "description": "You can claim compensation for defective goods, deficient services, unfair trade practices. District forum handles claims up to ₹1 crore.", "law": "Consumer Protection Act, 2019"},
            {"title": "E-Commerce Rights", "description": "Online sellers must display return policy, delivery timeline, seller details. You can demand refund for defective products within return window.", "law": "Consumer Protection (E-Commerce) Rules, 2020"},
        ]
    },
    "digital": {
        "title": "Digital & Privacy Rights",
        "icon": "🔐",
        "color": "burgundy",
        "rights": [
            {"title": "Right to Privacy Online", "description": "Your personal data cannot be collected without consent. Companies must disclose what data they collect and how it is used.", "law": "Digital Personal Data Protection Act, 2023"},
            {"title": "Right to Data Erasure", "description": "You can request deletion of your personal data from platforms and companies subject to certain conditions.", "law": "DPDPA 2023"},
            {"title": "Protection from Cybercrime", "description": "Identity theft, phishing, online fraud, cyberstalking are criminal offences. File complaint at cybercrime.gov.in or local police.", "law": "IT Act, 2000"},
            {"title": "Right Against Fake News / Defamation", "description": "Publishing false information about you is actionable. Defamation online is covered under both criminal and civil law.", "law": "IPC + IT Act, 2000"},
            {"title": "Social Media Account Protection", "description": "Hacking, impersonation, and unauthorized access to social media accounts are criminal offences under the IT Act.", "law": "IT Act, 2000 (Section 66C, 66D)"},
        ]
    },
}


def get_checklist(state: str, doc_type: str) -> List[str]:
    state_checklists = STATE_CHECKLISTS.get(state, STATE_CHECKLISTS["default"])
    return state_checklists.get(doc_type, STATE_CHECKLISTS["default"].get(doc_type, [f"Consult a local lawyer in {state} for state-specific requirements", "Verify document registration requirements with local Sub-Registrar", "Keep copies of all signed documents safely"]))


def get_resources_by_state(state: str) -> List[Dict]:
    state_resources = [r for r in LEGAL_AID_DATA if r["state"] == state]
    nalsa = next((r for r in LEGAL_AID_DATA if "NALSA" in r["name"]), None)
    if nalsa and nalsa not in state_resources:
        state_resources = [nalsa] + state_resources
    return state_resources or [LEGAL_AID_DATA[0]]
