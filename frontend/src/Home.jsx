import React from 'react';
import {Link} from 'react-router-dom';
import './Home.css';


const Home = () => {
  return (
    <main>
      <section className="hero">
        <div className="hero-content">
          <h1>Welcome to FLASHKICK</h1>
          <p>Your ultimate source for football highlights</p>
          {/* <a href="/highlights" className="generate-button">Generate Highlights</a> */}
          <Link to="/highlights" className="generate-button">Generate Highlights</Link>
        </div>
      </section>
    </main>



  );
};

export default Home;
