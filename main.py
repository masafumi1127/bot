#ボット起動
def start(exchange,max_lot,lot,interval):

    print("paibot started! max_lot:{0}btc lot:{1}btc interval:{2}min".format(max_lot,lot,interval))

    while True:

        dt_now = datetime.now()
        
        #指定した時間間隔ごとに実行
        if dt_now.minute % interval == 0:

            try:

                #全注文をキャンセル
                exchange.cancelallchildorders(product_code="FX_BTC_JPY")

                #OHLCV情報を取得
                df_bf_fx = get_bitflyer_ohlcv("FX_BTC_JPY","15T")  # 5分足なら15Tを5Tに
                df = df_bf_fx.dropna()

                #特徴量計算
                df_features = calc_features(df)

                #モデル読み込み
                model_y_buy = joblib.load('./model/model_y_buy_bffx.xz')
                model_y_sell = joblib.load('./model/model_y_sell_bffx.xz')

                #推論
                df_features["y_predict_buy"] = model_y_buy.predict(df_features[features])
                df_features["y_predict_sell"] = model_y_sell.predict(df_features[features])

          
                #注文処理等
          

            except Exception as e:
                print(traceback.format_exc())
                pass

        time.sleep(60)
