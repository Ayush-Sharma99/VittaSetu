# scoring/credit_model.py

def compute_credit_score(metrics: dict) -> dict:
    """
    metrics = {
        "filing_rate": float, # 0-1, % of periods with GST filing
        "on_time_rate": float, # 0-1, % of filings made on time
        "reconciliation_rate": float, # 0-1, % of invoices reconciled
        "revenue_trend": float, # -1 to +1 (negative=declining, positive=growing)
        "transaction_consistency": float, # 0-1, regularity of cash flows
        "critical_flags": int, # count of critical compliance flags
        "warning_flags": int # count of warning flags
    }
    """
    weights = {
        "filing_rate": 20,
        "on_time_rate": 15,
        "reconciliation_rate": 20,
        "revenue_trend": 15,
        "transaction_consistency": 15,
        "compliance_health": 15 # derived from flag counts
    }
    
    critical_flags = metrics.get("critical_flags", 0)
    warning_flags = metrics.get("warning_flags", 0)
    
    compliance_health = max(0.0, 1.0 - (critical_flags * 0.15) - (warning_flags * 0.05))
    
    filing_rate = metrics.get("filing_rate", 1.0)
    on_time_rate = metrics.get("on_time_rate", 1.0)
    reconciliation_rate = metrics.get("reconciliation_rate", 1.0)
    revenue_trend = metrics.get("revenue_trend", 0.0)
    transaction_consistency = metrics.get("transaction_consistency", 1.0)
    
    base = (
        filing_rate * weights["filing_rate"] +
        on_time_rate * weights["on_time_rate"] +
        reconciliation_rate * weights["reconciliation_rate"] +
        ((revenue_trend + 1.0) / 2.0) * weights["revenue_trend"] +
        transaction_consistency * weights["transaction_consistency"] +
        compliance_health * weights["compliance_health"]
    )
    
    score = round(min(100.0, max(0.0, base)), 1)
    
    # Map score to grade
    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B+"
    elif score >= 60:
        grade = "B"
    else:
        grade = "C"
        
    return {
        "score": score,
        "grade": grade,
        "factor_breakdown": {
            "filing_compliance": round(filing_rate * weights["filing_rate"], 2),
            "filing_timeliness": round(on_time_rate * weights["on_time_rate"], 2),
            "invoice_reconciliation": round(reconciliation_rate * weights["reconciliation_rate"], 2),
            "revenue_trend": round(((revenue_trend + 1.0) / 2.0) * weights["revenue_trend"], 2),
            "cash_flow_consistency": round(transaction_consistency * weights["transaction_consistency"], 2),
            "compliance_health": round(compliance_health * weights["compliance_health"], 2)
        }
    }
