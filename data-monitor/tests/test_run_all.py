import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from monitor import checks, sample


def test_demo_data_is_detected():
    base = checks.build_baseline(sample.make_sample(False))
    res = checks.run_all_checks(sample.make_sample(True), base, {"timestamp_column": "order_date"})
    fails = {(r["check"], r["column"]) for r in res if r["status"] == "FAIL"}
    assert ("duplicate_rows", "*") in fails and ("drift_psi", "amount") in fails
    assert ("freshness", "order_date") in fails
    clean = checks.run_all_checks(sample.make_sample(False), base, {"timestamp_column": "order_date"})
    assert checks.quality_score(clean) >= 90
