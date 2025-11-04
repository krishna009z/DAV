import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import { Film, LayoutDashboard, Star, FileText, Search, LogOut } from 'lucide-react';
import './Navbar.css';

function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path;

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/dashboard" className="navbar-brand">
          <Film size={32} />
          <span>Movie Analyzer</span>
        </Link>

        <div className="navbar-links">
          <Link
            to="/dashboard"
            className={`navbar-link ${isActive('/dashboard') ? 'active' : ''}`}
          >
            <LayoutDashboard size={20} />
            Dashboard
          </Link>
          <Link
            to="/famous-movies"
            className={`navbar-link ${isActive('/famous-movies') ? 'active' : ''}`}
          >
            <Star size={20} />
            Famous Movies
          </Link>
          <Link
            to="/custom-analysis"
            className={`navbar-link ${isActive('/custom-analysis') ? 'active' : ''}`}
          >
            <FileText size={20} />
            Custom Analysis
          </Link>
          <Link
            to="/movie-search"
            className={`navbar-link ${isActive('/movie-search') ? 'active' : ''}`}
          >
            <Search size={20} />
            Movie Search
          </Link>
        </div>

        <div className="navbar-user">
          <span className="user-name">{user?.username}</span>
          <button onClick={handleLogout} className="btn-logout">
            <LogOut size={20} />
          </button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
