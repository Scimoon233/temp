from pathlib import Path
import json, hashlib, os, tempfile
root=Path(__file__).resolve().parent
folder=root/'04_Format_Reference/Jacobs_2019_Accepted_Manuscript_parts'
m=json.loads((folder/'MANIFEST.json').read_text())
target=root/m['original_path']
with tempfile.NamedTemporaryFile(dir=target.parent,delete=False) as output:
    temporary=Path(output.name)
    for item in m['parts']:
        data=(root/item['path']).read_bytes()
        assert len(data)==item['bytes'] and hashlib.sha256(data).hexdigest()==item['sha256']
        output.write(data)
assert temporary.stat().st_size==m['original_bytes']
assert hashlib.sha256(temporary.read_bytes()).hexdigest()==m['original_sha256']
os.replace(temporary,target)
print('Restored and verified:',target)
