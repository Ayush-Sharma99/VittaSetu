import fitz

def generate_bank_statement():
    doc = fitz.open()
    page = doc.new_page()
    
    content = """ADITYA ENTERPRISES - BANK STATEMENT
Period: 01-Jan-2026 to 31-Jan-2026
Account Number: 9876543210
Branch: Mumbai Main Branch

Transaction Ledger:
Date        Reference   Type    Amount (INR)   Description
02-Jan-2026 TXN1001     Credit  250000.00      Payment received from Verma Fabrics
10-Jan-2026 TXN1002     Debit   50000.00       Office rent payment
15-Jan-2026 TXN1003     Credit  125000.00      Payment received from Sharma Garments
25-Jan-2026 TXN1004     Debit   7500.00        Electricity bill payment

Closing Balance: INR 317500.00
"""
    # Insert text lines
    y = 50
    for line in content.split("\n"):
        page.insert_text((50, y), line, fontsize=11, fontname="helv")
        y += 18
        
    doc.save("c:/Users/Lenovo/Downloads/Vitta_Setu/uploaded_docs/bank_statement_aditya.pdf")
    doc.close()
    print("Generated bank_statement_aditya.pdf")

def generate_invoice_1():
    doc = fitz.open()
    page = doc.new_page()
    
    content = """INVOICE
Supplier: Aditya Enterprises
Address: 101, Business Park, Andheri, Mumbai - 400069
GSTIN: 27AEPA1234F1Z0

Invoice Number: AE/2026/001
Invoice Date: 02-Jan-2026
Due Date: 15-Jan-2026

Bill To:
Verma Fabrics
GSTIN: 27VFM7788A1Z2

Item Description                  Qty    Rate (INR)    Amount (INR)
Textile Wholesale - Cotton Roll   10     21186.44      211186.44

Taxable Amount: 211864.41
GST Rate: 18%
GST Amount: 38135.59
Total Amount (incl. GST): 250000.00
"""
    y = 50
    for line in content.split("\n"):
        page.insert_text((50, y), line, fontsize=11, fontname="helv")
        y += 18
        
    doc.save("c:/Users/Lenovo/Downloads/Vitta_Setu/uploaded_docs/invoice_001_aditya.pdf")
    doc.close()
    print("Generated invoice_001_aditya.pdf")

def generate_invoice_2():
    doc = fitz.open()
    page = doc.new_page()
    
    content = """INVOICE
Supplier: Aditya Enterprises
Address: 101, Business Park, Andheri, Mumbai - 400069
GSTIN: 27AEPA1234F1Z0

Invoice Number: AE/2026/002
Invoice Date: 15-Jan-2026
Due Date: 30-Jan-2026

Bill To:
Sharma Garments
GSTIN: 27SHM4433B1Z1

Item Description                  Qty    Rate (INR)    Amount (INR)
Textile Wholesale - Silk Roll     5      21186.44      105932.20

Taxable Amount: 105932.20
GST Rate: 18%
GST Amount: 19067.80
Total Amount (incl. GST): 125000.00
"""
    y = 50
    for line in content.split("\n"):
        page.insert_text((50, y), line, fontsize=11, fontname="helv")
        y += 18
        
    doc.save("c:/Users/Lenovo/Downloads/Vitta_Setu/uploaded_docs/invoice_002_aditya.pdf")
    doc.close()
    print("Generated invoice_002_aditya.pdf")

def generate_gst_return():
    doc = fitz.open()
    page = doc.new_page()
    
    content = """GOODS AND SERVICES TAX - GST RETURN (GSTR-3B)
Filing Period: January 2026
Filing Date: 20-Feb-2026
GSTIN: 27AEPA1234F1Z0
Legal Name: Aditya Enterprises

Section 3.1: Details of Outward Supplies
Total Outward Taxable Supplies: 317796.61
Integrated Tax (IGST): 0.00
Central Tax (CGST): 28601.70
State Tax (SGST): 28601.70

Filing Status: Filed on Time
Receipt Number: GSTIN3B99887766
"""
    y = 50
    for line in content.split("\n"):
        page.insert_text((50, y), line, fontsize=11, fontname="helv")
        y += 18
        
    doc.save("c:/Users/Lenovo/Downloads/Vitta_Setu/uploaded_docs/gst_return_aditya.pdf")
    doc.close()
    print("Generated gst_return_aditya.pdf")

if __name__ == "__main__":
    import os
    os.makedirs("c:/Users/Lenovo/Downloads/Vitta_Setu/uploaded_docs", exist_ok=True)
    generate_bank_statement()
    generate_invoice_1()
    generate_invoice_2()
    generate_gst_return()
