const express = require('express');
const app = express();
const port = process.env.PORT || 3001;
const Cloudant = require('@cloudant/cloudant');

// Initialize Cloudant connection with IAM authentication
async function dbCloudantConnect() {
    try {
        const cloudant = Cloudant({
            plugins: { iamauth: { iamApiKey: '_jugmwUV-zcyjoPk2D27MnfBO8ppCxzbkGj6SB1b8yW9' } }, // Replace with your IAM API key
            url: 'https://81085ec4-ddcf-415f-9741-2e328061803b-bluemix.cloudantnosqldb.appdomain.cloud', // Replace with your Cloudant URL
        });

        const db = cloudant.use('reviews');
        console.info('Connect success! Connected to DB');
        return db;
    } catch (err) {
        console.error('Connect failure: ' + err.message + ' for Cloudant DB');
        throw err;
    }
}

let db;

(async () => {
    db = await dbCloudantConnect();
})();

app.use(express.json());

// Define a route to create a new review for a specific dealership by ID
app.post('/dealerships/:dealership/reviews', (req, res) => {
    const dealershipId = req.params.id; // Get the dealership ID from the URL

    // Extract review data from the request body
    const { author, rating, comment } = req.body;

    // Create a new review object
    const newReview = {
        author,
        rating,
        comment,
        dealershipId, // Associate the review with the dealership by ID
        timestamp: new Date().toISOString(), // Add a timestamp if needed
    };

    // Insert the new review into the database
    db.insert(newReview, (err, body) => {
        if (err) {
            console.error('Error creating review:', err);
            res.status(500).json({ error: 'An error occurred while creating the review.' });
        } else {
            const createdReview = {
                id: body.id,
                ...newReview,
            };
            res.status(201).json(createdReview); // Respond with the created review
        }
    });
});

// get the list of reviews for a specific dealership by ID
app.get('/dealerships/:dealership/reviews', (req, res) => {
    const dealershipId = req.params.dealership; // Get the dealership ID from the URL

    // Create a selector object based on the dealership ID
    const selector = {
        dealership: Number(dealershipId), // Assuming dealership is stored as a number in your schema
    };

    const queryOptions = {
        selector,
        limit: 10, // Limit the number of reviews returned to 10 (adjust as needed)
    };

    db.find(queryOptions, (err, body) => {
        if (err) {
            console.error('Error fetching reviews:', err);
            res.status(500).json({ error: 'An error occurred while fetching reviews.' });
        } else {
            const reviews = body.docs;
            res.json(reviews);
        }
    });
});


app.listen(port, () => {
    console.log(`Server is running on port ${port}`);
});