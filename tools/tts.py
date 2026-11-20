#!/usr/bin/env python3
"""Generate MP3s from tools/tts_jobs.json with edge-tts, then trim silence (tools/trim.py).
Voices: f = en-US-AriaNeural, m = en-US-AndrewNeural (sentences, -8%), w = AriaNeural -15% (word tiles)."""
import asyncio, json, os, subprocess, sys
import edge_tts
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = {"f": ("en-US-AriaNeural", "-8%"), "m": ("en-US-AndrewNeural", "-8%"), "w": ("en-US-AriaNeural", "-15%")}
async def one(sem, fn, job, fails):
    path = os.path.join(ROOT, fn)
    if os.path.exists(path): return
    voice, rate = V[job["voice"]]
    async with sem:
        for a in range(5):
            try:
                await edge_tts.Communicate(job["text"], voice, rate=rate).save(path + ".part")
                assert os.path.getsize(path + ".part") > 1000
                os.replace(path + ".part", path); return
            except Exception:
                await asyncio.sleep(2 + 3 * a)
        fails.append(fn)
async def main():
    jobs = json.load(open(os.path.join(ROOT, "tools", "tts_jobs.json"), encoding="utf-8"))
    sem, fails = asyncio.Semaphore(8), []
    await asyncio.gather(*[one(sem, f, j, fails) for f, j in jobs.items()])
    if fails: print("FAILED", fails); sys.exit(1)
asyncio.run(main())
subprocess.run([sys.executable, os.path.join(ROOT, "tools", "trim.py")], check=True)
