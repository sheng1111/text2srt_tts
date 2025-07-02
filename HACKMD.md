# `text2srt_tts` 專案：文字轉語音與字幕自動生成工具

這個工具旨在將文字轉換為高品質語音，並自動生成精準的 SRT 字幕檔。

## 💡 核心功能

*   **文字轉語音 (TTS)**：
    *   支援 WAV 和 MP3 格式。
    *   **預設免費引擎**：使用 Microsoft Edge 瀏覽器內建的 `Edge TTS`，無需 API 金鑰。
    *   **高品質選用引擎**：支援 `Azure Speech Service`，提供更自然的語音（需自行申請 API 金鑰）。
    *   **智慧備援**：若 Azure TTS 失敗，自動切換至 Edge TTS。
    *   可調整語速、語調、音量。
*   **SRT 字幕生成**：
    *   根據語音單詞邊界，自動生成精準時間軸的 SRT 字幕。
    *   可設定每行最大字數，優化字幕顯示。
*   **直覺網頁介面 (Streamlit)**：
    *   提供友善的網頁操作介面，支援文字輸入、語音選擇、參數調整。
    *   即時預覽語音與字幕效果。
    *   可直接下載生成的語音檔和字幕檔。
    *   每次生成結果會獨立儲存於 `task/{task_id}/` 目錄。
*   **多種使用模式**：網頁介面、Docker、命令列 (CLI)、Google Colab。

## 🎯 應用情境

我開發這個工具，主要為了解決以下內容創作需求：

*   **影片製作**：
    *   當您有影片素材，但缺乏旁白語音或不想手動打逐字稿時，可快速生成語音與字幕，直接套用至影片。
*   **內容有聲化**：
    *   將文章、部落格內容轉換為有聲書或 Podcast，方便讀者以聽覺方式吸收資訊。
*   **教學與簡報**：
    *   為線上課程、教學影片或簡報快速生成語音解說與字幕，提升製作效率。
*   **語音素材測試**：
    *   開發者或設計師可快速生成大量語音素材，用於應用程式或介面測試。

## 🛠️ 如何開始使用？

### 1. 取得專案

```bash
git clone https://github.com/sheng1111/text2srt_tts.git
cd text2srt_tts
```

### 2. 環境準備

建議使用 Python 虛擬環境：

```bash
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows (PowerShell 可能需執行 Set-ExecutionPolicy RemoteSigned -Scope Process)
pip install -r requirements.txt
```

### 3. (選用) 安裝 ffmpeg

若需生成 MP3 格式語音，請確保系統已安裝 `ffmpeg`。可從 [ffmpeg 官網](https://ffmpeg.org/download.html) 下載。

### 4. 設定 `config.toml` (選用)

複製範本並編輯：

```bash
cp config.example.toml config.toml
```

*   **Azure 金鑰**：若使用 Azure 語音服務，請填入 `AZURE_KEY` 和 `AZURE_REGION`。若留空，將自動使用 Edge TTS。
*   **ffmpeg 路徑**：若 `ffmpeg` 未在系統 PATH 中，請指定其絕對路徑。
*   **語音選項**：在 `[voices]` 區塊設定，參考 [Azure 語音服務文件](https://aka.ms/speech/voices/neural)。

## ▶️ 使用方式

### 網頁介面 (Streamlit)

啟動虛擬環境後執行：

```bash
source .venv/bin/activate
python -m streamlit run app/ui/gui.py
```

應用程式將在瀏覽器中開啟 (通常是 `http://localhost:8501`)。介面支援繁體中文（臺灣）與英文切換。

### 命令列介面 (CLI)

啟動虛擬環境後執行：

```bash
source .venv/bin/activate
python -m app.cli --text input.txt --lang zh-CN-XiaoxiaoNeural --out output_folder/
```

*   `--text`: 輸入文字檔案路徑。
*   `--lang`: 語音名稱（參考 `config.toml`）。
*   `--out`: 輸出目錄。

### Google Colab

點擊專案中的 Colab 連結 [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sheng1111/text2srt_tts/blob/main/colab_run.ipynb)，即可在雲端環境中直接運行，無需本地設定。

## 🧪 測試

啟動虛擬環境後執行單元測試：

```bash
source .venv/bin/activate
pytest
```

## 🤝 貢獻與授權

本專案為開源性質，歡迎透過 GitHub 提交 Issue 或 Pull Request 進行貢獻。專案採用 MIT 授權條款。
