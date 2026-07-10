export type Direction = "Long" | "Short";
export type SafetyStatus = "Conservative" | "Moderate" | "High Risk";

export type RiskPayload = {
  account_balance: number;
  direction: Direction;
  entry_price: number;
  stop_price: number;
  leverage: number;
  risk_percent: number;
  client_metadata?: Record<string, unknown>;
};

export type RiskResult = {
  risk_per_unit: number;
  max_risk_amount: number;
  position_size_units: number;
  notional_position_value: number;
  margin_required: number;
  money_at_risk: number;
  account_risk_percent: number;
  liquidation_price: number;
  distance_to_stop_percent: number;
  distance_to_liquidation_percent: number;
  liquidation_vs_stop_warning: boolean;
  safety_status: SafetyStatus;
  warnings: string[];
  interpretation: string;
};

export type RiskResponse = {
  calculation_id: string | null;
  result: RiskResult;
};

export type FeedbackPayload = {
  rating?: number;
  message?: string;
  email?: string;
};

export type FeedbackResponse = {
  id: string;
  status: "received";
};

export type WaitlistPayload = {
  email: string;
  trader_type?: string;
  desired_feature?: string;
};

export type WaitlistResponse = {
  id: string;
  status: "joined";
};
