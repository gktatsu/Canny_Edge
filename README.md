# Canny Edge Processor

ディレクトリ内の画像に対して一括でCannyエッジ検出を行い、元のディレクトリ構造を維持したままエッジ画像を生成します。処理に使用したパラメータは再現性のためJSONログに記録されます。

## インストール

```bash
pip install .
```

## 使い方

```bash
canny-edge \
  --input-dir /path/to/images \
  --output-dir /path/to/output \
  --lower-threshold 50 \
  --upper-threshold 150
```

### 追加パラメータ

- `--gaussian-ksize`: ガウシアンぼかしに用いる奇数のカーネルサイズ（デフォルト: 5）
- `--gaussian-sigma`: ガウシアンぼかしの標準偏差。指定しない場合はOpenCVの自動計算値。
- `--log-path`: JSONログファイルの出力パス（デフォルト: `<output-dir>/processing_log.json`）

コマンドは入力ディレクトリの構造を出力先でも維持します。既存のファイルは上書きされません。

## 開発

- Python 3.9以上
- 依存関係のインストール: `pip install -e .`
- すべてのオプションを確認するには `python -m canny_edge.cli --help`
