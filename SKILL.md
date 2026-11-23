---
name: readme-skill
description: GitHub リポジトリの README を、有名リポジトリのような見た目（中央寄せの言語切替とタイトル、色分けしたバッジ、Alert、折りたたみの表、英日の2言語）に作る・作り直すスキル。「READMEを作って」「READMEを良くして」「READMEをかっこよく」「バッジを付けて」と頼まれたときに使う。バナーは、見栄えよく作れるときと、指定があるときだけ付ける。README と一緒に、LICENSE・SECURITY・CONTRIBUTING・About・Issue テンプレートなど、GitHub の画面で見えるリポジトリの整備も行う。
---

# README Creator SKILL

README を、見た目と中身の両方で整えます。READMEは、そのソフトを使う人のための文書です。作る人や公開する人のための手順は書きません。見た目の基準は Firecrawl や Disc Image Studio のような有名リポジトリです。ただし、見た目より事実の正しさを優先します。

## 手順

1. **事実を集める**: コード、package.json、既存の README、設定ファイルを読み、機能名、ツール名、上限値、必要なもの、ライセンスを確かめる。確認できないことは書かない。
2. **構成を決める**: 下の「構成」に沿って章を並べる。
3. **バナーを作る（任意）**: 暗い画面イメージや罫線の図柄などの元画像に大きなタイトルを重ねて、見栄えよく作れるときは付ける。ユーザーに指定があるときも付ける。コマンドやコードの文字を並べただけの画像（ターミナル画面の画像化、コード断片の背景）、文字だけ、単色の板になるときは付けない。迷うときも付けない。下の「バナー」に従う。
4. **README を書く**: `templates/README.template.md` を元にする。英語版を `README.md`、日本語版を `README.ja.md` に置き、構成をそろえる。
5. **推敲する**: 日本語は skill `yomiyasu` で推敲する。英語は文法と、削れる語を点検する。
6. **リポジトリを整える**: 下の「リポジトリの整備」で、足りないファイルと About の設定を調べ、足す。
7. **確かめる**: バッジの URL（バナーがある場合はバナーの URL も）が 200 を返すこと、リンク切れがないことを確認する。GitHub 上の表示を見られないときは、見ていないと報告する。

## 構成

上から順に、次の章を並べます。

1. 言語切替（`English | 日本語`、中央寄せ）と、その下のタイトル（`<h1>`）。バナーを付ける場合は、言語切替の上に置く（角丸、幅いっぱい）
3. キャッチコピー（太字の1文）と、短い説明（1〜2文）
4. バッジ行
5. 目次リンク（Quick start · Tools · Safety · Roadmap）
6. 概要: 何ができるか、頼み方の例
7. 特長: 箇条書き
8. Quick start: 必要なもの、インストール、設定、試し方
9. ツール／機能: 長い表は `<details>` に入れて、冒頭を短くする
10. 設定
11. 安全のために: WARNING や CAUTION の Alert
12. 今後の予定（実装済みの項目は載せない）
13. ライセンス

## バナー（任意）

付けてよい: 画面や UI の図柄（罫線のグリッド、ワイヤーフレーム、実際の画面）を暗くして、大きなタイトルを重ねたもの（基準は dark-landing-skill のバナー）。
付けない: コマンドやコードの文字を並べただけの画像（ターミナル画面の画像化、コード断片の背景）。文字だけ、単色の板、図柄が貧弱で見栄えのしないものも付けない。
迷うときは付けない。

- 2400×800 前後。角丸にして、プロジェクト名を大きな白字で重ねる。文字には控えめな影を付ける。
- 元になる画像は、そのプロジェクトの成果物の画像を使う。成果物が見た目のあるものなら、実物のレンダリングやスクリーンショットにする。
- 安いグラデーション、発光、汎用の立方体アイコン、意味のない抽象図形は使わない。AI が作った汎用画像に見えるため。
- `scripts/make-banner.py` が、元画像の暗転、角丸、文字の重ねを行う。使い方: `uv run --with pillow python <スキルのパス>/scripts/make-banner.py "プロジェクト名" [元画像] [出力]`（既定は `docs/images/hero.png` から `docs/images/banner.png`）。

## バッジ

shields.io の `style=flat-square` で統一し、バッジごとに固有の色とロゴを付ける。単色にそろえない。

| バッジ | 色の目安 |
|---|---|
| release | オレンジ `e8833a`、logo=github |
| CI | 既定の緑、logo=githubactions |
| license | 黄緑 `97ca00` |
| Bun | 薄い黄 `fbf0df`、logoColor=000000 |
| MCP | 紫 |
| Minecraft など対象 | 対象の色（Minecraft は緑 `62b47a`） |
| stars | 金 `e3b341` |
| last commit | 青 |

- 実在するリンクだけを付ける。X や Discord のように、持っていないものを置かない。
- ロゴは simple-icons にあるものだけ付ける。
- すべて `<a>` で包み、正しいリンク先を付ける。

## Alert

GitHub の Alert 記法で、意味のある所にだけ色を付ける。

| 種類 | 使う場面 |
|---|---|
| `> [!NOTE]` | 補足、未検証の範囲、仕様の限界 |
| `> [!TIP]` | 便利な使い方 |
| `> [!IMPORTANT]` | 挙動の変更、必須の設定 |
| `> [!WARNING]` | 危険な操作、暗号化されない通信 |
| `> [!CAUTION]` | データの消失など、取り返しのつかないこと |

絵文字は使わない。Alert を多用せず、1節に1〜2個までにする。

## リポジトリの整備

README を作る・作り直すときは、README だけで終わらせず、GitHub の画面に出るものを見直す。README の横にタブとして出るもの（Code of conduct・Contributing・License・Security）は、ファイルを置けば自動で出る。足りなければ積極的に足す。ただし README の中には、これらの手順や本文を書かない（「守ること」のとおり、README は利用者向けだけにする）。

