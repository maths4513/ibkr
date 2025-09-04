from plotly import graph_objects as go

def plot_comparison(results):
    fig = go.Figure()
    for name, (equity, stats, df) in results.items():
        fig.add_trace(go.Scatter(x=df.index, y=equity, mode="lines", name=name))
    fig.update_layout(title="Strategy Comparison (Cumulative Returns)", xaxis_title="Date", yaxis_title="Equity")
    fig.show()