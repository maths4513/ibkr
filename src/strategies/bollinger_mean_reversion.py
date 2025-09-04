def bollinger_mean_reversion(df, window=20, num_std=2):
    df = df.copy()
    df['MA'] = df['close'].rolling(window).mean()
    df['STD'] = df['close'].rolling(window).std()
    df['Upper'] = df['MA'] + num_std * df['STD']
    df['Lower'] = df['MA'] - num_std * df['STD']
    df['Signal'] = 0
    df.loc[df['close'] < df['Lower'], 'Signal'] = 1
    df.loc[df['close'] > df['Upper'], 'Signal'] = -1
    df['Position'] = df['Signal'].shift()
    return df