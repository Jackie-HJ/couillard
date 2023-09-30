// src/components/Home.js
import React from 'react';
import { Link } from 'react-router-dom';

export default function Home() {
    return (
        <div class="quote">
            <div class="italics">
                This is an inspiring quote, or a testimonial from a customer. Maybe it's just filling up space, or maybe people will actually read it. Who knows? All I know is that it looks nice.
            </div>
            <div class="attribution">
                - Olivia Pope
            </div>
        </div>
    );
}