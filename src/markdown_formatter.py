import re
import sys
import os

def format_markdown_table(input_file_path):
    """
    指定されたMarkdownファイルからテーブルを読み込み、
    指定された形式に変換したMarkdown文字列を返します。
    """
    try:
        with open(input_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except FileNotFoundError:
        print(f"エラー: ファイルが見つかりません - {input_file_path}", file=sys.stderr)
        return ""
    except Exception as e:
        print(f"エラー: ファイルの読み込み中に問題が発生しました - {e}", file=sys.stderr)
        return ""

    output_lines = []
    
    is_previous_line_heading = False # 直前の出力行が見出しだったかどうかを記憶

    for line in lines:
        stripped_line = line.strip()

        # テーブルの行を処理
        if stripped_line.startswith('|') and stripped_line.endswith('|'):
            # ヘッダーセパレーター行をスキップ (例: |---|---|)
            if re.match(r'^\|\s*-+\s*\|(?:\s*-+\s*\|)*\s*$', stripped_line): # 修正された正規表現
                continue

            # 各列のコンテンツを抽出
            # split('|') は最初と最後に空文字列を生成するので、[1:-1] で実際のコンテンツ部分を取得
            parts = [p.strip() for p in stripped_line.split('|')]
            content_parts = parts[1:-1] 
            
            content = ""
            current_table_column_index = -1 # コンテンツが見つかった列の0-indexedインデックス
            for i, part in enumerate(content_parts):
                if part:
                    content = part
                    current_table_column_index = i 
                    break
            
            if content:
                # 見出しの正規表現: 1. , 1.1. , 1.1.1. の形式を判定
                # 例: "1. ", "1.1. ", "1.1.1. "
                heading_match = re.match(r'^(\d+\.)+\s.*$', content)
                
                if heading_match:
                    # 見出しはインデントなしで出力
                    output_lines.append(content)
                    is_previous_line_heading = True # 次の行が文章の場合にインデントを調整するため
                else:
                    # 文章の場合
                    actual_indent = 0
                    if is_previous_line_heading:
                        # 直前の行が見出しだった場合、現在の文章はインデントなし
                        actual_indent = 0
                    else:
                        # 直前の行が見出しでなかった場合、テーブルの列インデックスに基づいてインデントを決定
                        # 修正後の例から、テーブルの3列目 (index 2) はインデント0、4列目 (index 3) はインデント2
                        # これは `(current_table_column_index - 2) * 2` で計算できる
                        actual_indent = max(0, current_table_column_index - 2) * 2
                    
                    output_lines.append(f"{' ' * actual_indent}- {content}")
                    is_previous_line_heading = False # 文章を処理したらフラグをリセット
            
            # コンテンツが見つからなかった行（例: 空のテーブルセルのみの行）はスキップ
        
        # テーブル行ではない、かつ空行ではない行はスキップ

    return "\n".join(output_lines)

if __name__ == "__main__":
    input_dir = "doc/markdown/修正前/"
    output_dir = "doc/markdown/修正後/"

    # 出力ディレクトリが存在しない場合は作成
    os.makedirs(output_dir, exist_ok=True)

    for filename in os.listdir(input_dir):
        if filename.endswith(".md"):
            input_path = os.path.join(input_dir, filename)
            output_path = os.path.join(output_dir, filename)
            
            print(f"処理中: {input_path}")
            result_markdown = format_markdown_table(input_path)
            
            # ファイル名を先頭に追記 (拡張子なし)
            filename_without_ext = os.path.splitext(filename)[0]
            final_output_content = f"{filename_without_ext}\n\n{result_markdown}"

            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(final_output_content)
            print(f"保存済み: {output_path}")

    print("すべてのMarkdownファイルの処理が完了しました。")
