# Disease Prediction API - Deployment Guide

## Quick Deployment Steps

### 1. Deploy to Render (Recommended)

1. **Push your code to GitHub** (if not already done)
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Render**:
   - Go to [render.com](https://render.com)
   - Sign up/Login with your GitHub account
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect the `render.yaml` configuration
   - Click "Create Web Service"

3. **Wait for deployment** (5-10 minutes)
   - Render will install dependencies
   - Train the model
   - Start the API service

4. **Get your API URL**
   - Once deployed, you'll get a URL like: `https://disease-prediction-api.onrender.com`

### 2. Alternative: Deploy to Railway

1. Go to [railway.app](https://railway.app)
2. Connect your GitHub repository
3. Add environment variable: `PORT=8000`
4. Deploy

### 3. Alternative: Deploy to Heroku

1. Create `Procfile`:
   ```
   web: cd app && gunicorn app:app --bind 0.0.0.0:$PORT --workers 1
   ```

2. Deploy:
   ```bash
   heroku create your-disease-api
   git push heroku main
   ```

## Testing Your Deployed API

Once deployed, test these endpoints:

- **Health Check**: `https://your-api-url.herokuapp.com/health`
- **Get Symptoms**: `https://your-api-url.herokuapp.com/symptoms`
- **Get Diseases**: `https://your-api-url.herokuapp.com/diseases`
- **Predict Disease**: `https://your-api-url.herokuapp.com/predict`
- **API Docs**: `https://your-api-url.herokuapp.com/docs`

## Integration with MERN App

Use the deployed API URL in your MERN application:

```javascript
const API_BASE_URL = 'https://your-api-url.onrender.com';

// Example API calls
const predictDisease = async (symptoms) => {
  const response = await fetch(`${API_BASE_URL}/predict`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ symptoms })
  });
  return response.json();
};
``` 