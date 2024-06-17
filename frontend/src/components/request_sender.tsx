import React, { useState } from 'react';
import { Button, MenuItem, Select, TextField, Grid, SelectChangeEvent } from '@mui/material';

interface RequestData {
  method: string;
  endpoint: string;
}

const HttpMethodOptions = ['GET', 'POST', 'PUT', 'DELETE'];

const RequestComponent: React.FC = () => {
  const [requestData, setRequestData] = useState<RequestData>({
    method: 'GET',
    endpoint: '',
  });

  const handleMethodChange = (event: SelectChangeEvent<string>) => {
    setRequestData({ ...requestData, method: event.target.value });
  };

  const handleEndpointChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setRequestData({ ...requestData, endpoint: event.target.value });
  };

  const handleSendRequest = async () => {
    try {
      const response = await fetch(`http://127.0.0.1:5000/${requestData.endpoint}`, {
        method: requestData.method,
        // Add other fetch options here as needed
      });
      
      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log('Response:', data);
      // Handle response data or update state as needed
    } catch (error) {
      console.error('Error sending request:', error);
      // Handle error or show error message
    }
  };

  return (
    <Grid container spacing={2}>
      <Grid item xs={3}>
        <Select
          value={requestData.method}
          onChange={handleMethodChange}
          fullWidth
          variant="outlined"
          size="small"
        >
          {HttpMethodOptions.map((method) => (
            <MenuItem key={method} value={method}>
              {method}
            </MenuItem>
          ))}
        </Select>
      </Grid>
      <Grid item xs={6}>
        <TextField
          value={requestData.endpoint}
          onChange={handleEndpointChange}
          label="Endpoint"
          variant="outlined"
          fullWidth
          size="small"
        />
      </Grid>
      <Grid item xs={3}>
        <Button
          variant="contained"
          color="primary"
          onClick={handleSendRequest}
          fullWidth
          size="large"
        >
          Send Request
        </Button>
      </Grid>
    </Grid>
  );
};

export default RequestComponent;
