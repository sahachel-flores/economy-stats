import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';


const Header = () => {
    return (
        
        <header className="w-full flex justify-between items-center px-6 py-3 shadow-md bg-white sticky top-0 z-50">
            {/* Logo Section */}
            <motion.div
                initial={{ opacity: 0, x: -30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
                className="flex items-center space-x-3"
            >
                <img
                    src="/logo.png" // replace with your logo path
                    alt="Economy Stats AI Logo"
                    className="h-10 w-10 object-contain"
                />
                <h1 className="text-xl font-bold text-gray-800">Economy Stats AI</h1>
            </motion.div>


            {/* Navigation Links */}
            <motion.nav
                initial={{ opacity: 0, x: 30 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
                className="flex space-x-8 text-gray-700 font-medium"
            >
                <a to="/" className="hover:text-blue-600 transition-colors duration-300">
                    Home
                </a>
                <a to="/news" className="hover:text-blue-600 transition-colors duration-300">
                    News
                </a>
                <a to="/predictions" className="hover:text-blue-600 transition-colors duration-300">
                    AI Predictions
                </a>
                <a to="/about" className="hover:text-blue-600 transition-colors duration-300">
                    About Us
                </a>
            </motion.nav>
        </header>
    );
}

export default Header;