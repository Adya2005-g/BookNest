
import { motion } from "framer-motion";
import {
  Search,
  BookOpen,
  ArrowRight,
  Sparkles
} from "lucide-react";
import BookCard from "../components/BookCard";

const books = [
  {
    title: "Atomic Habits",
    author: "James Clear",
    category: "Self Development",
    rating: "4.8",
    image: "https://covers.openlibrary.org/b/isbn/9780735211292-L.jpg"
  },
  {
    title: "The Alchemist",
    author: "Paulo Coelho",
    category: "Fiction",
    rating: "4.7",
    image: "https://covers.openlibrary.org/b/isbn/9780062315007-L.jpg"
  },
  {
    title: "Ikigai",
    author: "Hector Garcia",
    category: "Lifestyle",
    rating: "4.6",
    image: "https://covers.openlibrary.org/b/isbn/9780143130727-L.jpg"
  },
  {
    title: "Rich Dad Poor Dad",
    author: "Robert Kiyosaki",
    category: "Finance",
    rating: "4.8",
    image: "https://covers.openlibrary.org/b/isbn/9781612680194-L.jpg"
  }
];

export default function Home() {
  return (
    <div className="home-page">

      {/* HERO SECTION */}
      <section className="hero">

        <motion.div
          className="hero-content"
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <span className="hero-tag">
            <Sparkles size={16} />
            YOUR NEXT CHAPTER STARTS HERE
          </span>

          <h1>
            Discover a World
            <br />
            Between <span>Pages.</span>
          </h1>

          <p>
            Explore thousands of books, discover new authors
            and find your next favourite story with BookNest.
          </p>

          <div className="hero-search">
            <Search size={21} />
            <input
              type="text"
              placeholder="Search books, authors..."
            />
            <button>Search</button>
          </div>

          <div className="hero-buttons">
            <a href="/books" className="primary-btn">
              Explore Books <ArrowRight size={18} />
            </a>
            <a href="/register" className="secondary-btn">
              Join BookNest
            </a>
          </div>
        </motion.div>

        <motion.div
          className="hero-visual"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 1 }}
        >
          <div className="book-decoration">
            <BookOpen size={120} strokeWidth={1} />
            <span>Read. Explore. Grow.</span>
          </div>
        </motion.div>

      </section>

      {/* FEATURED BOOKS */}
      <section className="featured-section">

        <div className="section-heading">
          <div>
            <span className="section-tag">HANDPICKED FOR YOU</span>
            <h2>Featured Books</h2>
            <p>Stories and ideas worth discovering.</p>
          </div>

          <a href="/books">
            View All <ArrowRight size={17} />
          </a>
        </div>

        <div className="books-grid">
          {books.map((book, index) => (
            <motion.div
              key={book.title}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ delay: index * 0.15 }}
            >
              <BookCard book={book} />
            </motion.div>
          ))}
        </div>

      </section>

      {/* CALL TO ACTION */}
      <section className="join-section">
        <Sparkles size={28} />
        <h2>Your Reading Journey Starts Here</h2>
        <p>Join BookNest and discover your next favourite book.</p>
        <a href="/register" className="primary-btn">
          Get Started <ArrowRight size={18} />
        </a>
      </section>

    </div>
  );
}
