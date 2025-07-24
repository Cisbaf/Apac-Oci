'use client';
import React from "react";
import { useGlobalComponents } from "../context/GlobalUIContext";
import { Paper, Typography, Alert, Box, TextField, Button } from "@mui/material";
import { useRouter } from "next/navigation";
import { useSearchParams } from "next/navigation";
import { useMask } from "@react-input/mask";
import { CpfMask } from "../utils/mask";

export default function Login() {
    const cpfMakRef = useMask(CpfMask);
    const [username, setUsername] = React.useState('');
    const [password, setPassword] = React.useState('');
    const { showBackdrop, showAlert } = useGlobalComponents();
    const router = useRouter();
    const searchParams = useSearchParams();
    const redirectTo = searchParams.get('from') || '/visualizar';

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
      
        showBackdrop(true);
            try {
                const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                credentials: 'include', // <- ESSENCIAL para receber o cookie
                body: JSON.stringify({ username, password }),
            });
            if (response.ok) {
                router.push(redirectTo);
            } else {
                showAlert({color: "error", message: "Credenciais invalidas!"});
            }
        } catch (e) {
            showAlert({color: "error", message: "Não foi possivel realizar a conexão com o servidor!"})
        }
        showBackdrop(false);
    };

    return (
        <div style={{
            display: 'flex',
            justifyContent: 'center',
            alignItems: 'center',
            height: '100vh',
            backgroundColor: '#f5f5f5',
        }}>
            <Paper elevation={3} sx={{ padding: 4, width: '100%', maxWidth: 400 }}>
                <Typography variant="h4" align="center" gutterBottom>
                    Login
                </Typography>

                <Box component="form" onSubmit={handleSubmit} noValidate>
                    <TextField   size="small" 
                        inputRef={cpfMakRef}
                        label="CPF"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={username}
                        onChange={(e) => setUsername(e.target.value)}
                        required
                    />
                    <TextField   size="small" 
                        label="Password"
                        type="password"
                        variant="outlined"
                        fullWidth
                        margin="normal"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                    <Button
                        type="submit"
                        variant="contained"
                        color="primary"
                        fullWidth
                        sx={{ mt: 2 }}>
                        Login
                    </Button>
                </Box>
            </Paper>
        </div>
    );
}