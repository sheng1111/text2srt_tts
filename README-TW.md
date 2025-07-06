# text2srt_tts

[![Version](https://img.shields.io/badge/Version-v1.1.2-blue.svg)](https://github.com/sheng1111/text2srt_tts)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue?style=flat-square&logo=python)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?style=flat-square&logo=streamlit)](https://text2tts.streamlit.app)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](https://opensource.org/licenses/MIT)
[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/sheng1111/text2srt_tts)
[![Docker](https://img.shields.io/badge/Docker-Supported-blue?style=flat-square&logo=docker)](https://docker.com/)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sheng1111/text2srt_tts/blob/main/colab_run.ipynb)

一鍵將文字轉換為高品質語音（WAV & MP3）與精準字幕（SRT），並在現代化單頁式 Streamlit UI 中提供即時預覽和下載功能。具備智能文字分割、雙語言支援和側邊欄控制的增強使用者體驗。

## 🆕 v1.1.0 新功能

- **🎨 單頁式介面**：現代化側邊欄佈局，自動適應深色/淺色主題
- **🧠 增強字幕生成**：先進的標點符號處理和智能文字分割
- **🌐 雙語言支援**：繁體中文與英文間無縫切換
- **📊 即時回饋**：即時字數統計、進度追蹤和狀態指示器
- **🔧 改良 Docker**：優化容器化配置，包含健康檢查和持久化儲存
- **💡 智能間距**：自動間距修正和標點符號保留選項
- **🎛️ 側邊欄控制**：所有設定整理在可展開的側邊欄中，提供更好的工作流程

## ✨ 核心功能

### 🎤 文字轉語音 (TTS) 引擎

- **預設引擎 (免費)**：`Edge TTS` - Microsoft Edge 內建語音合成，無需 API 金鑰
- **高級引擎 (選用)**：`Azure Speech Service` - 專業級自然語音合成
- **自動備援**：Azure 失敗時自動切換到 Edge TTS
- **語音客製化**：可調整語速（-50% 到 +50%）、音調和音量參數
- **詞邊界擷取**：精確的時間資訊，完美同步字幕

### 📜 智能字幕生成

- **智能文字分割**：考慮自然語言斷點和標點符號的進階演算法
- **標點符號控制**：選擇是否在字幕中保留或移除標點符號
- **間距優化**：自動修正標點符號和引號周圍的間距問題
- **彈性行長度**：可配置的字幕行字數限制（20-80 字）
- **自然斷點**：檢測句子結尾、轉折詞和語音停頓
- **多語言支援**：針對中文和英文文字處理優化

### 🖥️ 現代化單頁式介面

- **側邊欄佈局**：所有設定整理在可展開的側邊欄中，提供清晰的工作流程
- **主題自適應**：自動適應 Streamlit 的深色/淺色主題模式
- **即時狀態**：即時字數統計、生成進度和狀態指示器
- **雙語言介面**：在側邊欄中切換繁體中文和英文
- **快速提示**：可展開的幫助區段，提供使用建議
- **響應式設計**：針對各種螢幕尺寸和設備優化

### 🚀 部署選項

- **Streamlit 網頁應用**：具有側邊欄控制的互動式單頁介面
- **增強 Docker**：優化的容器化配置，包含健康檢查和持久化卷
- **Docker Compose**：完整的編排設定，包含網路和環境管理
- **命令列介面**：自動化批次處理功能
- **Google Colab**：無需本地設定的雲端執行

## 📸 介面預覽

### 單頁式佈局與側邊欄控制

![現代化介面](docs/img/setting.png)

### 生成結果與下載

![結果介面](docs/img/result.png)

## 🏗️ 專案架構

```
text2srt_tts/
├── app/
│   ├── services/              # 核心業務邏輯
│   │   ├── voice.py          # TTS 合成 (Azure & Edge)
│   │   └── subtitle.py       # 增強字幕生成
│   ├── ui/                   # 使用者介面元件
│   │   └── gui.py           # 單頁式 Streamlit 應用
│   ├── utils/               # 工具函式
│   │   └── text_to_srt.py   # SRT 格式化工具
│   └── cli/                 # 命令列介面
│       └── __main__.py      # CLI 入口點
├── locales/                 # 國際化
│   ├── zh_TW.toml          # 繁體中文
│   └── en.toml             # 英文
├── docker/                  # Docker 配置
├── docs/                    # 文件資源
│   └── img/                # 截圖和圖片
├── task/                    # 生成的輸出檔案
│   └── {task_id}/          # 個別任務結果
├── tests/                   # 單元測試
├── Dockerfile              # 優化的 Docker 配置
├── docker-compose.yml      # 完整編排設定
├── .dockerignore           # Docker 建置優化
├── config.example.toml      # 配置範本
├── requirements.txt         # Python 依賴
└── README.md               # 此檔案
```

## 🚀 快速開始

### 1. 本地安裝

```bash
# 克隆儲存庫
git clone https://github.com/sheng1111/text2srt_tts.git
cd text2srt_tts

# 建立虛擬環境
python3 -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# 安裝依賴
pip install -r requirements.txt

# 啟動應用
streamlit run app/ui/gui.py
```

### 2. Docker 部署（推薦）

#### 使用 Docker Compose 快速設定

```bash
# 克隆並進入專案目錄
git clone https://github.com/sheng1111/text2srt_tts.git
cd text2srt_tts

# 使用 Docker Compose 啟動
docker-compose up --build

# 在 http://localhost:8501 存取應用
```

#### 手動 Docker 建置

```bash
# 建置映像
docker build -t text2srt_tts .

# 執行容器
docker run -p 8501:8501 -v ./task:/app/task text2srt_tts

# 使用環境變數
docker run -p 8501:8501 \
  -e AZURE_KEY="your-key" \
  -e AZURE_REGION="your-region" \
  -v ./task:/app/task \
  text2srt_tts
```

### 3. 配置（選用）

```bash
# 複製配置範本
cp config.example.toml config.toml

# 編輯配置檔案
# - 添加 Azure 憑證以使用高級 TTS（選用）
# - 配置語音選項和偏好設定
# - 設定 FFmpeg 路徑（MP3 輸出需要）
```

## 🔧 配置選項

### 語音設定

在 `config.toml` 中配置可用語音：

```toml
[voices]
"中文女聲" = { name = "zh-CN-XiaoxiaoNeural" }
"中文男聲" = { name = "zh-CN-YunxiNeural" }
"英文女聲" = { name = "en-US-AriaNeural" }
"英文男聲" = { name = "en-US-GuyNeural" }
```

### Azure TTS 設定（選用）

用於高級品質語音合成：

```toml
AZURE_KEY = "your-azure-key"
AZURE_REGION = "your-region"
```

### Docker 環境變數

在 `.env` 檔案中設定 Docker 部署變數：

```bash
# Azure TTS（選用）
AZURE_KEY=your-azure-key
AZURE_REGION=your-region

# Streamlit 配置
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=0.0.0.0
```

## 💡 使用技巧

### 單頁式介面

- **側邊欄控制**：所有設定都整理在左側邊欄中
- **主題適應**：介面自動適應您的 Streamlit 主題偏好
- **語言切換**：使用側邊欄頂部的語言選擇器
- **進度追蹤**：在主區域觀看生成過程的即時進度

### 文字輸入最佳實務

- 使用適當的標點符號來實現自然停頓
- 保持句子清晰簡潔以獲得更好的分割
- 避免過多特殊字符
- 先用較短的文字測試以獲得最佳效果

### 字幕優化

- **標點符號保留**：在側邊欄切換是否保留或移除標點符號
- **行長度**：根據內容類型調整（手機用 20-40，桌面用 40-80）
- **自然斷點**：演算法自動檢測句子結尾和轉折詞
- **間距控制**：自動修正標點符號和引號周圍的間距

### 語音參數調整

- **語速**：-50% 到 +50%（負值減慢，正值加快）
- **音調**：-50% 到 +50%（負值降低，正值提高）
- **音量**：-50% 到 +50%（負值降低，正值提高）

## 🌐 多語言支援

應用支援：

- **介面語言**：繁體中文 (zh_TW)、英文 (en)
- **文字處理**：針對中文和英文內容優化，包含適當的標點符號處理
- **語音選項**：通過側邊欄選擇多種語言特定語音

使用側邊欄的語言區段中的下拉選單切換語言。

## 🐳 Docker 功能

### 增強容器化

- **多階段建置**：優化映像大小和更快的建置速度
- **健康檢查**：應用健康狀態的自動監控
- **非 root 使用者**：使用專用應用使用者增強安全性
- **持久化儲存**：為生成檔案提供卷掛載
- **環境管理**：通過環境變數完整配置

### 生產就緒

- **資源優化**：高效的記憶體和 CPU 使用
- **自動重啟**：容器在失敗時自動重啟，除非手動停止
- **網路隔離**：專用 Docker 網路提供安全性
- **日誌管理**：結構化日誌用於監控和除錯

## 📊 效能與限制

### 效能特性

- **處理速度**：每分鐘語音約 5-10 秒處理時間
- **記憶體使用**：根據文字長度約 100-500MB
- **儲存空間**：每分鐘生成內容約 1-5MB
- **容器大小**：包含所有依賴的約 800MB Docker 映像

### 目前限制

- 最大文字長度：每次生成約 10,000 字
- 支援的音訊格式：WAV（預設）、MP3（需要 FFmpeg）
- 需要網路連線進行 TTS 合成
- 側邊欄需要最小螢幕寬度以獲得最佳顯示

## 🧪 測試

執行測試套件：

```bash
# 啟動虛擬環境
source .venv/bin/activate

# 執行所有測試
pytest

# 執行特定測試模組
pytest tests/test_subtitle.py
pytest tests/test_voice.py

# 執行覆蓋率測試
pytest --cov=app tests/
```

## 🤝 貢獻

我們歡迎貢獻！請參閱貢獻指南：

1. Fork 儲存庫
2. 建立功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交變更 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

### 開發環境設定

```bash
# 安裝開發依賴
pip install -r requirements-dev.txt

# 執行程式碼檢查
flake8 app/
black app/

# 執行類型檢查
mypy app/

# 本地測試 Docker 建置
docker build -t text2srt_tts:dev .
docker run -p 8501:8501 text2srt_tts:dev
```

## 📝 更新日誌

### v1.1.0（目前版本）

- 具有側邊欄控制的單頁式介面
- 增強的 SRT 生成與標點符號處理
- 主題自適應設計（深色/淺色模式支援）
- 改良的 Docker 部署與健康檢查
- 即時進度追蹤和狀態指示器
- 更好的錯誤處理和使用者回饋
- 優化的間距和文字處理演算法

### v1.0.1

- 初始版本，基本 TTS 和字幕生成
- 分頁式 Streamlit 介面
- Azure 和 Edge TTS 支援
- 基本 Docker 部署

## 📄 授權

本專案採用 MIT 授權條款 - 詳情請參閱 [LICENSE](LICENSE) 檔案。

## 🙏 致謝

- **Microsoft Edge TTS**：免費語音合成服務
- **Azure 認知服務**：高級 TTS 功能
- **Streamlit**：現代化網頁應用框架
- **Docker**：容器化平台
- **Python 社群**：優秀的程式庫和工具

## 📞 支援

- **文件**：[GitHub Wiki](https://github.com/sheng1111/text2srt_tts/wiki)
- **問題回報**：[GitHub Issues](https://github.com/sheng1111/text2srt_tts/issues)
- **討論**：[GitHub Discussions](https://github.com/sheng1111/text2srt_tts/discussions)

---

**⭐ 為此專案加星** 如果它幫助您創建更好的字幕和語音內容！
