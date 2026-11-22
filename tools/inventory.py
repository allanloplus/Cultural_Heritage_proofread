"""盤點：讀出兩個文資知識網站每個縣市的資料，以及所有受檢網站的清單。"""
import json, os, re
from common import cfg, load, repo_dir, repo_files, log

SITES = cfg("sites")["sites"]


def site(sid):
    return next(s for s in SITES if s["id"] == sid)


class City:
    def __init__(self, s, d, slug):
        self.site, self.repo, self.dir, self.slug = s, s["repo"], d, slug
        p = lambda n, default=None: load(os.path.join(d, slug, "data", n + ".json"), default)
        self.config = p("config", {})
        self.name = self.config.get("name", slug)
        self.official = p("sites-official", [])
        self.content = p("sites-content", [])
        self.ich = p("ich", {"items": [], "venues": []})
        self.images = p("images", {})
        self.eras = p("eras", {})
        self.extra = p("extra", {})
        self.url = s["url"] + slug + "/"

    def json_files(self):
        dd = os.path.join(self.dir, self.slug, "data")
        return [(n, load(os.path.join(dd, n))) for n in sorted(os.listdir(dd)) if n.endswith(".json") and n != "ubike.json"]


_CITIES = None


def cities():
    """兩個知識網站所有已有 data/config.json 的縣市。"""
    global _CITIES
    if _CITIES is None:
        _CITIES = []
        for s in SITES:
            if s["role"] != "core":
                continue
            d = repo_dir(s["repo"])
            if not d:
                log("找不到 repo：", s["repo"])
                continue
            for slug in sorted(os.listdir(d)):
                if os.path.exists(os.path.join(d, slug, "data", "config.json")):
                    _CITIES.append(City(s, d, slug))
    return _CITIES


def data_js(city):
    """縣市頁實際載入的 js/data.js（由主網站 tools/build_data.py 產生）。"""
    p = os.path.join(city.dir, city.slug, "js", "data.js")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    try:
        return json.loads(t[t.index("{", t.index("window.")):t.rstrip().rstrip(";").rindex("}") + 1])
    except Exception:
        return None


def audio_cues(city):
    p = os.path.join(city.dir, city.slug, "audio", "cues.js")
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8").read()
    try:
        return json.loads(t[t.index('{"'):t.rindex("}") + 1].rstrip(")"))
    except Exception:
        try:
            return json.loads(t[t.index('{"'):t.rindex("})") + 1])
        except Exception:
            return None
