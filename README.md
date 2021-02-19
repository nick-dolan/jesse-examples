# ⚙ Custom indicators for Jesse

Custom indicators for [Jesse](https://github.com/jesse-ai/jesse) trading framework, mostly ports from [TradingView](https://www.tradingview.com/), and a simple strategy to show how to work with some of them. 

> **MA Streak**
>
> Port of:  [MA Streak Can Show When a Run Is Getting Long in the Tooth](https://www.tradingview.com/script/Yq1z7cIv-MA-Streak-Can-Show-When-a-Run-Is-Getting-Long-in-the-Tooth/)

> **Moving Average Cross**
>
> Port of: [Moving Average Cross](https://www.tradingview.com/script/PcWAuplI-Moving-Average-Cross/)

> **Momentum Pinball**
>
> Port of: [Momentum Pinball](https://tradingview.com/script/X9zMa5Fn-Momentum-Pinball/)

> **Zero-Lag Exponential Moving Average**
>
> Can receive a custom source array.

> **Zero Lag Keltner Channels**
>
> Port of: [Zero Lag Keltner Channels](https://www.tradingview.com/script/CTzNAuUH-Zero-Lag-Keltner-Channels/)

> **Zero Lag Bollinger Bands**
>
> This is [Bollinger](https://www.tradingview.com/scripts/bollingerbands/) Bands (BB) with Zero Lag Moving Average (ZLEMA as base).

> **Percent Change Channel**
>
> Percent Change Channel is like KC unless it uses percentage changes in price to set channel distance. Original presented [here](https://www.tradingview.com/script/6wwAWXA1-MA-Streak-Change-Channel/). Example of signal you can find in  [IndicatorsPreview](/strategies/IndicatorsPreview/__init__.py).

#### Bulk import

The script provides a way to bulk import the candles for all defined trading pairs. Thanks to [macd2](https://forum.jesse.trade/d/83-bulk-candle-import) user.

To start, set up: exchange, start_date, and pairs inside the `bulk_import.py` file, then type:

```
python bulk_import.py
```

#### FinTA (Financial Technical Analysis)

See `FintaExamples` strategy to see how to connect third party technical indicators library [FinTA](https://github.com/peerchemist/finta). In FinTA, there're some indicators that are not on the official Jesse's [list](https://docs.jesse.trade/docs/indicators/reference.html).



To run, type: `jesse backtest 2020-12-01 2020-12-31 --debug`

[Forum](https://forum.jesse.trade/d/208-custom-indicators-for-jesse)