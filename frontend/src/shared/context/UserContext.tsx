import React from "react";
import { User } from "../schemas";
import SkeletonLayout from "../components/LayoutSkeleton";
import { useRouter } from "next/navigation";

const UserContext = React.createContext<User | null | undefined>(undefined);

export function UserContextProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = React.useState<User | null>(null);
    const router = useRouter();

    const getUser = async() => {
        const response = await fetch("/api/proxy/auth/user");
        if (response.ok) {
            const user = await response.json();
            return setUser(user);
        }
        return router.push("/login");
    }

    React.useEffect(() => {
        getUser();
    }, []);

    if (user === null) {
        return <SkeletonLayout/>;
    }

    return (
        <UserContext.Provider value={user}>
            {children}
        </UserContext.Provider>
    );
}

export function useContextUser() {
    const context = React.useContext(UserContext);
    if (context === undefined) {
        throw new Error("useContextUser must be used within a UserContextProvider");
    }
    if (context === null) {
        throw new Error("User is not loaded yet");
    }
    return context;
}
