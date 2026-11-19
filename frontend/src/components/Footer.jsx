
import { BookOpen } from "lucide-react";

export default function Footer() {
  return (
    <footer className="footer">
      <div className="footer-brand">
        <BookOpen size={26} />
        <h2>BookNest</h2>
      </div>

      <p>Your next favourite book is waiting for you.</p>

      <div className="footer-links">
        <a href="/">Home</a>
        <a href="/books">Explore Books</a>
        <a href="/about">About Us</a>
      </div>

      <p className="copyright">
        © 2026 BookNest. All rights reserved.
      </p>
    </footer>
  );
}
