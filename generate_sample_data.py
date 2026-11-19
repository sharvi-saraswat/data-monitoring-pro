"""Optional: writes data/sample_clean.csv and data/sample_dirty.csv for the 'File path' source."""
from pathlib import Path
from monitor.sample import make_sample

out = Path(__file__).resolve().parent / "data"
out.mkdir(exist_ok=True)
make_sample(False).to_csv(out / "sample_clean.csv", index=False)
make_sample(True).to_csv(out / "sample_dirty.csv", index=False)
print("Sample files created in data/")
