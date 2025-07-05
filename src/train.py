#!/usr/bin/env python3
"""
Train disease prediction models
Uses processed datasets from EDA notebook
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

from src.utils import load_processed_data, prepare_features, save_model
from src.models import get_all_models

def train_models():
    """
    Train multiple models and select the best one
    """
    print("🚀 Starting model training...")
    
    # Load processed data
    df, symptoms_list, disease_dist = load_processed_data()
    
    if df is None:
        print("❌ Failed to load data. Please run the EDA notebook first.")
        return
    
    # Prepare features
    X, y = prepare_features(df, symptoms_list)
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"📊 Training data: {X_train.shape[0]} samples")
    print(f"📊 Test data: {X_test.shape[0]} samples")
    
    # Get all models
    models = get_all_models()
    
    # Train and evaluate each model
    results = {}
    
    for name, model in models.items():
        print(f"\n🤖 Training {name}...")
        
        try:
            # Train model
            model.fit(X_train, y_train)
            
            # Make predictions
            y_pred = model.predict(X_test)
            
            # Calculate accuracy
            accuracy = accuracy_score(y_test, y_pred)
            results[name] = accuracy
            
            print(f"✅ {name} accuracy: {accuracy:.3f}")
            
        except Exception as e:
            print(f"❌ Error training {name}: {e}")
            results[name] = 0.0
    
    # Find best model
    if results:
        best_model_name = max(results, key=results.get)
        best_accuracy = results[best_model_name]
        
        print(f"\n🏆 BEST MODEL: {best_model_name}")
        print(f"📈 Best accuracy: {best_accuracy:.3f}")
        
        # Save ONLY the best model
        best_model_instance = models[best_model_name]
        best_model_instance.fit(X_train, y_train)  # Retrain on full training data
        save_model(best_model_instance, best_model_name)
        
        # Final evaluation of best model
        y_pred_best = best_model_instance.predict(X_test)
        
        print(f"\n📋 Final Evaluation of {best_model_name}:")
        print(classification_report(y_test, y_pred_best))
        
        return best_model_name, best_accuracy
    
    return None, 0.0

if __name__ == "__main__":
    train_models() 