import React, { useState, useEffect } from "react";
import { Search, Loader2, ExternalLink, Moon, Sun } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import axios from "axios";
import ShardLogo from "/src/shard.png";

export default function ShardSearchEngine() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [searchTriggered, setSearchTriggered] = useState(false); // Track if the search has been triggered
  const [theme, setTheme] = useState("bright"); // Default to bright theme
  const [suggestions, setSuggestions] = useState([]); // State for search suggestions
  const [isAddClicked, setIsAddClicked] = useState(false);
  const [articleId, setArticleId] = useState(""); // Store article ID input




  // Fetch search suggestions when query changes
  useEffect(() => {
    const fetchSuggestions = async () => {
      if (query.trim()) {
        try {
          const response = await axios.get("http://127.0.0.1:5000/search_suggestions", {
            params: { query: query }
          });
          setSuggestions(response.data.suggestions);
        } catch (err) {
          console.error("Error fetching search suggestions:", err);
        }
      } else {
        setSuggestions([]);
      }
    };

    const delayDebounceFn = setTimeout(() => {
      fetchSuggestions();
    }, 500); // Add delay for better performance

    return () => clearTimeout(delayDebounceFn); // Cleanup debounce
  }, [query]);

  const handleSearch = async (e) => {
    e.preventDefault();

    if (!query.trim()) {
      setError("Please enter a query.");
      return;
    }
    setSearchTriggered(true); // Set search as triggered
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

  const handleKeyDown1 = (e) => {
    if (e.key === "Enter") {
      handleSearch(e);
    }
  };

  // Function to toggle between bright and dark theme
  const toggleTheme = () => {
    setTheme(theme === "bright" ? "dark" : "bright");
  };

  // Handle suggestion click to autofill the search box
  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
    setSuggestions([]); // Hide suggestions after selection
    setSearchTriggered(false); // Reset search trigger status
  };

  // Handle Add button click
  const handleAddClick = () => {
    setIsAddClicked((prev) => !prev); // Toggle visibility of the text box
    setArticleId(""); // Clear the article ID when toggling
    setError(null); // Reset error when button is clicked
  };

  const handleArticleIdChange = (e) => {
    setArticleId(e.target.value); // Update article ID as the user types
  };

  const handleKeyDown = async (e) => {
    if (e.key === "Enter" && articleId.trim()) {
      try {
        // Send article ID to the backend
        const response = await axios.post("http://127.0.0.1:5000/add_article", { articleId });
        console.log("Response:", response.data);
        setIsAddClicked(false); // Hide the text box after submission
      } catch (err) {
        console.error("Error adding article:", err);
        setError("Failed to add article. Please try again.");
      }
    }
  };


  return (
    
    <div
      className={`relative min-h-screen ${theme === "bright" ? "bg-gradient-to-br from-purple-500 via-pink-300 to-purple-700 text-black" : "bg-gradient-to-br from-purple-900 via-indigo-900 to-black text-white"} p-8 overflow-hidden`}
    >
      <div className="absolute inset-0 -z-10 overflow-hidden">
        <div
          className={`absolute top-0 left-0 w-full h-full ${theme === "bright" ? "bg-gradient-to-b from-purple-300/30 via-transparent to-black/70" : "bg-gradient-to-b from-black/30 via-transparent to-purple-500"}`}
        />
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
        <div
          className={`absolute inset-0 ${theme === "bright" ? "bg-[radial-gradient(circle,_rgba(255,255,255,0.1)_0%,_rgba(0,0,0,0)_80%)]" : "bg-[radial-gradient(circle,_rgba(0,0,0,0.1)_0%,_rgba(255,255,255,0)_80%)]"}`}
        />
      </div>

      <div className="max-w-4xl mx-auto relative z-10">
        <motion.div 
          initial={{ opacity: 0, y: -50 }} 
          animate={{ opacity: 1, y: 0 }} 
          transition={{ duration: 0.5 }} 
          className="flex justify-center mb-10"
        >
          <img 
            src={ShardLogo} 
            alt="Shard Logo" 
            className="w-64 h-64 object-contain" 
          />
        </motion.div>

        <button
          onClick={toggleTheme}
          className={`absolute top-6 right-6 p-2 rounded-full ${theme === "bright" ? "bg-purple-600 text-white" : "bg-purple-800 text-black"}`}
        >
          {theme === "bright" ? <Sun className="w-6 h-6" /> : <Moon className="w-6 h-6" />}
        </button>

        <form onSubmit={handleSearch} className="mb-10">
          <div className="relative">
            <input
              type="text"
              placeholder="Enter your query"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown1}
              className={`w-full p-5 pr-16 rounded-full ${theme === "bright" ? "bg-white/30 backdrop-blur-md border border-white/30 text-purple-500 focus:ring-2 focus:ring-purple-400" : "bg-black/80 backdrop-blur-md border border-black/30 text-purple-500 focus:ring-2 focus:ring-purple-900"} text-lg placeholder-white/50 focus:outline-none transition-all duration-300 shadow-lg hover:shadow-purple-400/30`}
            />
            <button
              type="submit"
              className={`absolute right-4 top-1/2 transform -translate-y-1/2 p-4 ${theme === "bright" ? "bg-purple-500" : "bg-purple-800"} rounded-full hover:${theme === "bright" ? "bg-purple-600" : "bg-purple-900"} shadow-lg transition-all`}
            >
              <Search className="w-6 h-6 text-white" />
            </button>
          </div>
          {query.trim() && suggestions.length > 0 && (
            <div
              className={`absolute w-full mt-2 z-20 rounded-md backdrop-blur-md border border-white/30 ${theme === "dark" ? "bg-black/60 border-purple-500/50" : "bg-white/30 border-white/30"}`}
            >
              <ul>
                {suggestions.map((suggestion, index) => (
                  <li
                    key={index}
                    onClick={() => handleSuggestionClick(suggestion)}
                    className={`px-4 py-2 text-lg cursor-pointer ${theme === "dark" ? "text-purple-500 hover:bg-purple-500/50 hover:text-white" : "text-purple-500 hover:bg-purple-500/50 hover:text-white"}`}
                  >
                    {suggestion}
                  </li>
                ))}
              </ul>
            </div>
          )}
        </form>

        {loading && (
          <div className="flex justify-center">
            <Loader2 className={`w-10 h-10 ${theme === "bright" ? "text-purple-400" : "text-purple-600"} animate-spin`} />
          </div>
        )}

        {error && (
          <motion.p
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`text-center font-semibold ${theme === "bright" ? "text-red-400" : "text-red-600"}`}
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
              className={`space-y-4 w-900 backdrop-blur-md ${theme === "bright" ? "bg-white/10 border border-white/20" : "bg-black/10 border border-black/20"} rounded-lg p-6`}
            >
              {results.map((result, index) => (
                <motion.div
                  key={index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.3, delay: index * 0.1 }}
                  className={`p-6 rounded-lg shadow-lg hover:scale-105 transition-all ${theme === "bright" ? "bg-white/30 hover:bg-pink-200/50 hover:shadow-md hover:shadow-pink-400  backdrop-blur-lg border border-white/30" : "bg-black/20 hover:bg-purple-600/30 hover:shadow-md hover:shadow-purple-500 backdrop-blur-lg border border-black/30"}`}
                >
                  <h3 className={`text-2xl font-semibold mb-2 ${theme === "bright" ? "text-purple-500" : "text-purple-600"}`}>{result.title}</h3>
                  <p className={`text-lg ${theme === "bright" ? "text-purple-600" : "text-purple-300"} mb-4`}>
                    {result.snippet}
                  </p>

                  <div className="flex justify-between items-center">
                    <span className={`text-sm ${theme === "bright" ? "text-purple-500" : "text-purple-300"}`}>
                      Relevance Score: {result.score.toFixed(2)}
                    </span>
                    <a
                      href={result.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className={`flex items-center ${theme === "bright" ? "text-purple-500 hover:text-purple-300" : "text-purple-600 hover:text-black/80"}`}
                    >
                      Visit <ExternalLink className="w-5 h-5 ml-1" />
                    </a>
                  </div>
                </motion.div>
              ))}
            </motion.div>
          )}
        </AnimatePresence>

        {!loading && results.length === 0 && query && searchTriggered && (
          <p className="text-center text-white/60 text-lg">
            No results found. Please refine your search.
          </p>
        )}
      </div>

     {/* Add and Maintenance Buttons */}
<div className="absolute top-6 right-6 space-x-4 flex">
     {/* Add Button */}
     <button
        onClick={handleAddClick}
        className={`px-6 py-3 rounded-full ${theme === "bright" ? "bg-purple-500 text-white" : "bg-purple-800 text-black"} shadow-lg transition-all duration-300 hover:bg-purple-600`}
      >
        Add
      </button>

      {/* Display Text Box when Add button is clicked */}
      {isAddClicked && (
        <div className="mt-4">
          <input
            type="text"
            placeholder="Add Article ID"
            value={articleId}
            onChange={handleArticleIdChange}
            onKeyDown={handleKeyDown} // Trigger request when Enter is pressed
            className={`w-full px-5 py-3 rounded-full ${theme === "bright" ? "bg-white/30 text-purple-500" : "bg-black/80 text-purple-500"} border border-white/30 backdrop-blur-md focus:outline-none`}
          />
        </div>
      )}

    

</div>
 
   
    
    </div>
    
  );
}
