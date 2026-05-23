from typing import List, Dict

INDIA_STATES = [
    "Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chhattisgarh","Goa","Gujarat",
    "Haryana","Himachal Pradesh","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
    "Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
    "Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
    "Delhi","Chandigarh","Puducherry","Jammu & Kashmir","Ladakh","Andaman & Nicobar Islands",
    "Dadra & Nagar Haveli","Daman & Diu","Lakshadweep"
]

# All 10 doc types covered in default — states override only where rules differ
DEFAULT_CHECKLISTS = {
    "Rental Agreement": [
        "Verify stamp paper value with local Sub-Registrar",
        "Register agreement if period exceeds 11 months",
        "Police verification may be required in your city",
        "Keep original agreement in safe custody",
        "Verify property ownership documents before signing",
        "Clarify maintenance, utility, and parking responsibilities in writing",
    ],
    "Employment Contract": [
        "Verify company is legitimately registered (check MCA21)",
        "Get appointment letter before joining — do not join without one",
        "Understand PF/ESI deduction policy clearly",
        "Verify gratuity eligibility (5+ years continuous service)",
        "Get Form 16 annually for income tax filing",
        "Non-compete clauses have limited enforceability in India",
        "Moonlighting clauses — understand restrictions clearly",
    ],
    "NDA": [
        "Check jurisdiction clause — prefer your local court",
        "Ensure standard exceptions are included (publicly known info, independently developed)",
        "Request a reasonable time limit on confidentiality (1-3 years is standard)",
        "Understand exactly what information is considered confidential",
        "Data return/deletion clause is important — insist on it",
        "Mutual vs one-sided NDA — negotiate if possible",
        "Unilateral NDAs heavily favour the disclosing party — read carefully",
    ],
    "Service Agreement": [
        "Define scope of work clearly — vague scope leads to disputes",
        "Include payment milestones and timelines explicitly",
        "Specify deliverables with measurable acceptance criteria",
        "Add penalty/SLA clause for delays or non-performance",
        "Include termination clause with notice period",
        "IP ownership clause — who owns work product?",
        "Dispute resolution mechanism — arbitration preferred over litigation",
        "Governing law and jurisdiction clause — prefer your state",
    ],
    "Loan Document": [
        "Verify lender is RBI-registered (for institutional loans)",
        "Check for hidden processing fees, prepayment charges",
        "Understand EMI breakup — principal vs interest",
        "Foreclosure charges must be disclosed upfront",
        "Get loan agreement copy before signing — never sign blank documents",
        "CIBIL score impact — understand how defaults affect credit score",
        "Collateral/security details must be clearly documented",
        "For personal loans between individuals — register the agreement",
    ],
    "Legal Notice": [
        "Do not ignore any legal notice — ignoring is not a safe option",
        "Respond within the deadline specified in the notice",
        "Consult a lawyer before drafting any response",
        "Keep a copy of the notice and your response",
        "Send response by registered post with acknowledgment due (RPAD)",
        "Note the limitation period — some claims have strict deadlines",
        "A legal notice is often a precursor to court proceedings",
    ],
    "Business Agreement": [
        "Clearly define roles, responsibilities, and profit-sharing",
        "Include exit clause — what happens if a partner wants to leave",
        "Dispute resolution: arbitration is faster than civil courts",
        "IP ownership and non-compete between partners must be explicit",
        "Governing law and jurisdiction — prefer your home state",
        "Register the agreement if it involves property or significant assets",
        "Consider stamping even if not mandatory — adds evidentiary value",
    ],
    "Freelance Contract": [
        "Define deliverables and timelines precisely — avoid vague scope",
        "Payment terms: milestone-based preferred over lump-sum at end",
        "IP/copyright clause — ownership of created work must be explicit",
        "Revision policy — how many revisions are included?",
        "Kill fee clause — payment if client cancels mid-project",
        "Non-disclosure obligations if handling client data",
        "Invoice and GST compliance if your turnover exceeds threshold",
        "Dispute resolution — arbitration clause saves time and cost",
    ],
    "Property Document": [
        "Verify title chain for last 30 years minimum",
        "Check for encumbrances at Sub-Registrar office (EC certificate)",
        "Verify property tax receipts are up to date",
        "Check for any pending court cases on the property",
        "Ensure mutation/khata is in seller's name",
        "Get legal opinion from a property lawyer before purchase",
        "Check RERA registration for under-construction properties",
        "Verify approved building plan from local municipal authority",
        "Power of Attorney transactions — verify PA is valid and registered",
    ],
    "General Agreement": [
        "Ensure all parties are clearly identified with full legal names",
        "Consideration (payment/exchange) must be mentioned",
        "Effective date and duration of agreement must be stated",
        "Include termination clause with clear notice requirements",
        "Dispute resolution mechanism — arbitration preferred",
        "Governing law and jurisdiction clause",
        "Both parties must sign — witness signatures add strength",
        "Stamp the agreement as per your state's Stamp Act",
    ],
}

