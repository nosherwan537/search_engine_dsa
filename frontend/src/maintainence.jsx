import React from 'react';
import { FaSearch } from 'react-icons/fa';
import 'tailwindcss/tailwind.css';

const MaintenancePage = () => {
    return (
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-r from-purple-400 via-pink-500 to-red-500">
            <div className="text-center text-white">
                <FaSearch className="text-6xl animate-bounce mb-4" />
                <h1 className="text-4xl font-bold mb-2">Under Maintenance</h1>
                <p className="text-xl">We are currently working on the site. Please check back later.</p>
            </div>
        </div>
    );
};

export default MaintenancePage;