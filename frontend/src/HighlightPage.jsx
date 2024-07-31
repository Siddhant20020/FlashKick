import React from 'react';
import VideoUploader from './components/VideoUploader';
import VideoLinkUploader from './components/VideoLinkUploader';
import './HighlightPage.css';

const HighlightPage = () => (
  <main className="con">
    <h1>Upload Video</h1>
    <VideoUploader />
    <VideoLinkUploader />
  </main>
);

export default HighlightPage;
