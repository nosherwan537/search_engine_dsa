import React, { useState } from "react";
import { Search, Loader2, ExternalLink } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";

export default function ShardSearchEngine() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSearch = async (e) => {
    e.preventDefault(); // Prevent form submission from reloading the page

    if (!query.trim()) {
      setError("Please enter a query.");
      return;
    }
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post("http://127.0.0.1:5000/search", { query });
      setResults(response.data.results);
    } catch (err) {
      setError("Failed to fetch search results. Please try again later.");
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="min-h-screen bg-gradient-to-br from-purple-900 to-indigo-900 text-white p-8">
      <div className="max-w-4xl mx-auto">
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-6xl font-bold text-center mb-8"
        >
          SHARD
        </motion.h1>
        <form onSubmit={handleSearch} className="mb-8">
          <div className="relative">
            <input
              type="text"
              placeholder="Enter your query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full p-4 pr-12 rounded-full bg-white/10 backdrop-blur-md border border-white/20 focus:outline-none focus:ring-2 focus:ring-purple-500 hover:shadow-md hover:shadow-purple-500 text-white placeholder-white/50  transitions-all duration-300"
            />
            <button
              type="submit"
              className="absolute right-2 top-1/2 transform -translate-y-1/2 p-2 bg-purple-500 rounded-full hover:bg-purple-600 transition-colors"
            >
              <Search className="w-6 h-6" />
            </button>
          </div>
        </form>

        {loading && (
          <div className="flex justify-center">
            <Loader2 className="w-8 h-8 animate-spin " />
          </div>
        )}
        {error && <p className="text-red-400 text-center scale-110">{error}</p>}

        <AnimatePresence>
          {results.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.3 }}
            >
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="bg-white/10 backdrop-blur-md rounded-lg p-6 mb-4 border border-white/20 hover:border-purple-500 hover:scale-105 hover:shadow-md hover:shadow-purple-500 transition-colors"
                >
                  <h3 className="text-xl font-semibold mb-2">{result.title}</h3>
                  <p className="text-white/80 mb-2">{result.snippet}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-purple-300">
                      Relevance Score: {result.score.toFixed(2)}
                    </span>
                    <a
                      href="#"
                      className="text-purple-300 hover:text-purple-100 transition-colors flex items-center"
                    >
                      Visit <ExternalLink className="w-4 h-4 ml-1" />
                    </a>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {!loading && results.length === 0 && query && (
          <p className="text-center  scale-110 text-white/60">No results found.</p>
        )}
      </div>
    </div>
  );
}


