# MERN + Disease Prediction API Integration Guide

## Overview

This guide shows how to integrate the deployed Disease Prediction API with your MERN (MongoDB, Express.js, React.js, Node.js) application.

## 1. Backend Integration (Express.js)

### Create API Service

Create a new file `services/diseaseApi.js` in your Express backend:

```javascript
const axios = require('axios');

class DiseasePredictionService {
  constructor() {
    this.baseURL = process.env.DISEASE_API_URL || 'https://your-api-url.onrender.com';
  }

  // Health check
  async checkHealth() {
    try {
      const response = await axios.get(`${this.baseURL}/health`);
      return response.data;
    } catch (error) {
      throw new Error(`Disease API health check failed: ${error.message}`);
    }
  }

  // Get available symptoms
  async getSymptoms() {
    try {
      const response = await axios.get(`${this.baseURL}/symptoms`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch symptoms: ${error.message}`);
    }
  }

  // Get available diseases
  async getDiseases() {
    try {
      const response = await axios.get(`${this.baseURL}/diseases`);
      return response.data;
    } catch (error) {
      throw new Error(`Failed to fetch diseases: ${error.message}`);
    }
  }

  // Predict disease from symptoms
  async predictDisease(symptoms, modelName = 'randomforest') {
    try {
      const response = await axios.post(`${this.baseURL}/predict`, {
        symptoms,
        model_name: modelName
      });
      return response.data;
    } catch (error) {
      throw new Error(`Prediction failed: ${error.message}`);
    }
  }
}

module.exports = new DiseasePredictionService();
```

### Create API Routes

Create `routes/disease.js`:

```javascript
const express = require('express');
const router = express.Router();
const diseaseService = require('../services/diseaseApi');
const auth = require('../middleware/auth'); // Your auth middleware

