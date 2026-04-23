# 流程圖設計 - 猜數字遊戲系統

本文件根據 PRD 與系統架構設計，視覺化使用者的操作路徑與系統內的資料傳遞流程。

## 1. 使用者流程圖（User Flow）

描述玩家從進入遊戲到完成一局遊戲的完整路徑。

```mermaid
flowchart LR
    A([玩家開啟網頁]) --> B[首頁 / 遊戲畫面]
    B --> C{是否已初始化遊戲？}
    C -- 否 --> D[系統隨機產生數字 1-100]
    D --> E[等待玩家輸入]
    C -- 是 --> E
    
    E --> F[輸入數字並送出]
    F --> G{後端驗證與判斷}
    
    G -- 輸入無效\n(非數字或超出範圍) --> H[顯示錯誤提示]
    H --> E
    
    G -- 數字太大 --> I[顯示「太大」與歷史紀錄]
    I --> E
    
    G -- 數字太小 --> J[顯示「太小」與歷史紀錄]
    J --> E
    
    G -- 猜中數字 --> K[顯示成功訊息與總次數]
    K --> L[點擊「重新開始」]
    L --> D
```

## 2. 系統序列圖（Sequence Diagram）

以下描述「玩家送出猜測數字」到「畫面更新結果」的完整資料流互動。

```mermaid
sequenceDiagram
    actor User as 玩家
    participant Browser as 瀏覽器
    participant Flask as Flask Route
    participant Session as Flask Session
    participant DB as SQLite (排行榜)
    
    User->>Browser: 填寫數字並點擊「猜測」
    Browser->>Flask: POST /guess (傳遞 guess 變數)
    
    Flask->>Session: 讀取正確答案 (target_number) 與嘗試次數
    
    alt 輸入驗證失敗
        Flask-->>Browser: 重新渲染頁面並帶有錯誤提示 (如：請輸入 1-100 數字)
    else 驗證成功
        Flask->>Flask: 比較 guess 與 target_number
        Flask->>Session: 更新嘗試次數 (attempts += 1) 與歷史紀錄清單
        
        alt 猜中數字
            Flask->>Session: 標記遊戲狀態為「已結束」
            opt 進入排行榜 (Nice to have)
                Flask->>DB: INSERT INTO leaderboard (玩家名稱, 猜測次數)
                DB-->>Flask: 儲存成功
            end
        end
        
        Flask->>Flask: 透過 Jinja2 結合最新狀態渲染模板
        Flask-->>Browser: 回傳更新後的 HTML
        Browser-->>User: 顯示「太大 / 太小 / 正確」提示與最新歷史紀錄
    end
```

## 3. 功能清單對照表

列出目前系統主要功能的 URL 路由對應設計，供後續 API (`/api-design`) 與路由實作參考。

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| --- | --- | --- | --- |
| **進入遊戲首頁** | `/` | `GET` | 顯示主畫面。若 Session 無進行中狀態，則自動初始化隨機數字。 |
| **提交猜測數字** | `/guess` | `POST` | 接收表單傳來的數字，判斷大小並更新 Session，最後渲染回首頁。 |
| **重新開始遊戲** | `/restart` | `POST` | 清除 Session 中的當局遊戲狀態，並重導向回 `/` 開啟新局。 |
| **(選用) 最佳成績排行榜**| `/leaderboard` | `GET` | 從 SQLite 讀取前 10 名最佳成績並顯示。 |
