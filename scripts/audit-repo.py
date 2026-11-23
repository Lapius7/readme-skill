#!/usr/bin/env python3
"""リポジトリの整備状況を調べる。使い方: python3 audit-repo.py [リポジトリのパス]

README の置き換え忘れ、バッジ・リンク、英日の構成、LICENSE などのファイル、About の設定を点検し、
足りないものを一覧にする。変更はしない。終了コードは、問題があれば 1。
"""
import json, os, re, subprocess, sys, urllib.request, urllib.error

root = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
os.chdir(root)
problems, notes = [], []

def bad(m): problems.append(m)
def note(m): notes.append(m)

# 1. ファイル
files = {
    "LICENSE": ["LICENSE", "LICENSE.md", "LICENSE.txt", "COPYING"],
    "SECURITY.md": ["SECURITY.md", ".github/SECURITY.md"],
    "CONTRIBUTING.md": ["CONTRIBUTING.md", ".github/CONTRIBUTING.md"],
}
for name, cands in files.items():
    if not any(os.path.exists(c) for c in cands):
        (bad if name == "LICENSE" else note)(f"{name} がありません")
if not os.path.isdir(".github/ISSUE_TEMPLATE"):
    note("Issue テンプレート（.github/ISSUE_TEMPLATE）がありません")
for opt in ("CODE_OF_CONDUCT.md", ".github/release.yml"):
    if not os.path.exists(opt):
        note(f"{opt} がありません（必要なときだけ足す）")

# 2. README と置き換え忘れ
readmes = [f for f in ("README.md", "README.ja.md") if os.path.exists(f)]
if not readmes:
    bad("README.md がありません")
ph = re.compile(r"OWNER|\bREPO\b|DISPLAY NAME|LATEST_MINOR|BUILD_AND_TEST|ONE-LINE TAGLINE|TODO|FIXME")
targets = readmes + [f for f in ("SECURITY.md", "CONTRIBUTING.md") if os.path.exists(f)]
for dp, _, fs in os.walk(".github"):
    targets += [os.path.join(dp, f) for f in fs]
for f in targets:
    for i, line in enumerate(open(f, encoding="utf-8", errors="ignore"), 1):
        if ph.search(line):
            bad(f"{f}:{i} 置き換え忘れの疑い: {line.strip()[:70]}")

# 3. 英日の構成
def heads(f):
    return [l for l in open(f, encoding="utf-8") if re.match(r"#{2,3} ", l)]
if len(readmes) == 2:
    a, b = heads(readmes[0]), heads(readmes[1])
    if len(a) != len(b):
        bad(f"章の数が英日で違います（{readmes[0]}: {len(a)}、{readmes[1]}: {len(b)}）")

# 4. リンクとバッジ
def status(url):
    try:
        req = urllib.request.Request(url, method="GET", headers={"User-Agent": "readme-audit"})
        return urllib.request.urlopen(req, timeout=15).status
    except urllib.error.HTTPError as e:
        return e.code
    except Exception:
        return 0
seen = set()
for f in readmes:
    text = open(f, encoding="utf-8").read()
    for url in re.findall(r'(?:src|href)="(https?://[^"]+)"|\]\((https?://[^)\s]+)\)', text):
        u = url[0] or url[1]
        if u in seen:
            continue
        seen.add(u)
        s = status(u)
        if s != 200:
            if s == 404 and re.search(r"github\.com/[^/]+/[^/]+/(stargazers|forks|network/members)$", u):
                note(f"{f}: {u} は 404 です（星やフォークが 0 のときの GitHub の仕様。付くまでの一時的なもの）")
            else:
                bad(f"{f}: {u} が {s or '接続失敗'} を返しました")
    for rel in re.findall(r'(?:src|href)="(?!https?:|#|mailto:)([^"]+)"|\]\((?!https?:|#|mailto:)([^)\s]+)\)', text):
        p = (rel[0] or rel[1]).split("#")[0]
        if p and not os.path.exists(p):
            bad(f"{f}: {p} が存在しません")

# 5. About
try:
    j = json.loads(subprocess.run(
        ["gh", "repo", "view", "--json", "description,homepageUrl,repositoryTopics,licenseInfo"],
        capture_output=True, text=True, check=True).stdout)
    if not j["description"]: bad("About の説明が空です")
    if len(j["repositoryTopics"] or []) < 3: note("topics が 3 個未満です")
    if not j["licenseInfo"]: note("GitHub がライセンスを認識していません")
    if j["homepageUrl"]:
        s = status(j["homepageUrl"])
        if s != 200: bad(f"About のホームページ {j['homepageUrl']} が {s or '接続失敗'} です（推測した URL や審査中の公開先は入れない）")
    else:
        note("About のホームページが空です（公開先があれば入れる）")
except Exception as e:
    note(f"gh で About を調べられませんでした: {e}")

print("== 直す ==" if problems else "== 直すもの無し ==")
print("\n".join("- " + p for p in problems))
print("== 検討 ==" if notes else "")
print("\n".join("- " + n for n in notes))
sys.exit(1 if problems else 0)
