import React from 'react';
import './AboutPage.css';

const AboutPage = () => (
  <main className="about">
    <section className="hero">
      <div className="hero-content">
        <h1>About Us</h1>
        <p>
          Welcome to Football Highlights Generator. We are passionate about
          creating cutting-edge technology to bring the best football
          highlights to you. Our mission is to provide an unparalleled viewing
          experience with the latest innovations in video analysis and
          highlight generation.
        </p>
        <p>
          Our team consists of football enthusiasts and tech experts dedicated
          to delivering top-quality highlights that capture the essence of
          every game. We strive to keep fans connected and excited by
          providing quick, easy access to the most thrilling moments in
          football.
        </p>
        <p>
          For inquiries or support, please contact us at
          <a href="mailto:contact@footballhighlights.com">contact@footballhighlights.com</a>.
        </p>
      </div>
    </section>
  </main>
);

export default AboutPage;
