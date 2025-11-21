import React, { useEffect, useState } from 'react';
import { fetchReviews } from './api';
import ReviewList from './components/ReviewList';
import './App.css';

function App() {
    const [reviews, setReviews] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const loadReviews = async () => {
            try {
                const data = await fetchReviews();
                setReviews(data);
            } catch (error) {
                console.error("Failed to load reviews");
            } finally {
                setLoading(false);
            }
        };

        loadReviews();
        // Poll every 5 seconds to keep updated
        const interval = setInterval(loadReviews, 5000);
        return () => clearInterval(interval);
    }, []);

    return (
        <div className="App">
            <header className="App-header">
                <h1>WhatsApp Product Reviews</h1>
            </header>
            <main>
                {loading ? <p>Loading...</p> : <ReviewList reviews={reviews} />}
            </main>
        </div>
    );
}

export default App;
