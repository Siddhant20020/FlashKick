import React, { useState } from 'react';
import axios from 'axios';
import './VideoLinkUploader.css';

const VideoLinkUploader = () => {
  const [videoLink, setVideoLink] = useState('');
  const [submissionStatus, setSubmissionStatus] = useState('');

  const handleLinkChange = (event) => {
    setVideoLink(event.target.value);
  };

  const handleLinkSubmit = async () => {
    if (!videoLink) {
      alert('Please enter a video link.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/upload-link', { videoLink });
      setSubmissionStatus('Link submitted and highlights are being generated.');
      alert('Link submitted successfully. Highlights are being processed.');
    } catch (error) {
      console.error('Error submitting the link:', error);
      setSubmissionStatus('Failed to submit the link.');
      alert('Failed to submit the link.');
    }
  };

  return (
    <section className="hero">
      <div className="link-container">
        <h2>Upload Video Link</h2>
        <label htmlFor="videoLinkInput">Enter video URL</label>
        <input
          type="url"
          id="videoLinkInput"
          name="videoLink"
          placeholder="Enter video URL"
          value={videoLink}
          onChange={handleLinkChange}
        />
        <button type="button" onClick={handleLinkSubmit}>
          Generate Highlights
        </button>
        {submissionStatus && <div className="status">{submissionStatus}</div>}
      </div>
    </section>
  );
};

export default VideoLinkUploader;
