import os, subprocess, time, shutil, concurrent.futures as cf
from PIL import Image
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
OUT = f"{ROOT}/shots"; os.makedirs(OUT, exist_ok=True)
TMP = "/tmp/gallery_shots"; os.makedirs(TMP, exist_ok=True)
sites = sorted(d for d in os.listdir(f"{ROOT}/sites") if os.path.isfile(f"{ROOT}/sites/{d}/index.html"))

def shoot(slug):
    png, prof = f"{TMP}/{slug}.png", f"{TMP}/prof_{slug}"
    for p in (png,): 
        if os.path.exists(p): os.remove(p)
    cmd = [CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--no-first-run",
           "--no-default-browser-check", "--disable-extensions", "--force-device-scale-factor=1",
           "--window-size=1280,800", "--virtual-time-budget=4000",
           f"--user-data-dir={prof}", f"--screenshot={png}",
           f"http://localhost:8777/sites/{slug}/index.html"]
    proc = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    # 크롬이 스크린샷을 쓴 뒤에도 종료되지 않으므로, 파일 크기가 안정되면 직접 죽인다
    deadline, last, stable = time.time() + 90, -1, 0
    try:
        while time.time() < deadline:
            if proc.poll() is not None: break
            if os.path.exists(png):
                sz = os.path.getsize(png)
                stable = stable + 1 if sz == last and sz > 10000 else 0
                last = sz
                if stable >= 3: break
            time.sleep(0.4)
    finally:
        if proc.poll() is None:
            proc.terminate()
            try: proc.wait(timeout=8)
            except Exception: proc.kill()
    shutil.rmtree(prof, ignore_errors=True)
    if not os.path.exists(png) or os.path.getsize(png) < 10000:
        return slug, "실패"
    im = Image.open(png).convert("RGB")
    if im.size != (1280, 800): im = im.resize((1280, 800), Image.LANCZOS)
    im.resize((960, 600), Image.LANCZOS).save(f"{OUT}/{slug}.webp", "WEBP", quality=82, method=6)
    return slug, f"ok ({os.path.getsize(f'{OUT}/{slug}.webp')//1024}KB)"

ok = 0
with cf.ThreadPoolExecutor(max_workers=3) as ex:
    for slug, st in ex.map(shoot, sites):
        print(f"  {slug:<26} {st}", flush=True)
        ok += st.startswith("ok")
tot = sum(os.path.getsize(f"{OUT}/{f}") for f in os.listdir(OUT))
print(f"\n성공 {ok}/{len(sites)} | shots/ {tot/1024/1024:.1f} MB")
