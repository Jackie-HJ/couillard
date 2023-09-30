import React from 'react';
import { Routes, Route } from 'react-router-dom';

import Home from '../home/Home';
import Catalog from '../catalog/Catalog';
import Contact from '../contact/Contact';

export default function Frame() {
  return (
    <Routes> 
      <Route path='/' element={<Home />}/>
      <Route path='/catalog' element={<Catalog />} />
      <Route path='/contact' element={<Contact />} />
    </Routes>
  );
}
