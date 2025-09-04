def rsi_strategy(df, window=14, lower=30, upper=70):
    df = df.copy()
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    RS = gain / loss
    df['RSI'] = 100 - (100 / (1 + RS))
    df['Signal'] = 0
    df.loc[df['RSI'] < lower, 'Signal'] = 1
    df.loc[df['RSI'] > upper, 'Signal'] = -1
    df['Position'] = df['Signal'].shift()
    return df