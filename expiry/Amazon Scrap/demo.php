const express = require('express');
const axios = require('axios');
const cheerio = require('cheerio');

const app = express();

app.use(express.static('public'));

app.get('/scrape', async (req, res) => {
  const url = req.query.url;

  try {
    const response = await axios.get(url, { headers: { 'User-Agent': 'Mozilla/5.0' } });
    const $ = cheerio.load(response.data);

    const productDetails = {
      name: $('#productTitle').text().trim(),
      price: $('#priceblock_ourprice').text().trim() || $('#priceblock_dealprice').text().trim() || 'Price not found',
      mrp: $('.priceBlockStrikePriceString').text().trim() || 'MRP not found',
      imageUrl: $('#landingImage').attr('src') || 'Image not found'
    };

    res.json(productDetails);
  } catch (error) {
    res.status(500).json({ error: 'Failed to fetch data' });
  }
});

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
