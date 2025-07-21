'use client';
import React from 'react';
import { useRouter } from 'next/navigation';

export default function LogoutPage() {
    const router = useRouter();
       
    React.useEffect(() => {
        fetch('/api/auth/logout', {
        method: 'POST',
        }).then(response=>{
            if (response.ok) {
                router.push('/login');
            }
        }).catch((error)=>{
            console.error('Erro ao fazer logout:', error);
        })
    }, []);

    return (
        <h1>Logging out...</h1>
    );
}