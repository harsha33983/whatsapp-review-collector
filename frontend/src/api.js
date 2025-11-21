import axios from 'axios';

const api = axios.create({
    baseURL: '/', // Proxy handles the redirection to backend
});

export const fetchReviews = async () => {
    try {
        const response = await api.get('/api/reviews');
        return response.data;
    } catch (error) {
        console.error("Error fetching reviews:", error);
        throw error;
    }
};
