'use client'
import React from "react";
import { useRouter } from "next/navigation";
import { useGlobalComponents } from "@/shared/context/GlobalUIContext";

export default function Home() {
  const route = useRouter();
  const { showBackdrop } = useGlobalComponents();

  React.useEffect(()=>{
    showBackdrop(true);
    route.push("/visualizar");
    setTimeout(()=>{
      showBackdrop(false);
    }, 500);
  }, []);

  return (
    <></>
  );
}
