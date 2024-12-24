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
    <div className="relative min-h-screen bg-gradient-to-br from-purple-900 via-indigo-900 to-black text-white p-8 overflow-hidden">
      
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div className="absolute top-0 left-0 w-full h-full bg-gradient-to-b from-purple-700/30 via-transparent to-black/70" />
        <motion.div
          className="absolute -top-20 -left-20 w-[400px] h-[400px] bg-purple-500 blur-3xl opacity-30 rounded-full"
          animate={{ x: [0, 100, -100, 0], y: [0, 50, -50, 0] }}
          transition={{ duration: 10, repeat: Infinity }}
        />
        <motion.div
          className="absolute -bottom-20 -right-20 w-[500px] h-[500px] bg-pink-500 blur-3xl opacity-30 rounded-full"
          animate={{ x: [0, -100, 100, 0], y: [0, -50, 50, 0] }}
          transition={{ duration: 12, repeat: Infinity }}
        />
        <div className="absolute inset-0 bg-[radial-gradient(circle,_rgba(255,255,255,0.1)_0%,_rgba(0,0,0,0)_80%)]" />
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
       
        <motion.h1
          initial={{ opacity: 0, y: -50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="text-7xl font-extrabold text-center mb-10 leading-tight text-transparent bg-clip-text bg-gradient-to-r from-purple-400 to-pink-400"
        >
          SHARD
        </motion.h1>

        
        <form onSubmit={handleSearch} className="mb-10">
          <div className="relative">
            <input
              type="text"
              placeholder="Enter your query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              className="w-full p-5 pr-16 rounded-full bg-white/10 backdrop-blur-md border border-white/30 text-lg placeholder-white/50 text-white focus:outline-none focus:ring-2 focus:ring-purple-400 focus:border-purple-400 transition-all duration-300 shadow-lg hover:shadow-purple-400/30"
            />
            <button
              type="submit"
              className="absolute right-4 top-1/2 transform -translate-y-1/2 p-4 bg-purple-500 rounded-full hover:bg-purple-600 shadow-lg transition-all"
            >
              <Search className="w-6 h-6 text-white" />
            </button>
          </div>
        </form>

       
        {loading && (
          <div className="flex justify-center">
            <Loader2 className="w-10 h-10 text-purple-400 animate-spin" />
          </div>
        )}

        
        {error && (
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className="text-red-400 text-center font-semibold"
          >
            {error}
          </motion.p>
        )}

       
        <AnimatePresence>
          {results.length > 0 && (
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: 20 }}
              transition={{ duration: 0.3 }}
              className="space-y-4"
            >
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className="bg-gradient-to-r from-purple-800/50 to-indigo-900/50 border border-purple-500/30 p-6 rounded-lg shadow-lg hover:shadow-purple-500/50 hover:scale-105 transition-all"
                >
                  <h3 className="text-2xl font-semibold mb-2 text-purple-200">{result.title}</h3>
                  <p className="text-lg text-purple-100/80 mb-4">{result.snippet}</p>
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-purple-400">
                      Relevance Score: {result.score.toFixed(2)}
                    </span>
                    <a
                      href="#"
                      className="text-purple-400 hover:text-purple-300 flex items-center"
                    >
                      Visit <ExternalLink className="w-5 h-5 ml-1" />
                    </a>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        
        {!loading && results.length === 0 && query && (
          <p className="text-center text-white/60 text-lg">
            No results found. Please refine your search.
          </p>
        )}
      </div>
    </div>
  );
}