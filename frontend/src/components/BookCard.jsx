
import { Star } from "lucide-react";

export default function BookCard({ book }) {
  return (
    <div className="book-card">
      <img src={book.image} alt={book.title} />

      <div className="book-info">
        <span className="book-category">
          {book.category}
        </span>

        <h3>{book.title}</h3>
        <p>{book.author}</p>

        <div className="book-rating">
          <Star size={16} fill="currentColor" />
          {book.rating}
        </div>
      </div>
    </div>
  );
}
