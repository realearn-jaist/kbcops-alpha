import { Paper } from "@mui/material";
import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFilesSelected }) => {
  // State to store the selected file
  const [file, setFile] = useState<File | null>(null);

  // Function to handle file drop
  const onDrop = useCallback((acceptedFiles: File[]) => {
    const singleFile = acceptedFiles[0]; // Ensure only one file is processed
    setFile(singleFile); // Update state with the selected file
    onFilesSelected([singleFile]); // Call the callback function with the selected file
  }, [onFilesSelected]);

  // Dropzone configuration
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { '.owl': [] }, // Accept only .owl files
    maxFiles: 1 // Limit the number of files to 1
  });

  return (
    <Paper
      sx={{
        cursor: 'pointer',
        background: '#fafafa',
        color: '#bdbdbd',
        border: '1px dashed #ccc',
        borderRadius: '15px',
        margin: '10px',
        height: '120px',
        '&:hover': { border: '1px solid #ccc' } // Change border style on hover
      }}
    >
      {/* Dropzone area */}
      <div style={{ padding: '16px', textAlign: 'center' }} {...getRootProps()}>
        <input {...getInputProps()} /> {/* Hidden input for file selection */}
        {isDragActive ? (
          <p style={{ color: 'green' }}>Drop the file here...</p> // Show when dragging a file over
        ) : (
          <p>Upload file<br />(.owl)</p> // Default message
        )}
        {file && <p>Selected file: {file.name}</p>} {/* Display selected file name */}
      </div>
    </Paper>
  );
};

export default FileUpload;
