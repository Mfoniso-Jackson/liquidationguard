# LiquidationGuard

LiquidationGuard is a simple Streamlit risk calculator for futures traders. It helps traders estimate position size, account risk, margin required, and approximate liquidation distance before entering a trade.

The v0.1 MVP is intentionally focused: no exchange APIs, login, payments, charts, databases, AI, or exchange-specific margin logic. It is a pre-trade risk decision tool, not a trading platform.

## Setup

1. Create and activate a Python virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependencies.

```bash
pip install -r requirements.txt
```

3. Run the app.

```bash
streamlit run app.py
```

## Testing

Run the lightweight unit tests for the calculation and validation layers.

```bash
python -m unittest
```

The tests cover long and short calculations, safety status thresholds, high leverage warnings, liquidation-before-stop warnings, margin warnings, and invalid stop placement.

## Deploy with a Custom Domain

For `liquidationguard.app`, use a host that supports custom domains directly. Render is a simple option for this MVP.

### Render

1. Push this repository to GitHub.
2. Create a new Render Web Service from the GitHub repository.
3. Render can use `render.yaml`, or you can enter these settings manually:

```bash
Build Command: pip install -r requirements.txt
Start Command: streamlit run app.py --server.port $PORT --server.address 0.0.0.0
```

4. Deploy the service.
5. In Render, open the service settings and add these custom domains:

```text
liquidationguard.app
www.liquidationguard.app
```

6. Render will show the exact DNS records to add at your domain registrar. Add those records, then wait for DNS and SSL verification.

Use `www.liquidationguard.app` as an alias for the root domain so both URLs work.

## Deploy on Streamlit Community Cloud

1. Push this project to a GitHub repository.
2. Go to Streamlit Community Cloud and create a new app.
3. Select the repository, branch, and `app.py` as the main file.
4. Deploy.

The app only needs `streamlit` from `requirements.txt`.

## Project Structure

- `app.py` handles the Streamlit user interface.
- `risk_engine.py` handles calculations, warnings, safety status, and decision text.
- `validators.py` handles input validation.
- `requirements.txt` lists runtime dependencies.
- `render.yaml` configures Render deployment.
- `test_risk_engine.py` tests the calculation and decision layer.
- `test_validators.py` tests input validation.

## Disclaimer

This is an educational risk estimation tool, not financial advice. Exchange-specific liquidation prices may differ due to fees, maintenance margin, funding, margin mode, and exchange rules.
