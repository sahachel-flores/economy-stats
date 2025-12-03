import { useState, useEffect } from "react";
import NewsCarousel from "./NewsCarousel";
const topics = ['us economy', 'housing', 'stock', 'labor']

const Homepage = () => {
    
    const [carousels, setCarousel] = useState({})
    const [loading, setLoading] = useState(true)
    
    useEffect( () => {
        const fetchCarousels = async () => {
            const news_articles = {}
            for (const topic of topics) {
                try {
                    const res = await fetch(`/api/homepage/${topic}`)
                    const data = await res.json()
                    news_articles[topic] = data
                } catch (error) {
                    console.error(`Error fetching news for ${topic}:`, error)
                }
            }
            setCarousel(news_articles);
            setLoading(false);
        }

        fetchCarousels()

    }, []);

    if (loading) {
        return <div className="flex justify-center items-center h-screen">
            <div className="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-gray-900">Loading...</div>
        </div>
    }

    return (
        <div className="space-y-12 px-6">
            {topics.map( (topic) => (
                <div key={topic}>
                    <h2 className="text-2xl font-semibold capitalize text-center mb-4">{topic}</h2>
                    {carousels[topic]?.length ? (
                        <NewsCarousel items={carousels[topic]} />
                    ) : (
                        <p> No news found </p>
                    )}
                    
                </div>
            ))}
        </div>
    );
}

export default Homepage;