まず今の状態を調べる。

```sh
gh repo view --json description,homepageUrl,repositoryTopics,licenseInfo,hasIssuesEnabled,hasDiscussionsEnabled
ls LICENSE* SECURITY* CONTRIBUTING* CODE_OF_CONDUCT* CITATION* .github 2>/dev/null
```

| 項目 | 置き場所 | 方針 |
|---|---|---|
| ライセンス | `LICENSE`（License タブ） | 無ければ必ず足す。リポジトリの持ち主の自作なら、既定は MIT（著者は持ち主、年は初公開の年）。他人のコードを含む、または持ち主が決めていないときは、足す前にライセンスの種類を確認する。README 末尾の「ライセンス」章もそろえる |
| セキュリティ | `SECURITY.md`（Security タブ） | 配布物・ネットワーク通信・ファイル取得を扱うなら足す。脆弱性の報告先は、公開で書いてよい連絡先か GitHub の Private vulnerability reporting にする。対応する版も書く |
| コントリビュート | `CONTRIBUTING.md`（Contributing タブ） | 外から Issue や PR を受けるなら足す。短く書く（Issue の出し方、PR の前に確かめること、ビルドとテストの方法）。ビルド手順などの開発者向けの内容は、README ではなくここに置く |
| 行動規範 | `CODE_OF_CONDUCT.md`（Code of conduct タブ） | コミュニティを作りたい公開リポジトリだけ。Contributor Covenant を使い、連絡先は公開してよいものにする。小さな個人ツールでは足さない |
| Issue テンプレート | `.github/ISSUE_TEMPLATE/bug_report.yml`・`feature_request.yml`・`config.yml` | Issue を受けるなら足す。バグ報告には版・環境・再現手順の欄を設ける。質問の誘導先があれば `config.yml` に書く |
| PR テンプレート | `.github/PULL_REQUEST_TEMPLATE.md` | PR を受けるなら短く足す |
| リリースノートの分類 | `.github/release.yml` | リリースを切るリポジトリなら足す（機能・修正などの分類） |
| 引用 | `CITATION.cff`（Cite this repository） | 研究や論文で使われうるものだけ |
| スポンサー | `.github/FUNDING.yml` | 持ち主が支援の窓口を持っているときだけ。持っていないものは置かない |
| 依存の更新 | `.github/dependabot.yml` | 依存を持つプロジェクトなら足す |
| コードの持ち主 | `.github/CODEOWNERS` | 複数人で管理するときだけ |

About（リポジトリの右上の説明）も設定する。README と矛盾しない短い説明、ホームページ、topics を入れる。

```sh
gh repo edit --description "<1 文の説明>" --homepage "<URL>" --add-topic <topic1> --add-topic <topic2>
```

- 説明は、README のキャッチコピーと同じ内容を、英語 1 文にする。
- topics は 5〜10 個。対象（minecraft・paper-plugin など）、言語、種類（cli・library など）を入れる。
- 公開先（Modrinth・npm・Releases など）があれば、`--homepage` に入れる。
- Discussions は、質問を受けたいときだけ `gh repo edit --enable-discussions` で有効にする。
- ソーシャルプレビュー画像は GitHub の画面（Settings）からしか設定できないので、バナーを使うときは、設定が必要だと利用者に伝える。

置くファイルと設定は、事実と合わせる。連絡先、対応版、ライセンスの名義、URL を、リポジトリの実際の内容と照合する。持っていない連絡先や、使っていない機能は書かない。ファイルを足したら、コミット（AI の名前は入れない）して push する。README の中に、足したファイルへのリンクを必要以上に並べない。

## 守ること

- **README は利用者向けだけにする**: 使う人が知りたいこと（何ができるか、入れ方、使い方、設定、安全上の注意、対応環境）だけを書く。次のものは書かない。
  - 開発者向けの内容: ソースからのビルド手順、開発環境の構築、テストの実行、内部の設計やアーキテクチャ、コントリビュートの手順。必要なら `CONTRIBUTING.md` か別の文書に分ける。
  - 公開・運用側の手順: リリースやタグの切り方、配布先（Modrinth、npm など）への公開手順、CI や自動公開の設定、トークン・secret・variable の設定。
  - 書き手や作業の事情: 「オーナーが確認」のような社内向けの言い方、作業の経緯、AI や担当者への指示。確認状況を書くときは「作者が確認」のように、読む人に通じる言い方にする。
  - 迷ったら「この文は、このソフトを使う人が読んで役に立つか」で判断し、役に立たなければ削る。
- **タイトルはリポジトリ名にしない**: `<h1>` とバナーの文字には、人が読む自然な表示名を使う（`readme-skill` → `README Creator SKILL`、`mcp-minecraft-controller` → `Minecraft Controller MCP`）。英語は単語の頭を大文字にし、ハイフンを外す。日本語版も同じ表示名にする。リポジトリ名は、URL、clone のパス、バッジの URL にだけ使う。バナー生成時の引数にも表示名を渡す。
- **事実を優先する**: ツール名、上限値、設定名は、コードと照合する。実機で試していないことは、未検証と書く。
- **比喩や宣伝文句を避ける**: 「革命的」「究極の」などの語を使わない。結論から書く。
- **英日で同じ構成にする**: 片方だけに章や表を足さない。
- **小さな変更は PR にしない**: README の修正は、利用者の許可があれば main へ直接コミットしてよい。
- **AI の名前を入れない**: コミットメッセージにも、README にも、Claude や Co-Authored-By を書かない。
- **改名したときは**: README の URL、clone のパス、バッジの URL をすべて直す。
