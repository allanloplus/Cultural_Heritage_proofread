"""共用：路徑、設定、下載、發現（finding）格式。只用 Python 標準函式庫。

網路禮儀：所有對外請求都用下面的 UA（只放專案網址，不放任何人的 Email 或帳號）；
同一個網站的請求之間固定間隔，被限流（429／403）時只記為「未能確認」，不重複衝撞。
"""
import datetime, hashlib, json, os, re, ssl, subprocess, sys, threading, time, unicodedata, urllib.error, urllib.parse, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(ROOT, ".cache")
STATE = os.path.join(ROOT, "state")
REPORTS = os.path.join(ROOT, "reports")
UA = "AllanLoCultureProofread/1.0 (https://github.com/allanloplus/Cultural_Heritage_proofread)"
TODAY = os.environ.get("PROOFREAD_DATE") or datetime.date.today().isoformat()

_CA = os.environ.get("TTS_CA_BUNDLE") or ("/root/.ccr/ca-bundle.crt" if os.path.exists("/root/.ccr/ca-bundle.crt") else None)
CTX = ssl.create_default_context(cafile=_CA) if _CA else ssl.create_default_context()
if _CA:  # 經過代理時：Python 3.13 預設嚴格 X.509，代理憑證缺 SKI 會被拒；只關嚴格模式，仍完整驗證憑證
    CTX.verify_flags &= ~ssl.VERIFY_X509_STRICT
VIA_PROXY = bool(_CA)


def load(path, default=None):
    if not os.path.exists(path):
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dump(obj, path, indent=1):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=indent, sort_keys=False)
        f.write("\n")
    os.replace(tmp, path)


def cfg(name):
    return load(os.path.join(ROOT, "config", name + ".json"))


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# ---------- 各網站的 repo ----------

def repo_dir(name):
    """其他 repo 的位置：環境變數 REPOS_DIR（底下每個 repo 一個資料夾），沒設就找本 repo 旁邊。"""
    base = os.environ.get("REPOS_DIR") or os.path.dirname(ROOT)
    for n in (name, name.lower()):
        d = os.path.join(base, n)
        if os.path.isdir(d):
            return d
    return None


_FILES = {}


def repo_files(d):
    """repo 裡有哪些檔案。用 git 的清單而不是磁碟：排程檢測只取出文字檔（不下載語音與照片），清單仍然完整。"""
    if d not in _FILES:
        try:
            out = subprocess.run(["git", "-C", d, "ls-files", "-z"], capture_output=True, check=True).stdout.decode("utf-8")
            _FILES[d] = set(out.split("\0")) - {""}
        except Exception:
            s = set()
            for r, ds, fs in os.walk(d):
                ds[:] = [x for x in ds if x != ".git"]
                for f in fs:
                    s.add(os.path.relpath(os.path.join(r, f), d).replace(os.sep, "/"))
            _FILES[d] = s
    return _FILES[d]


def git_date(d, *paths):
    """這些檔案最後一次提交的日期（YYYY-MM-DD）；查不到就回傳 None。"""
    try:
        out = subprocess.run(["git", "-C", d, "log", "-1", "--format=%cs", "--"] + list(paths),
                             capture_output=True, check=True).stdout.decode().strip()
        return out or None
    except Exception:
        return None


def git_blob(d, path):
    try:
        return subprocess.run(["git", "-C", d, "show", "HEAD:" + path], capture_output=True, check=True).stdout
    except Exception:
        return None


# ---------- 下載 ----------

_HOST_LOCK = {}
_HOST_LAST = {}
_GLOBAL = threading.Lock()


def _wait(host, gap):
    with _GLOBAL:
        lk = _HOST_LOCK.setdefault(host, threading.Lock())
    with lk:
        d = _HOST_LAST.get(host, 0) + gap - time.time()
        if d > 0:
            time.sleep(d)
        _HOST_LAST[host] = time.time()


class _NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *a, **k):
        return None


