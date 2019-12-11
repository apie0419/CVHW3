# HW 3 檔案說明

使用 Python 3.6。請記計得打開 firewall。

## metric server 架設

在一臺有 static ip（我的是 `140.114.76.113`）的電腦上，開好 python 虛擬環境，裝好 Flask，然後執行：

```python
python server.py
```

他就會在 server port 5000。server 啟動時會先去讀正確答案 `test.csv`，請相對應的修改路徑。

## File server 架設

在一臺有 static ip（我的是 `140.114.76.113`）的電腦上，將要 server 的檔案都放於一個資料夾中，如：

```
files
├── ccpd6000.zip
├── pA1.csv
└── pA2.csv
```

然後於該資料夾中執行：

```python
python -m http.server
```

就在將檔案 serve 於 port 8000。在瀏覽器中輸入 `<ip>:8000/`（我的是 `140.114.76.113:8000/`） 即可看到。
需注意他無法同時 serve 多個 requests，所以可能遇到使用者等很久的情況。
解決的方法為提供一個備用的 server 來 serve 檔案，或使用 tornado 來 serve 檔案。
記得別把 `test.csv` 也丟進該資料夾。