STATE_CHECKLISTS = {
    "Tamil Nadu": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement if rent period > 11 months (mandatory in TN)",
            "Stamp paper value: 1% of total rent + deposit",
            "Police verification required in Chennai and Coimbatore",
            "Check Model Tenancy Act 2021 provisions",
            "Verify property tax receipts are current",
            "Consider registered agreement for better legal protection",
        ],
        "Employment Contract": [
            "Tamil Nadu Shops and Establishments Act applies to most employers",
            "Verify PF/ESI deductions as per law",
            "Non-compete clauses have limited enforceability in India",
            "Check Gratuity eligibility after 5 years",
            "Right to Form 16 for income tax purposes",
        ],
        "Property Document": [
            "Verify patta and chitta documents (TN-specific land records)",
            "Check encumbrance certificate at Sub-Registrar office",
            "Verify property tax receipts with local municipality",
            "TNRERA registration mandatory for projects > 500 sqm or 8 units",
            "Check for any Wakf board claims on the property",
            "Verify approved plan from CMDA/DTCP",
        ],
    },
    "Maharashtra": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "E-registration mandatory for agreements > 12 months",
            "Stamp duty: 0.25% of total annual rent",
            "Police verification required in Mumbai/Pune",
            "Check Maharashtra Rent Control Act applicability",
            "Society NOC may be required",
            "Leave and License agreement is the preferred format in Maharashtra",
        ],
        "Employment Contract": [
            "Maharashtra Shops and Establishments Act applies",
            "MLWF (Maharashtra Labour Welfare Fund) contribution required",
            "Check Profession Tax deductions (PT slab varies by salary)",
            "Non-solicitation clauses are more enforceable than non-compete",
        ],
        "Property Document": [
            "Check 7/12 extract (Satbara) for agricultural land",
            "MahaRERA registration mandatory for new projects",
            "Verify Index II from Sub-Registrar for previous transactions",
            "Check for NA (Non-Agricultural) conversion order if needed",
            "Society share certificate must be transferred in your name",
            "Occupation Certificate (OC) mandatory before moving in",
        ],
    },
    "Karnataka": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Registration mandatory if rent period > 12 months",
            "Stamp duty: 0.5% of annual rent",
            "Verify BBMP property tax clearance",
            "Check BDA/BBMP regulations for the property",
            "Karnataka Rent Act may apply in some areas",
        ],
        "Employment Contract": [
            "Karnataka Shops and Establishments Act",
            "Check Profession Tax slab for your salary",
            "IT companies in Karnataka often have stricter IP clauses",
            "Moonlighting policy may be stricter in IT sector",
        ],
        "Property Document": [
            "Verify Khata certificate and extract from BBMP/Gram Panchayat",
            "Check RTC (Record of Rights) for agricultural land",
            "KRERA registration for new residential projects",
            "Verify BDA/BBMP approved building plan",
            "Check for B-Khata vs A-Khata — A-Khata preferred",
            "DC conversion certificate required for converted land",
        ],
    },
    "Delhi": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Delhi Rent Control Act applies to older properties (rent < ₹3,500)",
            "Register agreement if rent > ₹3,500/month and period > 12 months",
            "Stamp duty: 2% of annual rent",
            "Police verification mandatory",
            "E-stamping available at Sub-Registrar offices",
        ],
        "Property Document": [
            "Verify property in DDA/MCD records",
            "Check for unauthorized construction — DDA seal risk",
            "Power of Attorney sale — verify carefully, often problematic in Delhi",
            "Check circle rate vs market rate for stamp duty calculation",
            "Verify no encroachment on public land",
        ],
    },
    "West Bengal": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "West Bengal Tenancy Act applies",
            "Register agreement at local Sub-Registrar",
            "Stamp duty: 1% of annual rent",
            "Police verification required in Kolkata",
            "Khata/mutation documents important",
        ],
        "Property Document": [
            "Verify Khatian and plot number in West Bengal land records",
            "Check mutation certificate in seller's name",
            "WBHIRA registration for housing projects",
            "Verify conversion status for agricultural land",
            "Check for any Wakf or Trust claims",
        ],
    },
    "Gujarat": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement if period > 11 months",
            "Stamp duty: 1.5% of total rent",
            "E-registration available in major cities",
            "Police verification in Ahmedabad/Surat mandatory",
            "Gujarat Tenancy Act provisions apply",
        ],
        "Property Document": [
            "Verify 7/12 extract for land ownership",
            "GujRERA registration for new projects",
            "Check for Gamtal land restrictions",
            "Verify NA permission for non-agricultural use",
            "Check JantriRates (government valuation) for stamp duty",
        ],
    },
    "Telangana": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement if period > 11 months",
            "Stamp duty: 0.5% of average annual rent",
            "E-registration available via IGRS Telangana",
            "Police verification required in Hyderabad",
        ],
        "Property Document": [
            "Verify Pattadar Passbook and Title Deed",
            "Check Dharani portal for land records",
            "TSRERA registration for new projects",
            "Verify layout approval from HMDA/DTCP",
            "Check for any GO 111 restrictions near Hyderabad lakes",
        ],
    },
    "Andhra Pradesh": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement if period > 11 months",
            "Stamp duty: 0.5% of average annual rent",
            "E-registration available via IGRS AP",
            "Police verification required in major cities",
        ],
        "Property Document": [
            "Verify Pattadar Passbook",
            "Check AP land records portal (Meebhoomi)",
            "APRERA registration for new projects",
            "Verify layout approval from CRDA/VMRDA",
        ],
    },
    "Kerala": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Kerala Buildings (Lease & Rent Control) Act applies",
            "Register agreement at Sub-Registrar",
            "Stamp duty: 1% of annual rent",
            "Police verification in Thiruvananthapuram/Kochi",
        ],
        "Property Document": [
            "Verify Thandaper (ownership record) in Kerala land records",
            "Check for any restrictions under Kerala Land Reforms Act",
            "K-RERA registration for new projects",
            "Verify building permit from local body (Panchayat/Municipality)",
            "Check for coastal regulation zone (CRZ) restrictions",
        ],
    },
    "Rajasthan": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement at Sub-Registrar office",
            "Stamp duty: 1% of annual rent",
            "Police verification required in Jaipur",
            "Verify property ownership with Rajasthan land records (Apna Khata)",
        ],
        "Property Document": [
            "Verify Jamabandi (ownership record) on Apna Khata portal",
            "RERA Rajasthan registration for new projects",
            "Check for Nazul land restrictions in urban areas",
            "Verify approved map from JDA/local UIT",
        ],
    },
    "Uttar Pradesh": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "UP Urban Buildings (Regulation of Letting) Act applies in notified areas",
            "Register agreement at Sub-Registrar",
            "Stamp duty: 2% of annual rent",
            "Police verification required in Lucknow/Noida/Agra",
        ],
        "Property Document": [
            "Verify Khatauni on UP Bhulekh portal",
            "UP RERA registration for new projects",
            "Check for any Gram Sabha land issues",
            "Verify mutation in seller's name at Tehsil office",
            "Registry must be done at Sub-Registrar — Power of Attorney sales are risky",
        ],
    },
    "Punjab": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "East Punjab Urban Rent Restriction Act applies",
            "Register agreement at Sub-Registrar",
            "Stamp duty: 1% of annual rent",
            "Verify property ownership with Punjab land records",
            "Police verification in Chandigarh/Ludhiana",
        ],
    },
    "Haryana": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Haryana Urban (Control of Rent and Eviction) Act applies",
            "Register agreement at Sub-Registrar",
            "Stamp duty: 1.5% of annual rent",
            "Police verification in Gurugram/Faridabad mandatory",
        ],
        "Property Document": [
            "Verify Jamabandi on Haryana Bhulekh portal",
            "HRERA registration for new projects",
            "Check for CLU (Change of Land Use) permission",
            "Verify approved plan from DGTCP/Municipal Corporation",
            "Check for Lal Dora land restrictions",
        ],
    },
    "Madhya Pradesh": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Register agreement at Sub-Registrar office",
            "Stamp duty: 1% of annual rent",
            "Verify property ownership documents",
            "Police verification in Bhopal/Indore",
        ],
    },
    "Puducherry": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Puducherry Buildings (Lease and Rent Control) Act applies",
            "Register agreement if period > 11 months",
            "Stamp duty: 1% of annual rent",
            "Both Tamil Nadu and Puducherry rules may apply near borders",
        ],
    },
    "Jammu & Kashmir": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "J&K Rent Act 1995 applies",
            "Register agreement at Sub-Registrar",
            "Property laws changed after Article 370 — verify current status",
            "Police verification in Jammu/Srinagar",
        ],
    },
    "Goa": {
        **DEFAULT_CHECKLISTS,
        "Rental Agreement": [
            "Goa Buildings (Lease, Rent and Eviction) Control Act applies",
            "Register agreement at Sub-Registrar",
            "Stamp duty: 0.5% of annual rent",
            "Verify property is not under Portuguese Civil Code restrictions",
        ],
        "Property Document": [
            "Verify Form I & XIV (Goa land record equivalent)",
            "Check Communidade land status — some land has community ownership",
            "Portuguese Civil Code applies to inheritance — affects ownership",
            "RERA Goa registration for new projects",
            "Verify no ODP (Outline Development Plan) restrictions",
        ],
    },
}


