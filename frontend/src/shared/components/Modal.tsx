import React, {
  forwardRef,
  useImperativeHandle,
  useState,
  ReactNode,
} from 'react';
import { Modal, Box, Typography, Button } from '@mui/material';

export interface ModalHandles {
  openModal: () => void;
  closeModal: () => void;
}

interface ModalProps {
  title?: string;
  children?: ReactNode;
  handleChanged?: (open?: boolean) => void;
}

const style = {
  position: 'absolute' as 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  bgcolor: 'background.paper',
  borderRadius: 2,
  boxShadow: 24,
  p: 4,
};

const CustomModal = forwardRef<ModalHandles, ModalProps>(
  ({ title = 'Modal Title', children, handleChanged }, ref) => {
    const [open, setOpen] = useState(false);

    const openModal = () => {
      setOpen(true);
      if (handleChanged) handleChanged(true);
    };
    const closeModal = () => {
      setOpen(false);
      if (handleChanged) handleChanged(false);
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
        <Box sx={style}>
          <Typography id="modal-title" variant="h6" component="h2" gutterBottom>
            {title}
          </Typography>
          <Box id="modal-description" sx={{ mb: 2 }}>
            {children}
          </Box>
          <Button variant="contained" onClick={closeModal} fullWidth>
            Fechar
          </Button>
        </Box>
      </Modal>
    );
  }
);

export default CustomModal;
