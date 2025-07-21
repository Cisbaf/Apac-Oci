import React from "react";
import type { Metadata } from "next";
import "./layout.css"
import LayoutComponent from "@/shared/components/layout";

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
            <LayoutComponent>
              {children}
            </LayoutComponent>
          </body>
        </html>
    
  );
}
