import React from "react";
import type { Metadata } from "next";
import "./layout.css"
import LayoutSystem from "@/shared/components/Layout";
import { GlobalComponentsProvider } from "@/shared/context/GlobalUIContext";

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
          <body>
            <GlobalComponentsProvider>
              <LayoutSystem>{children}</LayoutSystem>
            </GlobalComponentsProvider>
          </body>
        </html>
    
  );
}
