# UN NATURAL

日々の出来事を記録し、満足度や社会との関わりをグラフで振り返る Streamlit アプリです。

## GitHub にアップロードするファイル

このフォルダー内の次のファイルを GitHub リポジトリ `un-natural` の直下にアップロードしてください。

- `app.py`
- `requirements.txt`
- `.gitignore`
- `README.md`

個人の投稿データや設定ファイルはアップロードしないでください。

## ローカルで実行

Python 3.11 以降を用意し、プロジェクトフォルダーで次を実行します。

```powershell
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

表示された URL をブラウザーで開きます。

## Streamlit Community Cloud で公開

1. GitHub で `un-natural` という名前の**公開リポジトリ**を作成します。
2. 上記 4 ファイルをリポジトリ直下にアップロードして保存します。
3. [Streamlit Community Cloud](https://share.streamlit.io/) に GitHub アカウントでサインインします。
4. **Create app** を選び、リポジトリ `un-natural`、ブランチ `main`、起動ファイル `app.py` を指定してデプロイします。

## 投稿データとプライバシー

- 投稿履歴は Streamlit のブラウザーセッションごとに分けて、セッション中だけ保持します。他の利用者の画面とは共有されません。
- データベースを使わないため、セッション終了や再起動後に投稿履歴は引き継がれません。記録を長期保存する用途には使用しないでください。
- 公開アプリでは、氏名・住所などの個人情報や、外部に知られたくない内容を入力しないでください。
- このアプリの分析は振り返りの補助であり、医療・診断・専門家への相談の代わりではありません。
