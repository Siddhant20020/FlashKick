import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => (
  <header>
    <div className="container">
      <div className="logo-container">
        <img src="/logo.png" alt="FLASHKICK Logo" className="logo-img" />
        <span className="logo-text">FLASHKICK</span>
      </div>
      <nav>
        <ul>
          <li><Link to="/">Home</Link></li>
          <li><Link to="/highlights">Highlights</Link></li>
          <li><Link to="/about">About</Link></li>
        </ul>
      </nav>
    </div>
  </header>
);

export default Header;
