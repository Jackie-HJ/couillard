// src/components/Nav.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function Nav() {
    return (

        <div class="header">
            <div class="width-define">
                <div class="link-row">
                    <div class="logo">
                        Couillard Solar Foundation
                    </div>

                    <div class="header-links">
                        <ul>
                            <li><Link to="/">Home</Link></li>
                            <li><Link to="/catalog">Catalog</Link></li>
                            <li><Link to="/contact">Contact</Link></li>
                        </ul>
                    </div>
                </div>
                
            </div>
        </div>
    );
}