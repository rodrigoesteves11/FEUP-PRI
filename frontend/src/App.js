import React, { useState, useEffect } from "react";

const SolrSearchApp = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    console.log("Query state changed:", query);
  }, [query]);

  useEffect(() => {
    console.log("Results state changed:", results);
  }, [results]);

  const fetchData = async () => {
    console.log("fetchData called");
    try {
      const solrQuery = encodeURIComponent(query);
      const url = `http://localhost:3000/solr/species/select?defType=edismax&indent=true&q.op=AND&q=${solrQuery}&qf=introduction%20sections&wt=json`;
      console.log("Fetching URL:", url);

      const response = await fetch(url);
      console.log("Fetch response:", response);

      if (!response.ok) {
        throw new Error(`HTTP error! Status: ${response.status}`);
      }

      const data = await response.json();
      console.log("Response JSON:", data);
      setResults(data.response.docs);
    } catch (error) {
      console.error("Error in fetchData:", error);
    }
  };

  return (
    <div>
      <div className="centered-container-search">
        <h1>BioFinder</h1>
        <div className="header-contents">
          <p>Current Query: {query}</p>
          <p>Results Count: {results.length}</p>
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Enter search query (e.g., introduction:animalia)"
        />
        <button onClick={fetchData}>Search</button>
      </div>

      <div className="centered-container-results">
        <h2>Search Results</h2>
        <ul>
          {results.length > 0 ? (
            results.map((result, index) => (
              <li key={index} className="single-result">
                <div className="result-text-content">
                  <h2>{result.name?.[0] || "No Name"}</h2>
                  <p>{result.introduction?.[0] || "No Introduction"}</p>
                </div>
                <img
                  src={result.image_url?.[0] || "https://via.placeholder.com/150"}
                  alt={result.name?.[0] || "No Image"}
                />
              </li>
            ))
          ) : (
            <p>No results found or still loading...</p>
          )}
        </ul>
      </div>
    </div>

  );
};

export default SolrSearchApp;
