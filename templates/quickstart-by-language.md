# 言語・種類別の Quick start とバッジ

README の「Quick start」と、バッジ行の言語バッジに使う。実際のコマンドは、package.json・pyproject.toml・Cargo.toml・go.mod・build.gradle などを読んで確かめた値にする（書いてあるものだけ書く）。

| 種類 | インストール | 実行 | バッジ（shields.io、`style=flat-square`） |
|---|---|---|---|
| Node（Bun） | `bun add <pkg>` / `bunx <pkg>` | `bun run <script>` | Bun: `color=fbf0df&logo=bun&logoColor=000000` |
| Node（pnpm / npm） | `pnpm add <pkg>` / `npm i <pkg>` | `pnpm <script>` | npm: `img.shields.io/npm/v/<pkg>?color=cb3837&logo=npm` |
| Python | `uv tool install <pkg>` / `uv add <pkg>` | `uvx <pkg>` | PyPI: `img.shields.io/pypi/v/<pkg>?color=3775a9&logo=pypi&logoColor=white` |
| Rust | `cargo install <crate>` | `cargo run` | crates.io: `img.shields.io/crates/v/<crate>?color=e6732a&logo=rust` |
| Go | `go install <module>@latest` | `<command>` | Go: `img.shields.io/github/go-mod/go-version/OWNER/REPO?color=00add8&logo=go&logoColor=white` |
| Docker | `docker pull <image>` | `docker run --rm <image>` | Docker: `img.shields.io/docker/v/<image>?color=2496ed&logo=docker&logoColor=white` |
| Java / Gradle（Minecraft プラグインなど） | Releases から jar を入れる | サーバーを再起動する | 対象のゲーム（Minecraft は `62b47a`）と Java の版 |
| Web アプリ | URL を開く / `docker compose up` | — | デプロイ先（Vercel・Cloudflare など） |

- 公開前のもの（まだ npm や PyPI に無いもの）のバッジは付けない。404 を返すバッジが並ぶため。
- ソースから入れる手順は、利用者が通常使う方法でないなら README に書かず、`CONTRIBUTING.md` に置く。
