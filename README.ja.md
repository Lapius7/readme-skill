<div align="center">

<p align="center"><img alt="readme-creator: a sample README rendered in GitHub dark theme" src="docs/images/banner.png" width="100%"></p>

<p align="center"><a href="README.md">English</a> | <b>日本語</b></p>

<h1 align="center">README Creator SKILL</h1>

<h3 align="center">有名リポジトリのような README を作る、Claude 向けのスキル。</h3>

<p align="center">中央寄せのバナー、色分けしたバッジ、GitHub の Alert、折りたたみの表、そろえた英日の2言語版を作ります。見た目より事実を優先します。</p>

<p align="center">
  <a href="https://github.com/Lapius7/readme-skill/stargazers"><img alt="Stars" src="https://img.shields.io/github/stars/Lapius7/readme-skill?style=flat-square&color=e3b341&logo=github"></a>
  <a href="https://github.com/Lapius7/readme-skill/commits/main"><img alt="Last commit" src="https://img.shields.io/github/last-commit/Lapius7/readme-skill?style=flat-square&color=3b82f6"></a>
  <a href="https://docs.claude.com/en/docs/claude-code/skills"><img alt="Claude skill" src="https://img.shields.io/badge/Claude-skill-d97757?style=flat-square&logo=anthropic&logoColor=white"></a>
  <a href="https://github.com/python-pillow/Pillow"><img alt="Pillow" src="https://img.shields.io/badge/banner-Pillow-3776ab?style=flat-square&logo=python&logoColor=white"></a>
</p>

<p align="center">
  <a href="#できること">できること</a> ·
  <a href="#インストール">インストール</a> ·
  <a href="#使い方">使い方</a> ·
  <a href="#中身">中身</a>
</p>

</div>

---

Claude に「READMEを良くして」「バッジとバナーを付けて」と頼むと、このスキルが構成、バッジ、Alert、バナーを決め、できあがりを確かめます。

## できること

- **構成**: 言語切替、バナー、キャッチコピー、バッジ、概要、特長、クイックスタート、ツール、設定、安全、開発、今後の予定、ライセンスの順に並べます。
- **バナー**: プロジェクトの実物のレンダリングやスクリーンショットから、角丸の横長の画像を作り、大きな白字で名前を重ねます。暗くする処理、角丸、文字の重ねは `scripts/make-banner.py` が行います。
- **バッジ**: shields.io の `flat-square` で、バッジごとに色とロゴを付けます。実在するリンクだけを置きます。
- **Alert**: `NOTE`、`TIP`、`IMPORTANT`、`WARNING`、`CAUTION` を、意味のある所にだけ使います。絵文字は使いません。
- **英日の2言語**: 2つの版を同じ構成にします。日本語は `yomiyasu` スキルで推敲します。
- **事実を優先**: ツール名、上限値、設定名は、コードと照合します。実機で試していないことは、未検証と書きます。

## インストール

Claude Code がスキルを探すフォルダに置きます。

```sh
git clone https://github.com/Lapius7/readme-skill ~/.claude/skills/readme-creator
```

バナーのスクリプトには [uv](https://docs.astral.sh/uv/) が要ります。Pillow は `uv run` が必要なときに取得します。

> [!NOTE]
> 日本語の推敲には、スキル `yomiyasu` を参照します。なくても動きますが、日本語の推敲はされません。

## 使い方

ふだんの言葉で頼みます。例を挙げます。

- 「このリポジトリの README を書いて」
- 「README を、バッジとバナーつきで良くして」
- 「改名したので、README の URL を直して」

バナーだけを作るときは、次のようにします。

```sh
uv run --with pillow python scripts/make-banner.py "プロジェクト名" docs/images/hero.png docs/images/banner.png
```

元画像の既定は `docs/images/hero.png`、出力の既定は `docs/images/banner.png` で、実行したフォルダが基準です。

## 中身

| パス | 内容 |
|---|---|
| `SKILL.md` | Claude が従う指示です。手順、構成、バナー、バッジ、Alert、守ることを書いています。 |
| `templates/README.template.md` | 中央寄せのヘッダー、バッジ行、Alert、折りたたみの表を入れた README の雛形です。 |
| `scripts/make-banner.py` | プロジェクト名を重ねた、角丸のバナーを作ります。 |

> [!IMPORTANT]
> 英語版と日本語版の README は、同じ構成に保ちます。片方に節を足したら、もう片方にも足します。

## ライセンス

MIT です。[LICENSE](LICENSE) を見てください。`scripts/vendor` の CSS は github-markdown-css（MIT、Sindre Sorhus）です。
