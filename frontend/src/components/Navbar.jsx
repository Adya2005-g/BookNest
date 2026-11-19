
import { Link } from "react-router-dom";
import { BookOpen, Search, Menu } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="navbar">
      <Link to="/" className="logo">
        <BookOpen size={28} />
        <span>BookNest</span>
      </Link>

      <div className="nav-links">
        <Link to="/">Home</Link>
        <Link to="/books">Explore Books</Link>
        <Link to="/about">About</Link>
      </div>

      <div className="nav-actions">
        <button aria-label="Search">
          <Search size={20} />
        </button>
        <Link to="/login" className="login-btn">Login</Link>
        <Link to="/register" className="signup-btn">Join Now</Link>
      </div>

      <button className="mobile-menu" aria-label="Menu">
        <Menu />
      </button>
    </nav>
  );
}
