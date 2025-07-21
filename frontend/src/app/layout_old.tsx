import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { GlobalComponentsProvider } from "@/shared/context/GlobalUIContext";

import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Apac OCI",
  description: "Apac Oci",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="pt-br">
      <body className={`${geistSans.variable} ${geistMono.variable}`}>
          <GlobalComponentsProvider>
              {children}
          </GlobalComponentsProvider>
      </body>
    </html>
  );
}