# Disease Prediction API

A machine learning-based disease prediction system using FastAPI and scikit-learn.

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Train Model
```bash
python src/train.py
```

### 3. Start API
```bash
python app/app.py
```

Visit: http://127.0.0.1:8000/docs

## 📁 Project Structure

```
├── app/app.py              # FastAPI application
├── src/                    # Source code
│   ├── train.py           # Model training
│   ├── inference.py       # Prediction functions
│   └── utils.py           # Utilities
├── data/                   # Datasets
├── model/                  # Trained models
└── requirements.txt        # Dependencies
```

## 🔧 API Endpoints

- `GET /health` - System health check
- `GET /symptoms` - Get available symptoms
- `GET /diseases` - Get available diseases
- `POST /predict` - Predict disease from symptoms

## 📝 Usage Example

```bash
# Predict disease
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"symptoms": ["fever", "cough", "fatigue"]}'
```

## 🚀 Deployment

### Render (Recommended)
1. Push to GitHub
2. Connect repository to Render
3. Deploy using `render.yaml`

### Environment Variables
- `PORT` - Server port (auto-set by Render)

## 📊 Features

- Multiple ML models (RandomForest, SVC, etc.)
- Cross-validation for model selection
- Disease descriptions and precautions
- RESTful API with automatic documentation
- CORS enabled for frontend integration 