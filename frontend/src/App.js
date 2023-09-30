import "./App.css";
import React from "react";
import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Nav from "./components/nav";
import Frame from "./components/frame";
import Footer from "./components/footer";
import Plot from "react-plotly.js";
/*import Catalog from './components/catalog';
import Contact from './components/contact';
*/

//import { Helmet } from 'react-helmet';

function App() {
  const data = [
    {
      x: [1, 2, 3, 4, 5],
      y: [1, 2, 4, 8, 16],
      type: "scatter",
      mode: "lines+markers",
      marker: { color: "red" },
    },
  ];
  return (
    <body>
      <Nav />
      <Frame />
      <div id="test"></div>
      <Plot data={data}></Plot>
      <Footer />
    </body>
  );
}

export default App;
