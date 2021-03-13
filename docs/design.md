# dotfiles design

## アクター
- 反映したい人
- 更新したい人


## 反映したい環境
#### メイン機
エントリーポイント, GUIを使用する
十分な依存ライブラリと最大限カスタマイズした設定ファイル
git, zsh, fzy, neovim, tmux, nerd-font, asdf, chrome, slack

#### 開発機
ssh接続などで使用する, ある程度リッチな環境
開発に必要な依存ライブラリと設定ファイル
git, zsh, fzy, neovim, tmux, asdf?

#### 検証機など
ssh接続などで使用する, 必要最小限の環境
必要最低限の依存ライブラリと設定ファイル
git, vim


## ライブラリはどこまで自動インストールするか
#### CLI
CLIについては基本的に自動インストールで良いと思われる。
基本的にはzsh環境に付随させる形で良いと思われる。

#### GUI
メイン機のみなのでそこまで手間ではないだろう。
自動化しない方が良い気がする。