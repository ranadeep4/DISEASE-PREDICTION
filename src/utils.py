#!/usr/bin/env python3
"""
Utility functions for disease prediction
Uses processed datasets from EDA notebook
"""

import pandas as pd
import numpy as np
import pickle
from pathlib import Path

def load_processed_data():
    """
    Load processed datasets from the EDA notebook
    """
    try:
        # Load main processed dataset
        df = pd.read_csv('data/processed/processed_dataset.csv')
        
        # Load symptoms list
        symptoms_df = pd.read_csv('data/processed/symptoms_list.csv')
        symptoms_list = symptoms_df['symptom'].tolist()
        
        # Load disease distribution
        disease_dist = pd.read_csv('data/processed/disease_distribution.csv')
        
        print(f"✅ Loaded processed data:")
        print(f"   • Dataset: {df.shape[0]} patients, {df.shape[1]} features")
        print(f"   • Symptoms: {len(symptoms_list)} unique symptoms")
        print(f"   • Diseases: {len(disease_dist)} unique diseases")
        
        return df, symptoms_list, disease_dist
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Please run the EDA notebook first to create processed datasets")
        return None, None, None

def prepare_features(df, symptoms_list):
    """
    Prepare features for training
    """
    # Separate features and target - ONLY SYMPTOMS
    feature_columns = symptoms_list  # Only use symptom features
    X = df[feature_columns]
    y = df['Disease']
    
    print(f"✅ Prepared features:")
    print(f"   • Input features: {len(feature_columns)}")
    print(f"   • Target classes: {len(y.unique())}")
    
    return X, y

def save_model(model, model_name):
    """
    Save trained model
    """
    model_dir = Path('model')
    model_dir.mkdir(exist_ok=True)
    
    model_path = model_dir / f'{model_name.lower()}_model.pkl'
    
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"💾 Model saved: {model_path}")

def load_model(model_name):
    """
    Load trained model
    """
    model_path = Path('model') / f'{model_name.lower()}_model.pkl'
    
    if not model_path.exists():
        print(f"❌ Model not found: {model_path}")
        return None
    
    with open(model_path, 'rb') as f:
        model = pickle.load(f)
    
    print(f"✅ Model loaded: {model_path}")
    return model

def predict_disease(symptoms, model, symptoms_list):
    """
    Predict disease based on symptoms
    """
    # Create feature vector - ONLY SYMPTOMS
    features = np.zeros(len(symptoms_list))
    
    # Set symptoms to 1
    for symptom in symptoms:
        if symptom in symptoms_list:
            idx = symptoms_list.index(symptom)
            features[idx] = 1
    
    # Make prediction
    prediction = model.predict([features])[0]
    probability = model.predict_proba([features])[0]
    
    return prediction, probability 