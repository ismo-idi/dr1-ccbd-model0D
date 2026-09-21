"""Verify or restore losslessly archived input evidence; never run a solver."""
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import json


def sha(data):
    return hashlib.sha256(data).hexdigest()


def safe(root, relative):
    p = Path(relative)
    if p.is_absolute() or '..' in p.parts:
        raise ValueError(f'Unsafe relative path: {relative}')
    result = (root / p).resolve()
    if not result.is_relative_to(root.resolve()):
        raise ValueError(f'Path leaves archive: {relative}')
    return result


def put(path, data):
    if path.exists():
        if path.read_bytes() != data:
            raise ValueError(f'Refusing to overwrite differing file: {path}')
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--verify', action='store_true')
    mode.add_argument('--restore', action='store_true')
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / 'provenance/INPUT_FILE_MAP.json').read_text())
    restored = 0
    for entry in manifest['entries']:
        stored = safe(root, entry['stored_path']).read_bytes()
        if sha(stored) != entry['stored_sha256']:
            raise ValueError(f'Stored hash mismatch: {entry["stored_path"]}')
        raw = gzip.decompress(stored) if entry['compression'] == 'gzip' else stored
        if len(raw) != entry['original_bytes'] or sha(raw) != entry['original_sha256']:
            raise ValueError(f'Original hash mismatch: {entry["original_path"]}')
        if args.restore and entry['compression']:
            dst = safe(root, f'attempts/{entry["attempt"]}/{entry["original_path"]}')
            restored += put(dst, raw)
    for entry in manifest['excluded_cache_files']:
        raw = base64.b64decode(entry['base64'], validate=True)
        if len(raw) != entry['original_bytes'] or sha(raw) != entry['original_sha256']:
            raise ValueError(f'Historical cache mismatch: {entry["path"]}')
        if args.restore:
            dst = safe(root, f'attempts/{entry["attempt"]}/{entry["path"]}')
            restored += put(dst, raw)
    print(json.dumps({'status': 'PASS', 'input_files_verified': len(manifest['entries']),
                      'historical_cache_files_verified': len(manifest['excluded_cache_files']),
                      'files_restored': restored, 'simulation_executed': False}))


if __name__ == '__main__':
    main()
