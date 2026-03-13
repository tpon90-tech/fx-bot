import yfinance as yf
import datetime
import tweepy

# ===== X APIキー =====
API_KEY = "YOUR_API_KEY"
API_SECRET = "YOUR_API_SECRET"
ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
ACCESS_SECRET = "YOUR_ACCESS_SECRET"

client = tweepy.Client(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# ===== 通貨ペア =====
symbols = {
    "メキシコペソ": "MXNJPY=X",
    "南アランド": "ZARJPY=X",
    "トルコリラ": "TRYJPY=X"
}

def get_rate(symbol):
    data = yf.download(symbol, period="2d", interval="1d")
    today = data["Close"][-1]
    yesterday = data["Close"][-2]
    change = (today - yesterday) / yesterday * 100
    return today, change

def judge_trend(change):
    if change > 0.3:
        return "（強い）"
    elif change < -0.3:
        return "（下落続く）"
    else:
        return "（底堅い）"

# ===== 投稿文生成 =====
lines = ["【今日の高金利通貨まとめ】"]

for name, symbol in symbols.items():
    rate, change = get_rate(symbol)
    trend = judge_trend(change)
    lines.append(f"・{name}：{rate:.2f}円{trend}")

lines.append("金利だけでは判断できない相場。")
lines.append("だからこそ、レバ3×の規律で積み上げるスワップ戦略が効く👇")
lines.append("https://note.com/swap_discipline/n/nf4f50c311c6b")

post_text = "\n".join(lines)

# ===== Xへ投稿 =====
client.create_tweet(text=post_text)
print("投稿完了:", post_text)
