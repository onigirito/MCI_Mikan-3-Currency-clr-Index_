# Mikan 3-Currency clr Index データ算出仕様書（PPP年次版）v1.0

**対象通貨：USD・JPY・TRY**

---

## 重要な前提

**Mikan 3-Currency clr Index** は、PPPにロックされた道具ではなく、**K_i を差し替える汎用フレームワーク**である。

ただし、本仕様書では **PPP年次データ** を K_i として採用した実装例を示す。

---

## 0. 全体像

### 目的

USD・JPY・TRY の実データ（為替＋PPP）から、以下を算出する：

1. **PPP乖離率**
   - d_USDJPY (USD/JPY の PPP 乖離率)
   - d_USDTRY (USD/TRY の PPP 乖離率)

2. **Mikan 3-Currency clr Index の三通貨相対座標**
   - m[USD], m[JPY], m[TRY]

### 通貨の対応

- A = USD
- B = JPY
- C = TRY

以下の公式では、この A, B, C に対応して計算を行う。

---

## 1. 必要データと取得先

### 1-1. 必須データ（年次）

#### 1. PPP（GDPベース, LCU per intl $）

**ソース：** World Bank World Development Indicators
**指標コード：** PA.NUS.PPP（PPP conversion factor, GDP (LCU per international $)）

**取得対象国：**
- 日本：country = JPN
- トルコ：country = TUR

**解釈：**
- PPP_JPY(year) = その年の「1国際ドルあたり JPY」
- PPP_TRY(year) = その年の「1国際ドルあたり TRY」

「国際ドル」は USD PPP ベースなので、実務的には：
- USD/JPY の PPPフェアレート ≒ PPP_JPY
- USD/TRY の PPPフェアレート ≒ PPP_TRY

とみなして良い。

#### 2. 年平均の公定為替レート（LCU per USD, period average）

**ソース：** World Bank WDI／IMF IFS
**指標コード：** PA.NUS.FCRF（Official exchange rate (LCU per US$, period average)）

**取得対象国：**
- 日本（JPY per USD）：FX_JPY_USD(year)
- トルコ（TRY per USD）：FX_TRY_USD(year)

**記法：**
- S_USDJPY(year) = FX_JPY_USD(year)
- S_USDTRY(year) = FX_TRY_USD(year)

---

### 1-2. 任意（高頻度の分析をする場合）

**日次 or 月次 USD/JPY, USD/TRY スポットレート**

**ソース例：** 各国中銀、BIS、投資サイト（Investing.com, Refinitiv, etc.）

**記号：**
- S_USDJPY(t)：t日時点の USD/JPY
- S_USDTRY(t)：t日時点の USD/TRY

PPP は年次の PPP_JPY(year(t)), PPP_TRY(year(t)) をその年いっぱい固定で使う。

> ※最初の実装は「年次だけ」で十分。そのあと必要なら高頻度版に拡張、という二段階でOK。

---

## 2. 前処理

### 2-1. 時間軸の設定

**期間：** 少なくとも 2005–最新年（例：2025）

**年次データの場合：**
- 年 t ごとに、以下を揃える：
  - PPP_JPY(t), PPP_TRY(t)
  - S_USDJPY(t), S_USDTRY(t)

**高頻度データの場合：**
- 各時点 t について年を year(t) として、以下を対応させる：
  - PPP_JPY(year(t)), PPP_TRY(year(t))
  - S_USDJPY(t), S_USDTRY(t)

### 2-2. 単位確認

PA.NUS.PPP と PA.NUS.FCRF はどちらも **LCU per 1 USD/intl$** 形式。

よって、割り算はそのまま可能：
- S_USDJPY / PPP_JPY は次元的に無次元（比）になる
- S_USDTRY / PPP_TRY も同様

---

## 3. 基本計算：PPP乖離率 d_AB, d_AC

**通貨対応：** A = USD, B = JPY, C = TRY

### 3-1. ペア A–B（USD/JPY）

年次なら、各年 t について：

**実勢レート（スポット）：**
```
S_{AB}(t) = S_USDJPY(t)
```

**PPPフェアレート：**
```
F_{PPP,AB}(t) = PPP_JPY(t)
```

**PPP乖離率：**
```
d_{AB}(t) = ln( S_{AB}(t) / F_{PPP,AB}(t) )
          = ln( S_USDJPY(t) / PPP_JPY(t) )
```

### 3-2. ペア A–C（USD/TRY）

同様に：

**実勢レート：**
```
S_{AC}(t) = S_USDTRY(t)
```

**PPPフェアレート：**
```
F_{PPP,AC}(t) = PPP_TRY(t)
```

**PPP乖離率：**
```
d_{AC}(t) = ln( S_{AC}(t) / F_{PPP,AC}(t) )
          = ln( S_USDTRY(t) / PPP_TRY(t) )
```

ここで出てくるのが、**Mikan 3-Currency clr Index の入力となる 2 本**：
- d_AB(t) = d_{USDJPY}(t)
- d_AC(t) = d_{USDTRY}(t)

