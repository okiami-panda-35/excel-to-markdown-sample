# README

## オフライン環境での仮想環境構築

### オンライン環境での事前準備

```bash
# ロックファイル生成
uv lock

# requirements.txt形式でエクスポート
uv export --format=requirements-txt > requirements.txt

# 標準のpipでパッケージをダウンロード
pip download -r requirements.txt -d ./packages
```

### オフライン環境での構築

```bash
# 仮想環境作成
uv venv

# ローカルパッケージからインストール
uv pip install --find-links ./packages -r requirements.txt --no-index
```

### 移行用ファイル

以下のファイルをオフライン環境に持参：

- `requirements.txt`
- `packages/` ディレクトリ（ダウンロードしたwheel/tarballファイル）
- `pyproject.toml` (プロジェクト設定)

### スクリプト実行

```bash
uv run .\src\excel_to_markdown.py
```