LEGAL_AID_DATA = [
    {"name": "National Legal Services Authority (NALSA)", "resource_type": "National Legal Aid", "city": "New Delhi", "state": "Delhi", "address": "12/11, Jam Nagar House, Shahjahan Road, New Delhi - 110011", "phone": "011-23388922 / 15100", "website": "nalsa.gov.in", "description": "Free legal services for SC/ST, women, children, persons with disabilities, industrial workmen, and those below poverty line.", "is_free": True},
    {"name": "Tamil Nadu State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Chennai", "state": "Tamil Nadu", "address": "High Court Buildings, Chennai - 600 104", "phone": "044-25213521", "website": "tnsla.tn.gov.in", "description": "Free legal aid for Tamil Nadu residents. Walk-in or call for appointment.", "is_free": True},
    {"name": "Maharashtra State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Mumbai", "state": "Maharashtra", "address": "Old Secretariat Building, Fort, Mumbai - 400 032", "phone": "022-22620711", "website": "msla.gov.in", "description": "Free legal services for eligible Maharashtra residents.", "is_free": True},
    {"name": "Karnataka State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Bengaluru", "state": "Karnataka", "address": "High Court Building, Bengaluru - 560 001", "phone": "080-22113170", "website": "kslsa.kar.nic.in", "description": "Free legal aid for Karnataka residents. District-level services available.", "is_free": True},
    {"name": "Delhi State Legal Services Authority", "resource_type": "State Legal Aid", "city": "New Delhi", "state": "Delhi", "address": "Central District, Tis Hazari Courts Complex, Delhi - 110054", "phone": "011-23917914", "website": "dslsa.org", "description": "Free legal services for Delhi residents. Multiple Lok Adalat centres.", "is_free": True},
    {"name": "Telangana State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Hyderabad", "state": "Telangana", "address": "High Court Buildings, Hyderabad - 500 001", "phone": "040-23447083", "website": "tslsa.org", "description": "Free legal aid for Telangana residents.", "is_free": True},
    {"name": "Gujarat State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Ahmedabad", "state": "Gujarat", "address": "Gujarat High Court, Sola, Ahmedabad - 380 060", "phone": "079-27560950", "website": "gujaratslsa.org", "description": "Free legal services for eligible Gujarat residents.", "is_free": True},
    {"name": "Rajasthan State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Jaipur", "state": "Rajasthan", "address": "High Court Premises, Jodhpur - 342 001", "phone": "0291-2545212", "website": "rlsa.gov.in", "description": "Free legal aid for Rajasthan residents.", "is_free": True},
    {"name": "West Bengal State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Kolkata", "state": "West Bengal", "address": "Calcutta High Court Centenary Building, Kolkata - 700 001", "phone": "033-22454483", "website": "wbslsa.org", "description": "Free legal aid for West Bengal residents.", "is_free": True},
    {"name": "Kerala State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Ernakulam", "state": "Kerala", "address": "High Court Buildings, Ernakulam - 682 031", "phone": "0484-2562252", "website": "kelslsa.org", "description": "Free legal aid for Kerala residents.", "is_free": True},
    {"name": "Andhra Pradesh State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Amaravati", "state": "Andhra Pradesh", "address": "High Court of Andhra Pradesh, Amaravati", "phone": "0863-2340901", "website": "apslsa.org", "description": "Free legal aid for Andhra Pradesh residents.", "is_free": True},
    {"name": "Madhya Pradesh State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Jabalpur", "state": "Madhya Pradesh", "address": "High Court of MP, Jabalpur - 482 001", "phone": "0761-2621366", "website": "mpslsa.org", "description": "Free legal aid for Madhya Pradesh residents.", "is_free": True},
    {"name": "Uttar Pradesh State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Lucknow", "state": "Uttar Pradesh", "address": "Lucknow Bench, High Court, Lucknow - 226 001", "phone": "0522-2209754", "website": "upslsa.org", "description": "Free legal aid for Uttar Pradesh residents.", "is_free": True},
    {"name": "Punjab State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Chandigarh", "state": "Punjab", "address": "Punjab & Haryana High Court, Chandigarh - 160 001", "phone": "0172-2748882", "website": "slsapunjab.org", "description": "Free legal aid for Punjab residents.", "is_free": True},
    {"name": "Haryana State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Chandigarh", "state": "Haryana", "address": "Punjab & Haryana High Court, Chandigarh - 160 001", "phone": "0172-2748490", "website": "haryanslsa.org", "description": "Free legal aid for Haryana residents.", "is_free": True},
    {"name": "Odisha State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Cuttack", "state": "Odisha", "address": "Orissa High Court, Cuttack - 753 002", "phone": "0671-2304856", "website": "orissa.gov.in/slsa", "description": "Free legal aid for Odisha residents.", "is_free": True},
    {"name": "Assam State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Guwahati", "state": "Assam", "address": "Gauhati High Court Campus, Guwahati - 781 001", "phone": "0361-2735026", "website": "assamslsa.org", "description": "Free legal aid for Assam residents.", "is_free": True},
    {"name": "Himachal Pradesh State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Shimla", "state": "Himachal Pradesh", "address": "HP High Court, Shimla - 171 001", "phone": "0177-2623537", "website": "hpslsa.nic.in", "description": "Free legal aid for Himachal Pradesh residents.", "is_free": True},
    {"name": "Uttarakhand State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Nainital", "state": "Uttarakhand", "address": "Uttarakhand High Court, Nainital - 263 001", "phone": "05942-235430", "website": "ukslsa.uk.gov.in", "description": "Free legal aid for Uttarakhand residents.", "is_free": True},
    {"name": "Bihar State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Patna", "state": "Bihar", "address": "Patna High Court, Patna - 800 001", "phone": "0612-2215247", "website": "bslsa.bih.nic.in", "description": "Free legal aid for Bihar residents.", "is_free": True},
    {"name": "Jharkhand State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Ranchi", "state": "Jharkhand", "address": "Jharkhand High Court, Ranchi - 834 002", "phone": "0651-2482093", "website": "jharkhandhighcourt.nic.in", "description": "Free legal aid for Jharkhand residents.", "is_free": True},
    {"name": "Chhattisgarh State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Bilaspur", "state": "Chhattisgarh", "address": "Chhattisgarh High Court, Bilaspur - 495 001", "phone": "07752-241349", "website": "cgslsa.gov.in", "description": "Free legal aid for Chhattisgarh residents.", "is_free": True},
    {"name": "Goa State Legal Services Authority", "resource_type": "State Legal Aid", "city": "Panaji", "state": "Goa", "address": "Bombay High Court Bench, Panaji, Goa - 403 001", "phone": "0832-2224958", "website": "goaslsa.gov.in", "description": "Free legal aid for Goa residents.", "is_free": True},
    {"name": "Chandigarh Legal Services Authority", "resource_type": "UT Legal Aid", "city": "Chandigarh", "state": "Chandigarh", "address": "District Courts Complex, Sector 43, Chandigarh - 160 036", "phone": "0172-2665015", "website": "chandigarhlsa.gov.in", "description": "Free legal aid for Chandigarh UT residents.", "is_free": True},
    {"name": "Puducherry State Legal Services Authority", "resource_type": "UT Legal Aid", "city": "Puducherry", "state": "Puducherry", "address": "Sessions Court Complex, Puducherry - 605 001", "phone": "0413-2220283", "website": "pondicherry.gov.in", "description": "Free legal aid for Puducherry residents.", "is_free": True},
    {"name": "Jammu & Kashmir Legal Services Authority", "resource_type": "UT Legal Aid", "city": "Srinagar", "state": "Jammu & Kashmir", "address": "J&K High Court Complex, Srinagar", "phone": "0194-2452354", "website": "jkhcsl.nic.in", "description": "Free legal aid for J&K residents.", "is_free": True},
]

