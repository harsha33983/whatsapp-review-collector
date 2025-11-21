import React from 'react';

const ReviewList = ({ reviews }) => {
    return (
        <div className="review-container">
            <h2>Customer Reviews</h2>
            {reviews.length === 0 ? (
                <p>No reviews yet.</p>
            ) : (
                <table className="review-table">
                    <thead>
                        <tr>
                            <th>Product</th>
                            <th>User</th>
                            <th>Review</th>
                            <th>Time</th>
                        </tr>
                    </thead>
                    <tbody>
                        {reviews.map((review) => (
                            <tr key={review.id}>
                                <td>{review.product_name}</td>
                                <td>{review.user_name}</td>
                                <td>{review.product_review}</td>
                                <td>{new Date(review.created_at).toLocaleString()}</td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            )}
        </div>
    );
};

export default ReviewList;
