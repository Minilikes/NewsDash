// routes/news.js
const express = require('express');
const axios = require('axios');
const User = require('../models/user.model');
const router = express.Router();

const API_KEY = process.env.NEWS_API_KEY;
const BASE_URL = 'https://newsapi.org/v2';

// GET: Fetch news based on user preferences
router.get('/', async (req, res) => {
  try {
    // Find preferences for our guest user
    const user = await User.findOneAndUpdate(
        { userId: 'guest-user' }, // query
        {}, // update (none)
        { upsert: true, new: true } // options: create if not found
    );
    const preferences = user.preferences.join(','); // e.g., "technology,business"
    
    // Fetch news from the NewsAPI
    const newsResponse = await axios.get(`${BASE_URL}/everything?q=${preferences}&apiKey=${API_KEY}&pageSize=20`);
    
    res.json(newsResponse.data.articles);
  } catch (error) {
    console.error("Error fetching news:", error.message);
    res.status(500).json({ message: 'Failed to fetch news' });
  }
});

// GET: Fetch user preferences
router.get('/preferences', async (req, res) => {
    try {
        const user = await User.findOne({ userId: 'guest-user' });
        if (!user) {
            // Create a default user if none exists
            const newUser = new User();
            await newUser.save();
            return res.json(newUser.preferences);
        }
        res.json(user.preferences);
    } catch (error) {
        res.status(500).json({ message: 'Failed to get preferences' });
    }
});

// POST: Update user preferences
router.post('/preferences', async (req, res) => {
  const { preferences } = req.body;
  if (!preferences || !Array.isArray(preferences)) {
    return res.status(400).json({ message: 'Invalid preferences format' });
  }

  try {
    const user = await User.findOneAndUpdate(
      { userId: 'guest-user' },
      { preferences: preferences },
      { new: true, upsert: true }
    );
    res.json(user.preferences);
  } catch (error) {
    res.status(500).json({ message: 'Failed to update preferences' });
  }
});

module.exports = router;