// Health check
router.get('/health', async (req, res) => {
  try {
    const health = await diseaseService.checkHealth();
    res.json(health);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get symptoms
router.get('/symptoms', async (req, res) => {
  try {
    const symptoms = await diseaseService.getSymptoms();
    res.json(symptoms);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get diseases
router.get('/diseases', async (req, res) => {
  try {
    const diseases = await diseaseService.getDiseases();
    res.json(diseases);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Predict disease (protected route)
router.post('/predict', auth, async (req, res) => {
  try {
    const { symptoms, modelName } = req.body;
    
    if (!symptoms || !Array.isArray(symptoms) || symptoms.length === 0) {
      return res.status(400).json({ error: 'Symptoms array is required' });
    }

    const prediction = await diseaseService.predictDisease(symptoms, modelName);
    
    // Save prediction to database (optional)
    const predictionRecord = {
      userId: req.user.id,
      symptoms,
      prediction: prediction.prediction,
      confidence: prediction.confidence,
      timestamp: new Date()
    };
    
    // await Prediction.create(predictionRecord); // Your MongoDB model
    
    res.json(prediction);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

// Get user's prediction history
router.get('/history', auth, async (req, res) => {
  try {
    // const history = await Prediction.find({ userId: req.user.id }).sort({ timestamp: -1 });
    // res.json(history);
    res.json({ message: 'History endpoint - implement with your MongoDB model' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;
```

### Update Main App

In your `app.js` or `server.js`:

```javascript
const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();

// Middleware
app.use(cors());
app.use(express.json());

// Routes
app.use('/api/disease', require('./routes/disease'));
// ... other routes

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
```

### Environment Variables

Add to your `.env` file:

```env
DISEASE_API_URL=https://your-api-url.onrender.com
```

## 2. Frontend Integration (React.js)

### Create API Service

Create `services/diseaseApi.js` in your React app:

```javascript
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api';

class DiseaseApiService {
  constructor() {
    this.baseURL = API_BASE_URL;
  }

  // Get auth token
  getAuthToken() {
    return localStorage.getItem('token');
  }

  // Make authenticated request
  async makeRequest(endpoint, options = {}) {
    const token = this.getAuthToken();
    const config = {
      headers: {
        'Content-Type': 'application/json',
        ...(token && { Authorization: `Bearer ${token}` }),
        ...options.headers,
      },
      ...options,
    };

    const response = await fetch(`${this.baseURL}${endpoint}`, config);
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Request failed');
    }
    
    return response.json();
  }

  // Get symptoms
  async getSymptoms() {
    return this.makeRequest('/disease/symptoms');
  }

  // Get diseases
  async getDiseases() {
    return this.makeRequest('/disease/diseases');
  }

  // Predict disease
  async predictDisease(symptoms, modelName = 'randomforest') {
    return this.makeRequest('/disease/predict', {
      method: 'POST',
      body: JSON.stringify({ symptoms, modelName }),
    });
  }

  // Get prediction history
  async getHistory() {
    return this.makeRequest('/disease/history');
  }
}

export default new DiseaseApiService();
```

### Create React Components

#### Disease Prediction Form

```jsx
// components/DiseasePrediction.jsx
import React, { useState, useEffect } from 'react';
import diseaseApi from '../services/diseaseApi';

const DiseasePrediction = () => {
  const [symptoms, setSymptoms] = useState([]);
  const [selectedSymptoms, setSelectedSymptoms] = useState([]);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadSymptoms();
  }, []);

  const loadSymptoms = async () => {
    try {
      const symptomsList = await diseaseApi.getSymptoms();
      setSymptoms(symptomsList);
    } catch (error) {
      setError('Failed to load symptoms');
    }
  };

  const handleSymptomToggle = (symptom) => {
    setSelectedSymptoms(prev => 
      prev.includes(symptom)
        ? prev.filter(s => s !== symptom)
        : [...prev, symptom]
    );
  };

  const handlePredict = async () => {
    if (selectedSymptoms.length === 0) {
      setError('Please select at least one symptom');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const result = await diseaseApi.predictDisease(selectedSymptoms);
      setPrediction(result);
    } catch (error) {
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="disease-prediction">
      <h2>Disease Prediction</h2>
      
      {error && <div className="error">{error}</div>}
      
      <div className="symptoms-section">
        <h3>Select Symptoms</h3>
        <div className="symptoms-grid">
          {symptoms.map(symptom => (
            <label key={symptom} className="symptom-checkbox">
              <input
                type="checkbox"
                checked={selectedSymptoms.includes(symptom)}
                onChange={() => handleSymptomToggle(symptom)}
              />
              {symptom}
            </label>
          ))}
        </div>
      </div>

      <button 
        onClick={handlePredict}
        disabled={loading || selectedSymptoms.length === 0}
        className="predict-btn"
      >
        {loading ? 'Predicting...' : 'Predict Disease'}
      </button>

      {prediction && (
        <div className="prediction-result">
          <h3>Prediction Result</h3>
          <div className="result-card">
            <h4>Predicted Disease: {prediction.prediction}</h4>
            <p>Confidence: {(prediction.confidence * 100).toFixed(2)}%</p>
            
            {prediction.disease_info && (
              <div className="disease-info">
                <h5>Description:</h5>
                <p>{prediction.disease_info.description}</p>
                
                <h5>Precautions:</h5>
                <ul>
                  {prediction.disease_info.precautions.map((precaution, index) => (
                    <li key={index}>{precaution}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default DiseasePrediction;
```

#### Prediction History Component

```jsx
// components/PredictionHistory.jsx
import React, { useState, useEffect } from 'react';
import diseaseApi from '../services/diseaseApi';

const PredictionHistory = () => {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadHistory();
  }, []);

  const loadHistory = async () => {
    try {
      const historyData = await diseaseApi.getHistory();
      setHistory(historyData);
    } catch (error) {
      console.error('Failed to load history:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div>Loading history...</div>;

  return (
    <div className="prediction-history">
      <h2>Prediction History</h2>
      
      {history.length === 0 ? (
        <p>No prediction history found.</p>
      ) : (
        <div className="history-list">
          {history.map((record, index) => (
            <div key={index} className="history-item">
              <div className="history-header">
                <span className="disease">{record.prediction}</span>
                <span className="confidence">
                  {(record.confidence * 100).toFixed(1)}%
                </span>
                <span className="date">
                  {new Date(record.timestamp).toLocaleDateString()}
                </span>
              </div>
              <div className="symptoms">
                <strong>Symptoms:</strong> {record.symptoms.join(', ')}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default PredictionHistory;
```

### Add Routes

In your React app's routing:

```jsx
// App.js or your main routing component
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import DiseasePrediction from './components/DiseasePrediction';
import PredictionHistory from './components/PredictionHistory';

function App() {
  return (
    <Router>
      <div className="App">
        <nav>
          <Link to="/predict">Disease Prediction</Link>
          <Link to="/history">Prediction History</Link>
        </nav>
        
        <Routes>
          <Route path="/predict" element={<DiseasePrediction />} />
          <Route path="/history" element={<PredictionHistory />} />
          {/* ... other routes */}
        </Routes>
      </div>
    </Router>
  );
}
```

## 3. Environment Setup

### Frontend (.env)
```env
REACT_APP_API_URL=http://localhost:5000/api
```

### Backend (.env)
```env
DISEASE_API_URL=https://your-api-url.onrender.com
MONGODB_URI=your_mongodb_connection_string
JWT_SECRET=your_jwt_secret
```

## 4. Deployment Considerations

### CORS Configuration
Update your disease prediction API's CORS settings with your MERN app's domain:

```python
# In app/app.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-mern-app.vercel.app",  # Your frontend domain
        "http://localhost:3000",  # Local development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### Error Handling
Implement proper error handling and retry logic for API calls:

```javascript
// Enhanced API service with retry logic
async makeRequest(endpoint, options = {}, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      return await this._makeRequest(endpoint, options);
    } catch (error) {
      if (i === retries - 1) throw error;
      await new Promise(resolve => setTimeout(resolve, 1000 * (i + 1)));
    }
  }
}
```

This integration provides a complete microservice architecture where your disease prediction API runs independently and communicates with your MERN application through REST APIs. 