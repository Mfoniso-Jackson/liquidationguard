import type { FeedbackPayload, FeedbackResponse, RiskPayload, RiskResponse } from "./types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

async function parseResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const detail = await response.json().catch(() => null);
    const message =
      typeof detail?.detail === "string"
        ? detail.detail
        : "The request could not be completed. Please check the inputs and try again.";
    throw new Error(message);
  }
  return response.json() as Promise<T>;
}

export async function calculateRisk(payload: RiskPayload): Promise<RiskResponse> {
  const response = await fetch(`${API_BASE_URL}/api/risk/calculate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<RiskResponse>(response);
}

export async function submitFeedback(payload: FeedbackPayload): Promise<FeedbackResponse> {
  const response = await fetch(`${API_BASE_URL}/api/feedback`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  return parseResponse<FeedbackResponse>(response);
}
