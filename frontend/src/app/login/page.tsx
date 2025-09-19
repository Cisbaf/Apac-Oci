"use client";

import { useState } from "react";
import { signIn } from "next-auth/react";
import {
  Box,
  Button,
  TextField,
  Typography,
  CircularProgress,
  Alert,
} from "@mui/material";
import { useRouter } from "next/navigation";
import { isValidCPF, formatCPF } from "@/shared/utils/validate";
import "./style.css"
import logoImg from "../../../public/logo_cisbaf.png"
import Image from "next/image";

export default function SignIn() {
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState("");
  const router = useRouter();

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setErrorMsg("");

    const submit = async() => {
      const form = event.currentTarget;
      const formData = new FormData(form);

      var username = formData.get("username")?.toString() ?? "";
      const password = formData.get("password")?.toString() ?? "";

      if (!isValidCPF(username)) {
        return setErrorMsg("Cpf Invalido!")
      }

      username = formatCPF(username);
      const result = await signIn("credentials", {
        redirect: false,
        username,
        password,
      });

      if (result?.error) {
        setErrorMsg("Usuário ou senha inválidos.");
      } else {
        router.push("/");
      }

    }

    await submit();
    setLoading(false);
  }

  return (
    <Box className="container">

      {/* Bloco Esquerdo - Login */}
      <Box className="box-login" component="form" onSubmit={handleSubmit} >
        <Image src={logoImg.src} width={200} height={50} alt=""/>
        <Typography variant="h5" textAlign="center" fontWeight="bold" gutterBottom>
          Sistema Apac
        </Typography>

        {errorMsg && <Alert severity="error">{errorMsg}</Alert>}

        <TextField
          label="Usuário"
          name="username"
          variant="outlined"
          required
          fullWidth
          sx={{ mb: 2 }}
        />

        <TextField
          label="Senha"
          name="password"
          type="password"
          variant="outlined"
          required
          fullWidth
          sx={{ mb: 2 }}
        />

        <Button
          type="submit"
          variant="contained"
          color="primary"
          disabled={loading}
          sx={{ py: 1.5 }}
          fullWidth
        >
          {loading ? <CircularProgress size={24} color="inherit" /> : "Entrar"}
        </Button>
      </Box>

      {/* Bloco Direito - Informações */}
      <Box className="box-info" sx={{ color: "white" }}>
              
      <Box>
        <Typography variant="h4" fontWeight="bold" gutterBottom>
          Bem-vindo ao Sistema Apac OCI
        </Typography>

        <Typography variant="body1" gutterBottom>
          O Sistema Apac OCI foi desenvolvido para <strong>centralizar</strong> e <strong>agilizar</strong> o processo de 
          solicitação, autorização e faturamento das APACs em cada município.
        </Typography>

        <Typography variant="body1" gutterBottom>
          Com ele, você poderá:
        </Typography>

        <ul style={{ marginLeft: "1rem" }}>
          <li>
            <Typography variant="body2">
              Realizar <strong>solicitações de APAC</strong> por unidade de forma simples e segura
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              Permitir que o <strong>profissional autorizador</strong> valide as solicitações, aprovando ou recusando com justificativa
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              Garantir <strong>controle e rastreabilidade</strong> de todas as etapas do processo
            </Typography>
          </li>
          <li>
            <Typography variant="body2">
              Gerar automaticamente o <strong>arquivo de produção mensal</strong> para fins de faturamento municipal
            </Typography>
          </li>
        </ul>

        <Typography variant="body2" sx={{ mt: 2, opacity: 0.8 }}>
          Resultados esperados: mais agilidade, redução de erros no faturamento e melhor gestão das APACs no município.
        </Typography>

        <Typography variant="body2" sx={{ mt: 1, opacity: 0.8 }}>
          Dúvidas ou suporte? Entre em contato com a equipe do CisBaf.
        </Typography>
      </Box>

      </Box>

    </Box>

  );
}
