"""Measure XZ size/load time/isolated process peak RAM; never rewrite sources."""
import argparse
import ctypes
import json
import lzma
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import ijson


def peak_rss():
    if os.name == 'nt':
        class Counters(ctypes.Structure):
            _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [
                (name, ctypes.c_size_t) for name in ('PeakWorkingSetSize', 'WorkingSetSize',
                'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage',
                'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage')]
        counters = Counters(); counters.cb = ctypes.sizeof(counters)
        kernel = ctypes.windll.kernel32
        kernel.GetCurrentProcess.restype = ctypes.c_void_p
        psapi = ctypes.windll.psapi
        psapi.GetProcessMemoryInfo.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        if not psapi.GetProcessMemoryInfo(kernel.GetCurrentProcess(), ctypes.byref(counters), counters.cb):
            raise ctypes.WinError()
        return counters.PeakWorkingSetSize
    import resource
    value = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return value if sys.platform == 'darwin' else value * 1024


def decode(path, mode):
    start = time.perf_counter()
    with lzma.open(path, 'rb') as stream:
        first = stream.read(1); stream.seek(0)
        iterator = ijson.items(stream, 'exams.item' if first == b'{' else 'item', use_float=True)
        count = len(list(iterator)) if mode == 'list' else sum(1 for _ in iterator)
    return {'mode': mode, 'exam_count': count, 'seconds': time.perf_counter() - start,
            'process_peak_rss_bytes': peak_rss()}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--report', type=Path)
    parser.add_argument('--decode', choices=['stream', 'list'])
    args = parser.parse_args()
    if args.decode:
        print(json.dumps(decode(args.source, args.decode)))
    else:
        with lzma.open(args.source, 'rb') as stream:
            raw = stream.read()
        rows = []
        with tempfile.TemporaryDirectory(prefix='gsai-xz-benchmark-') as directory:
            for dictionary in (1 << 20, 4 << 20, 8 << 20, 64 << 20):
                start = time.perf_counter()
                packed = lzma.compress(raw, filters=[{'id': lzma.FILTER_LZMA2, 'preset': 6, 'dict_size': dictionary}])
                compress_seconds = time.perf_counter() - start
                candidate = Path(directory) / 'candidate.xz'; candidate.write_bytes(packed)
                assert lzma.decompress(packed) == raw
                for mode in ('stream', 'list'):
                    child = subprocess.run([sys.executable, __file__, '--source', str(candidate), '--decode', mode],
                        check=True, capture_output=True, text=True)
                    rows.append({'dictionary_bytes': dictionary, 'compressed_bytes': len(packed),
                        'compression_seconds': compress_seconds, **json.loads(child.stdout)})
        report = {'source': str(args.source), 'uncompressed_bytes': len(raw),
            'scope': 'single real shard benchmark; not a universal optimality or knowledge certificate',
            'method': 'separate decode processes; OS peak working set includes interpreter/native decoder; one run per case',
            'rows': rows}
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2), encoding='utf-8')
        print(json.dumps(rows))