---

## 4. Mikan 3-Currency clr Index：三通貨相対座標 m[*] の算出

### Mikan 3-Currency clr Index の三通貨分解公式

**通貨対応：** A = USD, B = JPY, C = TRY

```
m[A](t) = ( d_{AB}(t) + d_{AC}(t) ) / 3
m[B](t) = ( -2·d_{AB}(t) + d_{AC}(t) ) / 3
m[C](t) = ( d_{AB}(t) - 2·d_{AC}(t) ) / 3
```

これを時系列で回せば、各時点 t について以下が得られる：
- m_USD(t) = m[A](t)
- m_JPY(t) = m[B](t)
- m_TRY(t) = m[C](t)

### 検算条件

常に以下が成り立つ：
```
m[A](t) + m[B](t) + m[C](t) = 0
```

---

## 5. 追加で出しておくと便利な派生量

### 5-1. 単純PPP乖離（TRY/JPY）

**実勢 TRY/JPY クロス：**
```
S_TRYJPY(t) = S_USDJPY(t) / S_USDTRY(t)
```

**PPPフェアレート（TRY/JPY）：**
```
F_{PPP,TRYJPY}(t) = PPP_JPY(t) / PPP_TRY(t)
```

**PPP乖離率（TRY/JPY）：**
```
d_TRYJPY(t) = ln( S_TRYJPY(t) / F_{PPP,TRYJPY}(t) )
```

### 5-2. Mikan 3-Currency clr Index との関係を確認する用

理論的には：
- d_TRYJPY(t) は E[TRY] - E[JPY] に相当
- m_TRY(t) - m_JPY(t) は「三通貨かご内での相対位置差」

これらもチェック用に、列を一緒に出しておくとよい。

---

## 6. 出力フォーマット（推奨仕様）

### 6-1. 年次CSVフォーマット案

**列の定義：**

1. **year**：西暦（int）
2. **S_USDJPY**：年平均 USD/JPY（float）
3. **S_USDTRY**：年平均 USD/TRY（float）
4. **PPP_JPY**：PPP_JPY(year)（float）
5. **PPP_TRY**：PPP_TRY(year)（float）
6. **d_USDJPY**：ln(S_USDJPY / PPP_JPY)
7. **d_USDTRY**：ln(S_USDTRY / PPP_TRY)
8. **m_USD**：Mikan Index m[A]
9. **m_JPY**：Mikan Index m[B]
10. **m_TRY**：Mikan Index m[C]
11. **S_TRYJPY**：S_USDJPY / S_USDTRY
12. **PPP_TRYJPY**：PPP_JPY / PPP_TRY
13. **d_TRYJPY**：ln(S_TRYJPY / PPP_TRYJPY)

### 6-2. サブセット出力

- **長軸用：** 2005–直近年のフル系列
- **レジーム用：** 2019–直近年だけを抜いたサブCSV
  - シムシェキ前後／2023以降の分布を見る用途

---

## 7. 実装上の注意

### 1. PPP の選択

基本は **PA.NUS.PPP（GDPベース）** で統一。

私的消費ベース（PA.NUS.PPPC）を使う場合は、全通貨で同じ指標に揃えること。

### 2. 欠損値

もし一部年で PPP or FX に欠損があれば：
- その年はスキップする
- または前後年で線形補間

### 3. 対数の基数

**ln は自然対数で統一。**

分布解析（平均・標準偏差）もこの ln 値で行う。

### 4. 単位の一貫性

すべて **「LCU per USD（or intl$）」** に統一されているか確認すること。

為替サイトから取った日次データは、USD/JPY, USD/TRY 方向をきちんと合わせる
（例：もし JPY/USD 形式なら逆数を取る）。

---

## 8. データ処理フロー（実装メモ）

> WDI から PA.NUS.PPP（JPN, TUR）と PA.NUS.FCRF（同じく JPN, TUR）の年次データを2005–最新年まで取得。

そこから上記ステップに従って：
- d_USDJPY(t), d_USDTRY(t)
- m_USD(t), m_JPY(t), m_TRY(t)

を年次時系列で計算。

さらに、d_TRYJPY(t) も出して、「単純PPP乖離」と「Mikan 3-Currency clr Index の三通貨相対座標」の両方を比較できるCSVを出力する。

---

## 9. K_i の差し替えについて（将来の拡張）

本仕様書では K_i = PPP（年次）を採用しているが、**Mikan 3-Currency clr Index は汎用フレームワーク**であり、以下のような K_i への差し替えが可能：

- **実質実効為替レート（REER）ベース**
- **ビッグマック指数ベース**
- **ULCベースのフェアレート**
- **その他の購買力平価指標**

K_i を差し替える場合は、本仕様書の第3章「基本計算」における F_{PPP,AB}(t), F_{PPP,AC}(t) を、選択した K_i による F_{Ki,AB}(t), F_{Ki,AC}(t) に置き換えればよい。

---

**文書バージョン：** v1.0
**最終更新日：** 2025-11-20
