export type AnalyticsEvent =
  | "landing_page_viewed"
  | "calculation_submitted"
  | "copy_summary_clicked"
  | "feedback_submitted";

export function trackEvent(event: AnalyticsEvent, metadata?: Record<string, unknown>) {
  if (process.env.NODE_ENV !== "production") {
    console.info("[analytics]", event, metadata ?? {});
  }
}
