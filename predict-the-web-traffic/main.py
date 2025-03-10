def solve_arima(data: list[int]) -> None:
    from statsmodels.tsa.arima.model import ARIMA

    model = ARIMA(data, order=(1, 1, 1)).fit()
    forecast = model.forecast(steps=30)
    [print(int(x.round())) for x in forecast]


def solve_sarima(data: list[int]) -> None:
    from statsmodels.tsa.statespace.sarimax import SARIMAX

    model = SARIMAX(data, order=(0, 1, 0), seasonal_order=(2, 1, 0, 7)).fit()
    forecast = model.forecast(steps=30)
    [print(int(x.round())) for x in forecast]


def solve_auto_arima(data: list[int]) -> None:
    import pmdarima

    model = pmdarima.auto_arima(data, seasonal=False)
    print(model.summary())
    forecast = model.predict(n_periods=30)
    [print(int(x.round())) for x in forecast]


if __name__ == "__main__":
    n_days = int(input())
    traffics = [int(input()) for _ in range(n_days)]
    # solve_auto_arima(traffics)
    solve_arima(traffics)
    # solve_sarima(traffics)
