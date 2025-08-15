"use client";

import { useEffect } from "react";
import { signOut } from "next-auth/react";
import { useRouter } from "next/navigation";

export default function LogoutPage() {
  const router = useRouter();

  useEffect(() => {
    // Faz logout e redireciona para a página inicial
    signOut({ redirect: false }).then(() => {
      router.push("/login"); // ou "/" se quiser
    });
  }, [router]);

  return <p>Saindo...</p>;
}
