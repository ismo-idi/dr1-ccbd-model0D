import json
from src.io_utils import write_json,write_jsonl
def test_nonfinite_diagnostics_are_serialized_as_categorical_markers(tmp_path):
 p=tmp_path/'x.json';write_json(p,{'nan':float('nan'),'pinf':float('inf'),'ninf':float('-inf')});assert json.loads(p.read_text())=={'nan':'NONFINITE_NAN','pinf':'NONFINITE_POSITIVE_INFINITY','ninf':'NONFINITE_NEGATIVE_INFINITY'};q=tmp_path/'x.jsonl';write_jsonl(q,[{'v':float('nan')}]);assert json.loads(q.read_text().strip())['v']=='NONFINITE_NAN'
