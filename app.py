import streamlit as st

from risk_engine import calculate_risk
from validators import validate_inputs


RISK_PRESETS = {
    "Conservative 1%": 1.0,
    "Standard 2%": 2.0,
    "Aggressive 5%": 5.0,
}


st.set_page_config(
    page_title="LiquidationGuard",
    page_icon="LG",
    layout="centered",
    initial_sidebar_state="collapsed",
)


def money(value: float) -> str:
    return f"${value:,.2f}"


def price(value: float) -> str:
    return f"${value:,.2f}"


def percent(value: float) -> str:
    return f"{value:.2f}%"


def units(value: float) -> str:
    return f"{value:,.4f}"


def status_badge(status: str) -> str:
    colors = {
        "Conservative": ("#0f766e", "#ecfdf5"),
        "Moderate": ("#a16207", "#fffbeb"),
        "High Risk": ("#b91c1c", "#fef2f2"),
    }
    text_color, background = colors.get(status, ("#334155", "#f8fafc"))
    return (
        f"<span class='status-badge' style='color:{text_color};"
        f"background:{background};'>{status}</span>"
    )


st.markdown(
    """
    <style>
        .block-container {
            max-width: 860px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        h1, h2, h3 {
            letter-spacing: 0;
        }
        .intro {
            color: #475569;
            font-size: 1.05rem;
            line-height: 1.6;
            margin-bottom: 1.5rem;
        }
        .section-label {
            color: #334155;
            font-weight: 700;
            margin-top: 1.1rem;
            margin-bottom: .35rem;
        }
        .decision-box {
            border: 1px solid #cbd5e1;
            border-left: 5px solid #0f766e;
            border-radius: 8px;
            padding: 1rem;
            background: #f8fafc;
            color: #0f172a;
            font-size: 1.05rem;
            line-height: 1.5;
        }
        .summary-title {
            color: #0f172a;
            font-size: 1rem;
            font-weight: 800;
            margin-bottom: .15rem;
        }
        .summary-subtitle {
            color: #64748b;
            font-size: .9rem;
            margin-bottom: .85rem;
        }
        .summary-card {
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 1.15rem;
            background: #ffffff;
            box-shadow: 0 8px 28px rgba(15, 23, 42, 0.06);
        }
        .summary-row {
            display: flex;
            justify-content: space-between;
            gap: 1rem;
            border-bottom: 1px solid #e2e8f0;
            padding: .55rem 0;
        }
        .summary-row:last-child {
            border-bottom: 0;
        }
        .summary-label {
            color: #64748b;
        }
        .summary-value {
            color: #0f172a;
            font-weight: 700;
            text-align: right;
        }
        .status-badge {
            display: inline-block;
            border-radius: 999px;
            padding: .2rem .6rem;
            font-weight: 700;
        }
        .muted-panel {
            border: 1px solid #e2e8f0;
            border-radius: 8px;
            padding: .95rem;
            color: #475569;
            background: #f8fafc;
        }
        @media (max-width: 640px) {
            .summary-row {
                display: block;
            }
            .summary-value {
                text-align: left;
                margin-top: .15rem;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("LiquidationGuard")
st.markdown(
    "<div class='intro'>A calm pre-trade risk decision tool for futures traders. "
    "Check sizing, margin pressure, and liquidation distance before entering.</div>",
    unsafe_allow_html=True,
)

preset_choice = st.radio(
    "Risk preset",
    options=[*RISK_PRESETS.keys(), "Custom"],
    index=1,
    horizontal=True,
    help="Choose a common account-risk setting, or select Custom to enter your own.",
)

with st.form("risk_form"):
    st.markdown("<div class='section-label'>Account and trade setup</div>", unsafe_allow_html=True)

    account_balance = st.number_input(
        "Account balance",
        min_value=0.0,
        value=1000.0,
        step=100.0,
        format="%.2f",
        help="Your available trading account balance.",
    )

    direction = st.radio(
        "Trade direction",
        options=["Long", "Short"],
        horizontal=True,
        help="Choose Long if you expect price to rise, or Short if you expect price to fall.",
    )

    price_col_1, price_col_2 = st.columns(2)
    with price_col_1:
        entry_price = st.number_input(
            "Entry price",
            min_value=0.0,
            value=100.0,
            step=1.0,
            format="%.4f",
            help="The price where you plan to enter the trade.",
        )
    with price_col_2:
        stop_price = st.number_input(
            "Stop price",
            min_value=0.0,
            value=95.0,
            step=1.0,
            format="%.4f",
            help="The price where your trade idea is invalidated.",
        )

    risk_col_1, risk_col_2 = st.columns(2)
    with risk_col_1:
        leverage = st.number_input(
            "Leverage",
            min_value=1.0,
            value=10.0,
            step=1.0,
            format="%.2f",
            help="The leverage multiplier for the position.",
        )
    with risk_col_2:
        preset_risk_percent = RISK_PRESETS.get(preset_choice, 2.0)
        risk_percent = st.number_input(
            "Risk percentage",
            min_value=0.01,
            max_value=10.0,
            value=preset_risk_percent,
            step=0.25,
            format="%.2f",
            disabled=preset_choice != "Custom",
            help="The percentage of your account you are willing to lose if stopped out.",
        )

    submitted = st.form_submit_button("Calculate risk", use_container_width=True)

if submitted:
    errors = validate_inputs(
        account_balance=account_balance,
        direction=direction,
        entry_price=entry_price,
        stop_price=stop_price,
        leverage=leverage,
        risk_percent=risk_percent,
    )

    if errors:
        st.error("Please fix the setup before calculating.")
        for error in errors:
            st.write(f"- {error}")
    else:
        result = calculate_risk(
            account_balance=account_balance,
            direction=direction,
            entry_price=entry_price,
            stop_price=stop_price,
            leverage=leverage,
            risk_percent=risk_percent,
        )

        st.divider()
        st.subheader("Risk output")

        with st.container(border=True):
            metric_row_1 = st.columns(3)
            metric_row_1[0].metric(
                "Suggested position size",
                units(result["position_size_units"]),
            )
            metric_row_1[1].metric(
                "Notional position value",
                money(result["notional_position_value"]),
            )
            metric_row_1[2].metric("Margin required", money(result["margin_required"]))

            metric_row_2 = st.columns(3)
            metric_row_2[0].metric("Money at risk", money(result["money_at_risk"]))
            metric_row_2[1].metric("Account risk", percent(result["account_risk_percent"]))
            metric_row_2[2].metric("Approx. liquidation", price(result["liquidation_price"]))

            metric_row_3 = st.columns(3)
            metric_row_3[0].metric(
                "Distance to stop",
                percent(result["distance_to_stop_percent"]),
            )
            metric_row_3[1].metric(
                "Distance to liquidation",
                percent(result["distance_to_liquidation_percent"]),
            )
            metric_row_3[2].markdown(
                "<div style='padding-top:.35rem'><div class='summary-label'>Safety status</div>"
                f"<div style='margin-top:.4rem'>{status_badge(result['safety_status'])}</div></div>",
                unsafe_allow_html=True,
            )

        st.markdown("### Decision")
        st.markdown(
            f"<div class='decision-box'>{result['decision']}</div>",
            unsafe_allow_html=True,
        )

        st.markdown("### Warnings")
        for warning in result["warnings"]:
            st.warning(warning)

        st.markdown("### Screenshot summary")
        st.markdown(
            f"""
            <div class="summary-card">
                <div class="summary-title">LiquidationGuard Risk Summary</div>
                <div class="summary-subtitle">Pre-trade sizing check</div>
                <div class="summary-row">
                    <div class="summary-label">Direction</div>
                    <div class="summary-value">{direction}</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Entry</div>
                    <div class="summary-value">{price(entry_price)}</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Stop</div>
                    <div class="summary-value">{price(stop_price)}</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Leverage</div>
                    <div class="summary-value">{leverage:.2f}x</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Account risk</div>
                    <div class="summary-value">{percent(result["account_risk_percent"])}</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Liquidation price</div>
                    <div class="summary-value">{price(result["liquidation_price"])}</div>
                </div>
                <div class="summary-row">
                    <div class="summary-label">Safety status</div>
                    <div class="summary-value">{result["safety_status"]}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
else:
    st.info("Enter your trade details, then calculate risk before entering the trade.")

st.divider()
st.markdown(
    "<div class='muted-panel'><strong>Pro features coming soon:</strong> saved profiles, "
    "trade history, alerts, and portfolio risk.</div>",
    unsafe_allow_html=True,
)

st.caption(
    "This is an educational risk estimation tool, not financial advice. "
    "Exchange-specific liquidation prices may differ due to fees, maintenance margin, "
    "funding, margin mode, and exchange rules."
)
