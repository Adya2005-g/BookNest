
import { useEffect, useState } from "react";
import { Search, BookOpen, Star } from "lucide-react";
import { motion } from "framer-motion";
import api from "../services/api";

export default function Books() {
  const [books, setBooks] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const fetchBooks = async () => {
      try {
        const response = await api.get("/books/");

        const data = response.data;
        const bookList = Array.isArray(data)
          ? data
          : data.books || [];

        setBooks(bookList);
      } catch (err) {
        setError("Unable to load books. Please check your backend.");
      } finally {
        setLoading(false);
      }
    };

    fetchBooks();
  }, []);

  const filteredBooks = books.filter((book) =>
    `${book.title} ${book.author || ""}`
      .toLowerCase()
      .includes(search.toLowerCase())
  );

  return (
    <div className="books-page">
      <section className="books-header">
        <span>THE BOOKNEST COLLECTION</span>
        <h1>Explore Our Books</h1>
        <p>Find your next favourite story, idea or inspiration.</p>

        <div className="hero-search">
          <Search size={20} />
          <input
            type="text"
            placeholder="Search by book title or author..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
        </div>
      </section>

      <section className="all-books-section">
        <h2>Discover Books</h2>

        {loading && <p>Loading books...</p>}

        {error && <p className="books-error">{error}</p>}

        {!loading && !error && filteredBooks.length === 0 && (
          <p>No books found.</p>
        )}

        <div className="books-grid">
          {filteredBooks.map((book, index) => (
            <motion.div
              key={book.id || index}
              className="book-card"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.08 }}
            >
              <div className="book-cover">
                <BookOpen size={55} />
              </div>

              <div className="book-info">
                <span className="book-category">
                  {book.category_name || "General"}
                </span>

                <h3>{book.title}</h3>
                <p>{book.author || "Author unavailable"}</p>

                <div className="book-rating">
                  <Star size={16} />
                  {book.rating || "New"}
                </div>

                <p>
                  Available copies: {book.available_copies ?? "N/A"}
                </p>
              </div>
            </motion.div>
          ))}
        </div>
      </section>
    </div>
  );
}