KNOW_YOUR_RIGHTS = {
    "tenant": {
        "title": "Tenant Rights in India", "icon": "🏠", "color": "forest",
        "rights": [
            {"title": "Right to a Written Agreement", "description": "You have the right to a written rental agreement before moving in. Never pay deposit or rent without a written agreement.", "law": "Transfer of Property Act, 1882"},
            {"title": "Security Deposit Protection", "description": "Your deposit must be refunded within 30-60 days of vacating (after deducting legitimate costs). Landlord cannot withhold it without written reason.", "law": "State Rent Control Acts"},
            {"title": "Notice Before Eviction", "description": "Landlord cannot evict you without giving proper notice (typically 1-3 months). Emergency eviction without notice is illegal.", "law": "Transfer of Property Act + State Rent Control Acts"},
            {"title": "Right to Peaceful Enjoyment", "description": "Landlord cannot enter your home without prior notice except in genuine emergencies.", "law": "Common Law + ICA 1872"},
            {"title": "Receipt for All Payments", "description": "You are entitled to a written receipt for every rent payment, deposit, and maintenance charge paid.", "law": "Payment of Wages Act"},
            {"title": "Habitable Condition", "description": "The property must be in a reasonably habitable condition. Major structural repairs are typically the landlord's responsibility.", "law": "Transfer of Property Act, 1882"},
        ]
    },
    "employee": {
        "title": "Employee Rights in India", "icon": "💼", "color": "navy",
        "rights": [
            {"title": "Right to Written Appointment Letter", "description": "Every employee is entitled to a written appointment letter stating designation, salary, and key terms before joining.", "law": "Shops & Establishments Acts (state-wise)"},
            {"title": "Timely Salary Payment", "description": "Wages must be paid by the 7th of the following month (10th for companies with >1000 employees).", "law": "Payment of Wages Act, 1936"},
            {"title": "Notice Period Rights", "description": "Both parties must give contractual notice before termination. Employer cannot dismiss without proper notice or payment in lieu.", "law": "Industrial Disputes Act, 1947"},
            {"title": "Gratuity After 5 Years", "description": "After 5 years of continuous service, you are entitled to gratuity = 15 days salary × years of service.", "law": "Payment of Gratuity Act, 1972"},
            {"title": "PF & ESI Contributions", "description": "Employer must deposit your PF contribution + equal employer contribution.", "law": "EPF Act 1952 + ESI Act 1948"},
            {"title": "Maternity Leave", "description": "26 weeks paid maternity leave for first two children. 12 weeks for third child onwards.", "law": "Maternity Benefit Act, 1961 (amended 2017)"},
            {"title": "Protection from Harassment", "description": "Right to a safe workplace free from sexual harassment. Every employer with 10+ employees must have an Internal Complaints Committee.", "law": "POSH Act, 2013"},
        ]
    },
    "consumer": {
        "title": "Consumer Rights in India", "icon": "🛒", "color": "gold",
        "rights": [
            {"title": "Right to Safety", "description": "Protection against goods and services that are hazardous to life and property.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Information", "description": "Right to complete information about quality, quantity, potency, purity, standard, and price of goods or services.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Choose", "description": "Access to a variety of goods/services at competitive prices. Monopolistic trade practices are illegal.", "law": "Consumer Protection Act, 2019"},
            {"title": "Right to Seek Redressal", "description": "District forum handles claims up to ₹1 crore. State Commission for ₹1-10 crore. National Commission above ₹10 crore.", "law": "Consumer Protection Act, 2019"},
            {"title": "E-Commerce Rights", "description": "Online sellers must display return policy, delivery timeline, seller details. You can demand refund for defective products.", "law": "Consumer Protection (E-Commerce) Rules, 2020"},
        ]
    },
    "digital": {
        "title": "Digital & Privacy Rights", "icon": "🔐", "color": "burgundy",
        "rights": [
            {"title": "Right to Privacy Online", "description": "Your personal data cannot be collected without consent. Companies must disclose what data they collect and how it is used.", "law": "Digital Personal Data Protection Act, 2023"},
            {"title": "Right to Data Erasure", "description": "You can request deletion of your personal data from platforms and companies.", "law": "DPDPA 2023"},
            {"title": "Protection from Cybercrime", "description": "Identity theft, phishing, online fraud, cyberstalking are criminal offences. File complaint at cybercrime.gov.in.", "law": "IT Act, 2000"},
            {"title": "Right Against Defamation", "description": "Publishing false information about you is actionable under both criminal and civil law.", "law": "IPC + IT Act, 2000"},
            {"title": "Social Media Account Protection", "description": "Hacking, impersonation, and unauthorized access to social media accounts are criminal offences.", "law": "IT Act, 2000 (Section 66C, 66D)"},
        ]
    },
}


def get_checklist(state: str, doc_type: str) -> List[str]:
    state_data = STATE_CHECKLISTS.get(state, DEFAULT_CHECKLISTS)
    return state_data.get(doc_type, DEFAULT_CHECKLISTS.get(doc_type, [
        f"Consult a local lawyer in {state} for {doc_type} requirements",
        "Verify document registration requirements with local Sub-Registrar",
        "Keep copies of all signed documents safely",
        "Stamp the agreement as per your state's Stamp Act",
    ]))


def get_resources_by_state(state: str) -> List[Dict]:
    nalsa = next((r for r in LEGAL_AID_DATA if "NALSA" in r["name"]), None)
    state_resources = [r for r in LEGAL_AID_DATA if r["state"] == state]
    if nalsa and nalsa not in state_resources:
        return [nalsa] + state_resources
    return state_resources or [LEGAL_AID_DATA[0]]
