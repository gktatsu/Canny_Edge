# Canny Edge Processor

ディレクトリ内の画像に対して一括でCannyエッジ検出を行い、元のディレクトリ構造を維持したままエッジ画像を生成します。処理に使用したパラメータは再現性のためJSONログに記録されます。

## 特徴

- **バッチ処理**: ディレクトリ内のすべての画像を一括処理
- **構造維持**: 入力ディレクトリの階層構造を出力先でも維持
- **スキップ機能**: 既存ファイルは上書きせずスキップ
- **詳細ログ**: 処理パラメータと結果をJSONログに記録（再現性確保）
- **柔軟な設定**: 閾値、ガウシアンぼかし、対象拡張子をカスタマイズ可能

## インストール

```bash
pip install .
```

開発用（編集可能モード）:

```bash
pip install -e .
```

## 依存関係

- Python >= 3.9
- opencv-python >= 4.8.0
- numpy >= 1.24.0

## 使い方

### 基本的な使用例

```bash
canny-edge \
  --input-dir /path/to/images \
  --output-dir /path/to/output \
  --lower-threshold 50 \
  --upper-threshold 150
```

### 全オプション指定例

```bash
canny-edge \
  --input-dir /path/to/images \
  --output-dir /path/to/output \
  --lower-threshold 50 \
  --upper-threshold 150 \
  --gaussian-ksize 7 \
  --gaussian-sigma 1.5 \
  --log-path /path/to/custom_log.json \
  --extensions .png .jpg .bmp
```

## コマンドラインオプション

| オプション | 必須 | デフォルト | 説明 |
|-----------|------|-----------|------|
| `--input-dir` | ✓ | - | 入力画像が格納されたディレクトリ |
| `--output-dir` | ✓ | - | エッジ画像の出力先ディレクトリ |
| `--lower-threshold` | ✓ | - | Cannyエッジ検出の下側閾値（ヒステリシス） |
| `--upper-threshold` | ✓ | - | Cannyエッジ検出の上側閾値（ヒステリシス） |
| `--gaussian-ksize` | - | 5 | ガウシアンぼかしのカーネルサイズ（奇数） |
| `--gaussian-sigma` | - | auto | ガウシアンぼかしの標準偏差（省略時はOpenCV自動計算） |
| `--log-path` | - | `<output-dir>/processing_log.json` | JSONログファイルの出力パス |
| `--extensions` | - | `.png .jpg .jpeg .tif .tiff` | 処理対象のファイル拡張子 |

## 処理の流れ

1. 入力ディレクトリから対象拡張子の画像を再帰的に収集
2. 各画像に対して以下を実行:
   - カラー画像をグレースケールに変換
   - ガウシアンぼかしを適用
   - Cannyエッジ検出を実行
   - 二値化してPNG形式で保存
3. 処理結果をJSONログに記録

## 出力

- **エッジ画像**: PNG形式の二値画像（0または255）
- **処理ログ**: JSON形式で以下を記録
  - タイムスタンプ
  - 入出力ディレクトリ
  - 使用パラメータ
  - 処理済みファイル一覧
  - スキップされたファイル一覧（理由付き）

## 注意事項

- `lower_threshold` は `upper_threshold` より小さい値を指定してください
- `gaussian-ksize` は正の奇数のみ有効です
- 既存の出力ファイルは上書きされずスキップされます
- ログファイルが既に存在する場合は追記されます

## ヘルプ

すべてのオプションを確認するには:

```bash
canny-edge --help
```

または:

```bash
python -m canny_edge.cli --help
```
