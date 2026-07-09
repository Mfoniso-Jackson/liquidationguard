import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "LiquidationGuard",
  description: "Know your risk before you enter a futures trade.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
