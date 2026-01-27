import React, {
  forwardRef,
  useImperativeHandle,
  useState,
  ReactNode,
} from "react";
import { Modal, Box, Typography, Button, Slider } from "@mui/material";

export interface ModalHandles {
  openModal: () => void;
  closeModal: () => void;
}

interface ModalProps {
  title?: string;
  children?: ReactNode;
  handleChanged?: (open?: boolean) => void;
}

const baseStyle = {
  position: "absolute" as const,
  top: "50%",
  left: "50%",
  transform: "translate(-50%, -50%)",
  bgcolor: "background.paper",
  borderRadius: 2,
  boxShadow: 24,
  p: 4,
  maxHeight: "90vh",
  overflowY: "auto",
};

const CustomModal = forwardRef<ModalHandles, ModalProps>(
  ({ title = "Modal Title", children, handleChanged }, ref) => {
    const [open, setOpen] = useState(false);
    const [width, setWidth] = useState(50); // largura em %
    const [showResize, setShowResize] = useState(false);

    const openModal = () => {
      setOpen(true);
      handleChanged?.(true);
    };

    const closeModal = () => {
      setOpen(false);
      handleChanged?.(false);
    };

    useImperativeHandle(ref, () => ({
      openModal,
      closeModal,
    }));

    return (
      <Modal
        open={open}
        onClose={closeModal}
        aria-labelledby="modal-title"
        aria-describedby="modal-description"
      >
        <Box
          sx={{
            ...baseStyle,
            width: {
              xs: "95%",
              sm: "90%",
              md: `${width}%`,
            },
            transition: "width 0.25s ease",
          }}
        >
          {/* HEADER */}
          <Box
            sx={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              mb: 1,
            }}
          >
            <Typography variant="h6" component="h2">
              {title}
            </Typography>

            <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
              {/* BOTÃO DE AJUSTE */}
              <Typography
                component="button"
                onClick={() => setShowResize((prev) => !prev)}
                sx={{
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  fontSize: 18,
                }}
                title="Ajustar tamanho"
              >
                ↔
              </Typography>

              {/* BOTÃO FECHAR */}
              <Typography
                component="button"
                onClick={closeModal}
                sx={{
                  background: "transparent",
                  border: "none",
                  cursor: "pointer",
                  fontSize: 18,
                }}
                title="Fechar"
              >
                ✕
              </Typography>
            </Box>
          </Box>

          {/* SLIDER DE TAMANHO */}
          {showResize && (
            <Box sx={{ px: 1, pb: 2 }}>
              <Slider
                value={width}
                min={30}
                max={100}
                step={5}
                onChange={(_, newValue) => setWidth(newValue as number)}
                valueLabelDisplay="auto"
              />
            </Box>
          )}

          {/* CONTEÚDO */}
          <Box id="modal-description" sx={{ mb: 2 }}>
            {children}
          </Box>

          {/* RODAPÉ */}
          <Button variant="contained" onClick={closeModal} fullWidth>
            Fechar
          </Button>
        </Box>
      </Modal>
    );
  }
);

export default CustomModal;
