import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, MapIcon, CurrencyDollarIcon, ChartBarIcon } from '@heroicons/react/24/outline';

function Home() {
  const [searchQuery, setSearchQuery] = useState('');
  const navigate = useNavigate();

  const handleSearch = (e) => {
    e.preventDefault();
    if (searchQuery.trim()) {
      navigate(`/search?q=${searchQuery}`);
    }
  };

  const features = [
    {
      icon: <MagnifyingGlassIcon className="h-8 w-8 text-blue-500" />,
      title: "Smart Discovery",
      description: "AI finds the best places based on your preferences and millions of user votes"
    },
    {
      icon: <MapIcon className="h-8 w-8 text-green-500" />,
      title: "Smart Itinerary",
      description: "Optimized daily plans that minimize travel time and maximize experiences"
    },
    {
      icon: <CurrencyDollarIcon className="h-8 w-8 text-yellow-500" />,
      title: "Budget Tracking",
      description: "Real-time budget estimation and tracking for your entire trip"
    },
    {
      icon: <ChartBarIcon className="h-8 w-8 text-purple-500" />,
      title: "Community Votes",
      description: "See what other travelers recommend and vote for your favorites"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <div className="bg-gradient-to-r from-blue-600 to-indigo-700 text-white">
        <div className="max-w-7xl mx-auto px-4 py-20 text-center">
          <h1 className="text-5xl font-bold mb-4">Plan Your Perfect Trip with AI</h1>
          <p className="text-xl mb-8">PackVote helps you discover, plan, and budget your dream vacation</p>
          
          {/* Search Bar */}
          <form onSubmit={handleSearch} className="max-w-2xl mx-auto">
            <div className="flex gap-2">
              <input
                type="text"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Search for a city, country, or landmark..."
                className="flex-1 px-6 py-3 text-gray-900 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-300"
              />
              <button
                type="submit"
                className="bg-yellow-500 hover:bg-yellow-600 px-8 py-3 rounded-lg font-semibold transition"
              >
                Explore
              </button>
            </div>
          </form>
        </div>
      </div>

      {/* Features Grid */}
      <div className="max-w-7xl mx-auto px-4 py-16">
        <h2 className="text-3xl font-bold text-center mb-12">Why Choose PackVote?</h2>
        <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
          {features.map((feature, idx) => (
            <div key={idx} className="bg-white p-6 rounded-xl shadow-sm hover:shadow-md transition">
              <div className="mb-4">{feature.icon}</div>
              <h3 className="text-xl font-semibold mb-2">{feature.title}</h3>
              <p className="text-gray-600">{feature.description}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA Section */}
      <div className="bg-gray-900 text-white py-16">
        <div className="max-w-4xl mx-auto text-center px-4">
          <h2 className="text-3xl font-bold mb-4">Ready to Start Your Journey?</h2>
          <p className="text-xl mb-8">Join thousands of travelers using PackVote to plan unforgettable trips</p>
          <button className="bg-blue-500 hover:bg-blue-600 px-8 py-3 rounded-lg font-semibold transition">
            Get Started Free
          </button>
        </div>
      </div>
    </div>
  );
}

export default Home;
