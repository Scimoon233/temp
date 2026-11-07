from pathlib import Path
import json,hashlib
root=Path(__file__).resolve().parent
items=json.loads((root/"MANIFEST.json").read_text(encoding="utf-8"))
bad=[]
for item in items:
 p=root/item["path"]
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=item["sha256"]:
  bad.append(item["path"])
if bad:
 raise SystemExit("FAILED: "+str(bad))
print("Verified",len(items),"files")
