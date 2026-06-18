# demo/seed_data.py
from datetime import datetime, date

DEMO_BUSINESS = {
    "name": "Ravi Kumar Textiles",
    "gstin": "27AABCU9603R1ZM",
    "email": "ravi@ravitextiles.com",
    "phone": "9876543210",
    "demo_mode": True
}

DEMO_BANK_TRANSACTIONS = [
    {"date": "2026-01-05", "description": "NEFT CR MEHTA FABRICS", "amount": 185000, "txn_type": "credit", "category": "sales"},
    {"date": "2026-01-10", "description": "NEFT DR YARN SUPPLIER AHMEDABAD", "amount": 120000, "txn_type": "debit", "category": "purchase"},
    {"date": "2026-01-15", "description": "OFFICE RENT JAIPUR", "amount": 25000, "txn_type": "debit", "category": "other"},
    {"date": "2026-01-20", "description": "GST PAYMENT CHALLAN JAN", "amount": 33156, "txn_type": "debit", "category": "tax"},
    {"date": "2026-02-05", "description": "NEFT CR MEHTA FABRICS", "amount": 220000, "txn_type": "credit", "category": "sales"},
    {"date": "2026-02-12", "description": "NEFT DR YARN SUPPLIER AHMEDABAD", "amount": 130000, "txn_type": "debit", "category": "purchase"},
    {"date": "2026-02-20", "description": "GST PAYMENT CHALLAN FEB", "amount": 39600, "txn_type": "debit", "category": "tax"},
    {"date": "2026-03-03", "description": "NEFT CR MEHTA FABRICS", "amount": 185000, "txn_type": "credit", "category": "sales"},
    {"date": "2026-03-05", "description": "NEFT DR YARN SUPPLIER AHMEDABAD", "amount": 95000, "txn_type": "debit", "category": "purchase"},
    {"date": "2026-03-10", "description": "GST PAYMENT CHALLAN MAR", "amount": 24800, "txn_type": "debit", "category": "tax"},
    {"date": "2026-03-12", "description": "NEFT CR SHARMA EXPORTS", "amount": 234000, "txn_type": "credit", "category": "sales"},
    {"date": "2026-03-18", "description": "ELECTRICITY BILL", "amount": 8500, "txn_type": "debit", "category": "other"},
    {"date": "2026-03-25", "description": "SALARY RAVI EMPLOYEES", "amount": 60000, "txn_type": "debit", "category": "salary"},
    {"date": "2026-03-28", "description": "INTEREST CHARGES SBI", "amount": 4200, "txn_type": "debit", "category": "other"},
]

# We need 24 invoices - 21 match, 3 do not. Let's build exactly that structure.
# Let's seed invoices matching these transactions plus 3 unmatched.
DEMO_INVOICES = [
    # Reconciled/matching ones
    {"invoice_number": "RKT/2026/001", "date": "2026-01-05", "vendor_or_customer": "Mehta Fabrics", "amount": 185000, "gst_amount": 33300, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/002", "date": "2026-01-10", "vendor_or_customer": "Yarn Supplier Ahmedabad", "amount": 120000, "gst_amount": 21600, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/003", "date": "2026-02-05", "vendor_or_customer": "Mehta Fabrics", "amount": 220000, "gst_amount": 39600, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/004", "date": "2026-02-12", "vendor_or_customer": "Yarn Supplier Ahmedabad", "amount": 130000, "gst_amount": 23400, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/005", "date": "2026-03-03", "vendor_or_customer": "Mehta Fabrics", "amount": 185000, "gst_amount": 33300, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/006", "date": "2026-03-05", "vendor_or_customer": "Yarn Supplier Ahmedabad", "amount": 95000, "gst_amount": 17100, "gst_rate": 18, "hsn_code": "5208"},
    {"invoice_number": "RKT/2026/007", "date": "2026-03-12", "vendor_or_customer": "Sharma Exports", "amount": 234000, "gst_amount": 42120, "gst_rate": 18, "hsn_code": "5208"},
]

# Generate standard matches to fill up to 21 invoices matched and 3 unmatched.
for i in range(8, 22):
    DEMO_INVOICES.append({
        "invoice_number": f"RKT/2026/0{i:02d}",
        "date": f"2026-02-{(i%20)+1:02d}",
        "vendor_or_customer": "Local Distributor",
        "amount": 10000 + (i * 1000),
        "gst_amount": (10000 + (i * 1000)) * 0.18,
        "gst_rate": 18,
        "hsn_code": "5208"
    })
    # Corresponding bank transactions for those matches
    DEMO_BANK_TRANSACTIONS.append({
        "date": f"2026-02-{(i%20)+1:02d}",
        "description": f"NEFT CR LOCAL DISTRIBUTOR {i}",
        "amount": 10000 + (i * 1000),
        "txn_type": "credit",
        "category": "sales"
    })

# Unreconciled/Unmatched invoices
DEMO_INVOICES.extend([
    {"invoice_number": "RKT/2026/022", "date": "2026-03-20", "vendor_or_customer": "Patel Garments", "amount": 95000, "gst_amount": 17100, "gst_rate": 18, "hsn_code": "5209"},
    {"invoice_number": "RKT/2026/023", "date": "2026-03-22", "vendor_or_customer": "Raj Fabrics", "amount": 45000, "gst_amount": 8100, "gst_rate": 18, "hsn_code": "5209"},
    {"invoice_number": "RKT/2026/024", "date": "2026-03-24", "vendor_or_customer": "Karan Suits", "amount": 65000, "gst_amount": 11700, "gst_rate": 18, "hsn_code": "5209"},
])

DEMO_GST_RETURN = {
    "return_type": "GSTR-3B",
    "filing_period": "March 2026",
    "filing_date": "2026-04-22",  # 2 days late -> triggers warning
    "gstin": "27AABCU9603R1ZM",
    "taxable_turnover": 1842000,
    "total_tax_liability": 331560,
    "tax_paid": 331560,
    "late_fee": 100,
    "status": "filed"
}

DEMO_EXPECTED_SCORE = {
    "score": 71.0,
    "filing_rate": 0.92,
    "on_time_rate": 0.80, # 1 late filing in 5 periods
    "reconciliation_rate": 0.875, # 21 / 24
    "revenue_trend": 0.4, # mild growth
    "transaction_consistency": 0.72,
    "critical_flags": 0,
    "warning_flags": 2 # late filing + 3 unreconciled invoices
}
