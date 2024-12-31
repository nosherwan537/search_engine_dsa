import React from "react";
import ReactDOM from "react-dom/client";
import './index.css';
import { BrowserRouter } from "react-router-dom";  
import SearchApp from "./SearchApp"; 

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <BrowserRouter>  
      <SearchApp />
    </BrowserRouter>
  </React.StrictMode>
);
