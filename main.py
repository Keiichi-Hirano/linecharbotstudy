#
from flask import Flask, request, abort ,current_app

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
import os
import sys
#from account_response import Response
# 共通変数_辞書
answer_y = {'はい', 'うん','そう','Yes','Y','ええ','だな','です','ええ','そだね'}

#
app = Flask(__name__)
#from flask import current_app as app
#インスタンス生成
#res=Response()

#環境変数取得
# LINE Developersで設定されているアクセストークンとChannel Secretをを取得し、設定します。
YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)

## 1 ##
#Webhookからのリクエストをチェックします。
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    # リクエストヘッダーから署名検証のための値を取得します。
    signature = request.headers['X-Line-Signature']
    # get request body as text
    # リクエストボディを取得します。
    body = request.get_data(as_text=True)
    #app.logger.info("Request body: " + body)
    current_app.logger.info("Request body: " + body)

    # handle webhook body
    # 署名を検証し、問題なければhandleに定義されている関数を呼び出す。
    try:
        handler.handle(body, signature)
    # 署名検証で失敗した場合、例外を出す。
    except InvalidSignatureError:
        abort(400)
    # handleの処理を終えればOK
    return 'OK'

## 2 ##
###############################################
#LINEのメッセージの取得と返信内容の設定(オウム返し)
###############################################
#def以下の関数を実行
# reply_messageの第一引数のevent.reply_tokenは、
# イベントの応答に用いるトークン。
# 第二引数には、linebot.modelsに定義されている
# 返信用のTextSendMessageオブジェクトを渡している。
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    # text = event.message.text
    #if ('レストラン' in text or 'ランチ' in text or 'ディナー' in text or '食べ物' in text) and ('おすすめ' in text or '教えて' in text):
    #else:
#    line_bot_api.reply_message(
#    event.reply_token,
#    TextSendMessage(text=os.environ[res.getResponse(event.message.text)])
#    ) #ここでオウム返しのメッセージを返す。
    ask_ddp = True
    sendtext = ''
    sendtext = sendtext + 'って言いました？' + '/n' + 'DDPのガイドラインについて確認ですか？'
    line_bot_api.reply_message(event.reply_token,TextSendMessage(text=sendtext)) #ここでオウム返しのメッセージを返す。
    while ask_ddp != False:
        sendtext = event.message.text
        if (sendtext in answer_y ):
            sendtext = '現在工事中です。って言いました？'
        else:
            sendtext = 'それ以外はお答えできませんぜ？（＋＋'
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text=sendtext)) #ここでオウム返しのメッセージを返す。
        ask_ddp = False
    else:
        sys.exit(1)

# ポート番号の設定
if __name__ == "__main__":
#    app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
