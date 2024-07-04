import React from 'react';
import { IconButton, Tooltip, Dialog, DialogTitle, DialogContent, DialogContentText, DialogActions, Button, Grid, Paper, Box } from '@mui/material';
import InfoIcon from '@mui/icons-material/Info';

interface InfoButtonProps {
  title: string;
  description: {
    main_description: string;
    sub_description: Record<string, string>;
  };
}

export default function InfoButton({ title, description }: InfoButtonProps) {
  const [open, setOpen] = React.useState(false);

  const handleOpen = () => {
    setOpen(true);
  };

  const handleClose = () => {
    setOpen(false);
  };

  return (
    <>
      <Box sx={{ paddingBottom: 1, alignContent: "center" }}>
        <Tooltip title="Info">
          <IconButton onClick={handleOpen}>
            <InfoIcon />
          </IconButton>
        </Tooltip>
      </Box>

      <Dialog open={open} onClose={handleClose} maxWidth="md" fullWidth>
        <DialogTitle>{title}</DialogTitle>
        <DialogContent dividers style={{ minHeight: "80px"}}>
          {description.main_description.split('\n').map((line, index) => (
            <DialogContentText key={index}>{line}</DialogContentText>
          ))}
        </DialogContent>
        <DialogContent dividers>
          {Object.entries(description.sub_description).map(([key, value]) => (
            <Paper key={key} elevation={0} variant="outlined" sx={{ p: 2, marginBottom: 1, maxWidth: '100%' }}>
              <strong>{key}: </strong>{value}
            </Paper>
          ))}
        </DialogContent>

        <DialogActions>
          <Button onClick={handleClose}>Close</Button>
        </DialogActions>
      </Dialog>
    </>
  );
}
