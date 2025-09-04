def moving_average_crossover(df, short=10, long=50):
    df = df.copy()
    df['MA_Short'] = df['close'].rolling(short).mean()
    df['MA_Long'] = df['close'].rolling(long).mean()
    df['Signal'] = 0
    df.loc[df.index[short:], 'Signal'] = (df['MA_Short'][short:] > df['MA_Long'][short:]).astype(int)
    df['Position'] = df['Signal'].diff()
    return df