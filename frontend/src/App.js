import './App.css';
import React from 'react';
import { BrowserRouter as Router, Route, Routes, Link } from 'react-router-dom';
import Nav from './components/nav';
import Frame from './components/frame';
import Footer from './components/footer';
/*import Catalog from './components/catalog';
import Contact from './components/contact';
*/

//import { Helmet } from 'react-helmet';


function App() {
  return (
    <body>
      <Nav />
      <Frame />
      <Footer />
    </body>

  );
}

export default App;
