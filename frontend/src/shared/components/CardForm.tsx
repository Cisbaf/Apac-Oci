import { Box, Typography, SxProps, Theme } from "@mui/material";

interface Props {
    title: string;
    children: React.ReactNode;
    backgroundColor?: string;
    titleBackgroundColor?: string;
    colorTitle?: string;
    contentBoxStyle?: SxProps<Theme>; // <- nova prop para estilos adicionais
    padding?: number;
}

export default function CardForm(props: Props) {
    return (
        <Box
            sx={{
                border: "outset",
                borderWidth: 1,
                borderColor: "#b8b2b2",
                borderRadius: 0.5,
                position: "relative",
                minWidth: 180,
                padding: props.padding? props.padding : 0,
                backgroundColor: props.backgroundColor || "white",
                ...props.contentBoxStyle, // <- aplica os estilos adicionais aqui
            }}
        >
            <Box
                sx={{
                    position: "absolute",
                    top: "-12px",
                    left: 0,
                    right: 0,
                    margin: "0 auto",
                    display: "flex",
                    justifyContent: "center",
                    backgroundColor: props.titleBackgroundColor || "#343a40",
                    borderRadius: 0.5,
                    maxWidth: "fit-content",
                    paddingLeft: "8px",
                    paddingRight: "8px",
                }}
            >
                <Typography
                    style={{
                        color: props.colorTitle || "white",
                        fontWeight: 800,
                        whiteSpace: "nowrap",
                    }}
                >
                    {props.title}
                </Typography>
            </Box>
            {props.children}
        </Box>
    );
}
