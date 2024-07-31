import React, { useState } from 'react';
import axios from 'axios';
import './VideoUploader.css';

const VideoUploader = () => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [fileName, setFileName] = useState('');
    const [uploadProgress, setUploadProgress] = useState(0);
    const [uploadStatus, setUploadStatus] = useState('');

    const handleFileInput = (event) => {
        const file = event.target.files[0];
        setSelectedFile(file);
        setFileName(file ? file.name : '');
        setUploadProgress(0); // Reset progress when a new file is selected
        setUploadStatus(''); // Reset status
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert('Please select a file first.');
            return;
        }

        const formData = new FormData();
        formData.append('file', selectedFile);

        try {
            const response = await axios.post('http://localhost:5000/upload-video', formData, {
                headers: { 'Content-Type': 'multipart/form-data' },
                onUploadProgress: (progressEvent) => {
                    // Calculate the percentage of upload completed
                    const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total);
                    setUploadProgress(percentCompleted);
                }
            });
            setUploadStatus('File uploaded and highlights are being generated.');
            alert('File uploaded successfully. Highlights are being processed.');
        } catch (error) {
            console.error('Error uploading the file:', error);
            setUploadStatus('Failed to upload the file.');
            alert('Failed to upload the file.');
        }
    };

    return (
        <section className='hero'>
            <div className="form-container drop-zone" id="fileDropZone">
                <h2>Upload Video File</h2>
                <label htmlFor="fileInput">Drag and drop file here or click to upload</label>
                <input
                    type="file"
                    id="fileInput"
                    name="file"
                    accept="video/*"
                    onChange={handleFileInput}
                    style={{ display: 'none' }}
                />
                <div id="fileName" className="filename">{fileName}</div>
                <button type="button" id="uploadButton" onClick={handleUpload}>
                    Generate Highlights
                </button>
                {uploadProgress > 0 && (
                    <div className="progress-bar">
                        <div className="progress" style={{ width: `${uploadProgress}%` }}>
                            {uploadProgress}%
                        </div>
                    </div>
                )}
                {uploadStatus && <div className="status">{uploadStatus}</div>}
            </div>
        </section>
    );
};

export default VideoUploader;
