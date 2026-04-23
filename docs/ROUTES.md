# 路由設計 - 猜數字遊戲系統

本文件基於之前的 PRD、架構與資料庫設計，詳細規劃 Flask 的所有路由、對應的 Jinja2 模板，以及資料的輸入與輸出流程。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| --- | --- | --- | --- | --- |
| 遊戲首頁 | GET | `/` | `templates/game/index.html` | 顯示遊戲主畫面與歷史猜測紀錄。若 Session 無進行中遊戲，自動初始化。 |
| 提交猜測 | POST | `/guess` | — | 接收玩家猜測數字，判斷後更新 Session 狀態，並重導向回首頁。 |
| 重新開始 | POST | `/restart` | — | 清空當局 Session，重新開始一局新遊戲，並重導向回首頁。 |
| 排行榜 | GET | `/leaderboard` | `templates/leaderboard/index.html`| 顯示歷史最佳成績清單。 |

## 2. 每個路由的詳細說明

### 遊戲首頁 (GET `/`)
- **輸入**：讀取 Session 中的狀態 (`target_number`, `attempts`, `history`, `game_over`)。
- **處理邏輯**：如果 Session 裡沒有正在進行的遊戲（例如初次進入或剛按過重新開始），隨機產生 1-100 的數字存入 Session，並初始化猜測次數為 0，歷史紀錄為空陣列。
- **輸出**：渲染 `game/index.html`，並將 Session 中的狀態傳遞給模板進行渲染。
- **錯誤處理**：無特定錯誤，確保即使 Session 異常也能安全地重置為初始狀態。

### 提交猜測 (POST `/guess`)
- **輸入**：表單欄位 `guess`（玩家輸入的數字）。
- **處理邏輯**：
  1. 驗證輸入是否為合法的整數（1-100 之間）。
  2. 若不合法，透過 Flask `flash` 傳遞錯誤訊息。
  3. 若合法，將輸入數字與 Session 中的 `target_number` 比較，更新 `attempts` (+1)，並將結果（"太大"、"太小" 或 "正確"）與該次猜測數字加進 `history` 清單。
  4. 如果猜中（"正確"），將遊戲狀態改為結束，並將成績寫入 Leaderboard 資料表。
- **輸出**：重新導向 (`redirect`) 到 `/`，讓首頁重新渲染最新狀態。
- **錯誤處理**：若收到非整數，或是未初始化遊戲就收到猜測，皆重導向回 `/` 並顯示警告。

### 重新開始 (POST `/restart`)
- **輸入**：無。
- **處理邏輯**：清除 Session 中與遊戲相關的變數。
- **輸出**：重新導向 (`redirect`) 到 `/` 開啟新局。
- **錯誤處理**：無。

### 排行榜 (GET `/leaderboard`)
- **輸入**：無。
- **處理邏輯**：呼叫 `Leaderboard.get_top_scores(10)` 從 SQLite 資料庫取得前 10 名最佳成績。
- **輸出**：渲染 `leaderboard/index.html`，並將取得的成績資料傳遞給模板顯示。
- **錯誤處理**：若資料庫無資料，模板將顯示「目前尚無紀錄」。

## 3. Jinja2 模板清單

所有的模板將繼承自一個共用的 `base.html`，以保持視覺與導覽列的風格一致。

- `templates/base.html`：共用版型（包含 HTML `<head>`、CSS 檔案連結、網站共用 Header）。
- `templates/game/index.html`：遊戲主畫面，繼承 `base.html`。負責包含輸入表單、錯誤提示區塊、猜測歷史清單，以及成功猜中時才會出現的「重新開始」按鈕。
- `templates/leaderboard/index.html`：排行榜畫面，繼承 `base.html`。負責顯示最佳成績的表格。

## 4. 路由骨架程式碼

路由的 Python Blueprint 實作骨架已建立於 `app/routes/` 目錄中，分別為：
- `app/routes/game.py`
- `app/routes/leaderboard.py`
