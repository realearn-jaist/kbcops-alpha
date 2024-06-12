import { Paper } from "@mui/material";
import React, { useCallback, useState } from "react";
import { useDropzone } from "react-dropzone";

interface FileUploadProps {
  onFilesSelected: (files: File[]) => void;
}

const FileUpload: React.FC<FileUploadProps> = ({ onFilesSelected }) => {
  const [file, setFile] = useState<File | null>(null);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const singleFile = acceptedFiles[0]; // Ensure only one file is processed
    setFile(singleFile);
    onFilesSelected([singleFile]); // Call the callback function with the selected file
  }, [onFilesSelected]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { '.owl': [] },
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
        '&:hover': { border: '1px solid #ccc' }
      }}
    >
      <div style={{ padding: '16px', textAlign: 'center' }} {...getRootProps()}>
        <input {...getInputProps()} />
        {isDragActive ? (
          <p style={{ color: 'green' }}>Drop the file here...</p>
        ) : (
          <p>Upload file<br />(.owl)</p>
        )}
        {file && <p>Selected file: {file.name}</p>}
      </div>
    </Paper>
  );
};

export default FileUpload;