def http(url, method="GET", timeout=25, gap=1.0, max_bytes=65536, redirects=5, headers=None):
    """回傳 dict：code（HTTP 狀態碼，連不上為 0）、final（最後網址）、hops（轉址次數）、body（前段內容）、err、headers。"""
    hops, cur, perm = 0, url, True
    while True:
        host = urllib.parse.urlsplit(cur).netloc
        _wait(host, gap)
        h = {"User-Agent": UA, "Accept": "*/*", "Accept-Language": "zh-TW,zh;q=0.9,en;q=0.5"}
        h.update(headers or {})
        req = urllib.request.Request(_quote(cur), method=method, headers=h)
        op = urllib.request.build_opener(_NoRedirect, urllib.request.HTTPSHandler(context=CTX))
        try:
            with op.open(req, timeout=timeout) as r:
                body = r.read(max_bytes) if method != "HEAD" else b""
                return {"code": r.status, "final": cur, "hops": hops, "perm": perm and hops > 0, "body": body, "err": "", "headers": dict(r.headers)}
        except urllib.error.HTTPError as e:
            if e.code in (301, 302, 303, 307, 308) and e.headers.get("Location") and hops < redirects:
                perm = perm and e.code in (301, 308)
                cur = urllib.parse.urljoin(cur, e.headers["Location"])
                hops += 1
                continue
            return {"code": e.code, "final": cur, "hops": hops, "perm": False, "body": b"", "err": "", "headers": dict(e.headers or {})}
        except Exception as e:
            return {"code": 0, "final": cur, "hops": hops, "perm": False, "body": b"", "err": "%s: %s" % (type(e).__name__, str(e)[:120]), "headers": {}}


def _quote(u):
    """網址裡的中文等非 ASCII 字元先編碼（已編碼的 %xx 保持原樣）。"""
    p = urllib.parse.urlsplit(u)
    return urllib.parse.urlunsplit((p.scheme, p.netloc.encode("idna").decode() if not p.netloc.isascii() else p.netloc,
                                    urllib.parse.quote(p.path, safe="/%:@!$&'()*+,;=~-._"),
                                    urllib.parse.quote(p.query, safe="=&%:@!$'()*+,;/?~-._"), ""))


def get_json(url, timeout=60, tries=4, gap=1.0):
    """下載 JSON；429／5xx 會依 Retry-After 等一下再試。失敗回傳 None。"""
    for i in range(tries):
        r = http(url, timeout=timeout, gap=gap, max_bytes=50_000_000)
        if r["code"] == 200:
            try:
                return json.loads(r["body"])
            except Exception:
                return None
        if r["code"] in (429, 500, 502, 503, 504, 0):
            ra = r["headers"].get("Retry-After", "")
            if i < tries - 1:
                time.sleep(min(max(int(ra) if ra.isdigit() else 0, 5 * (i + 1)), 60))
            continue
        return None
    return None


# ---------- 發現（finding） ----------

SEV = ["high", "medium", "low", "info"]


def finding(check, sev, site, title, detail="", city="", item="", name="", url="", sub="", extra=None):
    """一筆檢測發現。key 由「檢測項目＋網站＋縣市＋文資＋sub」算出，跨次檢測不變，用來追蹤首次發現日與是否已解決。"""
    raw = "|".join([check, site or "", city or "", item or "", sub or ""])
    f = {"key": hashlib.sha1(raw.encode("utf-8")).hexdigest()[:12], "dsha": dsha(detail), "check": check, "sev": sev, "site": site or "",
         "city": city or "", "item": item or "", "name": name or "", "title": title, "detail": detail or "", "url": url or ""}
    if extra:
        f.update(extra)
    return f


VARIANTS = str.maketrans("台参湾厦啓峯羣舘床礮炮", "臺參灣廈啟峰群館牀砲砲")  # 異體字視為相同（官方資料常用異體字，網站用通行字）


def norm_name(s):
    """名稱比對用：異體字統一、去掉括號內容、空白與標點。"""
    s = unicodedata.normalize("NFKC", s or "")  # 官方資料偶有「相容字」（外觀相同、編碼不同）
    s = re.sub(r"[（(].*?[)）]", "", s)
    s = s.translate(VARIANTS).replace("國定古蹟-", "").replace("國定古蹟", "")
    return re.sub(r"[\s\-—–－─‧・·、，,。\.「」『』《》〈〉:：；;'’‘\"“”/／]", "", s).lower()


def same_name(a, b, loose=False):
    """名稱是否相同。括號內容去掉或保留都試（官方常寫成「族語名稱(中文名稱)」）；loose=True 時互相包含也算。"""
    va = {norm_name(a), norm_name(re.sub(r"[（()）]", " ", a or ""))} - {""}
    vb = {norm_name(b), norm_name(re.sub(r"[（()）]", " ", b or ""))} - {""}
    if va & vb:
        return True
    return loose and any(len(x) >= 3 and len(y) >= 3 and (x in y or y in x or (min(len(x), len(y)) >= 6 and (_subseq(x, y) or _subseq(y, x))))
                         for x in va for y in vb)


def _subseq(a, b):
    """a 的每個字是否依序出現在 b 裡（官方名稱常在中間多加年代、族語）。"""
    it = iter(b)
    return all(ch in it for ch in a)


def dsha(detail):
    return hashlib.sha1((detail or "").encode("utf-8")).hexdigest()[:8]


def days_between(a, b):
    try:
        return (datetime.date.fromisoformat(b) - datetime.date.fromisoformat(a)).days
    except Exception:
        return 0
