# AGENTS.md

個人用 dotfiles。

最初に @README.md は読んでおくこと。

多くのファイルは `$HOME` のミラーとなっている。
`./setup/deployer/symlink.sh` にてシンボリックリンクを作成する。

自動テストは `./.github/workflows/test.yml` のみ。
CI ジョブでは GUI アプリケーションの設定などはテストできていない点に注意する。

`bash -n`, `zsh -n` などでの構文チェックは基本的に実行する。
その他のテストはケースバイケースで検討する。

全てを記載しているわけではなく重要なポイントのみ本リポジトリの構成を説明する

```plaintext
.
├── .zshrc               # zsh の entrypoint として .zsh/ を番号順に読み込み tmux を起動
├── .zsh/                # zsh の設定を関心ごとで分割して定義
├── .bash_profile        # bash 設定: SSH 先などで使う想定のミニマム定義
├── .bash_prompt         # bash プロンプト: SSH 先などで使う想定のミニマム定義
├── .vimrc               # vim 設定: SSH 先などで使う想定のミニマム定義
├── .tmux.conf           # tmux 設定
├── .ssh/                # SSH 設定
├── .gitattributes        # git filter の適用対象; .pi/agent/settings.json の diff ノイズ抑制
├── .pi/                 # Pi (pi-coding-agent) 設定: agent/keybindings.json と agent/settings.json のみ管理。auth.json や sessions/ などは端末固有のため管理しない
├── .config/             # 各アプリの設定
│   ├── aerospace/       # Aerospace 設定
│   ├── alacritty/       # Alacritty 設定: メインのターミナル
│   ├── git/             # Git フック定義
│   ├── karabiner/       # Karabiner 設定
│   ├── mise/            # mise 設定; メインの言語・ツールマネージャー
│   ├── nvim/            # Neovim 設定: メインのエディタ
│   ├── opencode/        # OpenCode 設定: cli.json (service.json は端末固有のため管理しない)
│   └── sheldon/         # zsh プラグイン定義
├── bin/                 # 自作スクリプト
├── docs/                # 本リポジトリに関するドキュメント
└── setup/               # マシンのセットアップスクリプト
    ├── deployer/        # 設定ファイルのデプロイ本体
    └── entrypoint/      # OS ごとの entrypoint
```

`.pi/agent/settings.json` は Pi が起動時に `lastChangelogVersion` や `extensionChangelogVersions` を書き戻すため、
commit 時だけそのキーを落とす git clean filter (`filter.pi-settings`) を `.gitattributes` で適用している。
filter の定義は `.gitconfig` 側にあり `jq` が必要。値は実ファイルに残るので Pi の挙動は変わらない。
working tree と index で実際の差分が出ないため、`git status` が一瞬 `M` を出しても `git diff` が空なら問題ない。
filter を後から有効化した場合は `git add --renormalize .pi/agent/settings.json` で入れ直す。
