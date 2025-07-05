#!/usr/bin/env python3
"""
Disease Prediction Inference
Uses processed datasets and trained models
"""

import pandas as pd
import numpy as np
from src.utils import load_model, predict_disease, load_processed_data

def get_available_symptoms():
    """
    Get list of available symptoms
    """
    try:
        # Use the same function as training to avoid duplication
        _, symptoms_list, _ = load_processed_data()
        return symptoms_list or []
    except:
        return []

def get_available_diseases():
    """
    Get list of available diseases
    """
    try:
        # Use the same function as training to avoid duplication
        _, _, disease_dist = load_processed_data()
        if disease_dist is not None:
            return disease_dist['disease'].tolist()
        return []
    except:
        return []

def predict_from_symptoms(symptoms, model_name='randomforest'):
    """
    Predict disease from list of symptoms
    """
    # Load model and symptoms list
    model = load_model(model_name)
    _, symptoms_list, _ = load_processed_data()
    
    if model is None or symptoms_list is None:
        return None, None, "Model or symptoms list not found"
    
    # Validate symptoms
    valid_symptoms = []
    invalid_symptoms = []
    
    for symptom in symptoms:
        if symptom in symptoms_list:
            valid_symptoms.append(symptom)
        else:
            invalid_symptoms.append(symptom)
    
    if not valid_symptoms:
        return None, None, "No valid symptoms provided"
    
    # Make prediction
    try:
        prediction, probabilities = predict_disease(valid_symptoms, model, symptoms_list)
        
        # Get top 3 predictions with probabilities
        disease_names = get_available_diseases()
        if disease_names:
            # Get indices of top 3 probabilities
            top_indices = np.argsort(probabilities)[-3:][::-1]
            top_predictions = []
            
            for idx in top_indices:
                if idx < len(disease_names):
                    top_predictions.append({
                        'disease': disease_names[idx],
                        'probability': float(probabilities[idx])
                    })
        else:
            top_predictions = [{'disease': prediction, 'probability': float(max(probabilities))}]
        
        return prediction, top_predictions, None
        
    except Exception as e:
        return None, None, f"Prediction error: {str(e)}"

def get_disease_info(disease_name):
    """
    Get disease description and precautions
    """
    try:
        # Load disease description
        desc_df = pd.read_csv('content/symptom_Description.csv')
        desc_info = desc_df[desc_df['Disease'].str.strip() == disease_name.strip()]
        
        # Load precautions
        prec_df = pd.read_csv('content/symptom_precaution.csv')
        prec_info = prec_df[prec_df['Disease'].str.strip() == disease_name.strip()]
        
        description = desc_info['Description'].iloc[0] if not desc_info.empty else "No description available"
        precautions = []
        
        if not prec_info.empty:
            for col in prec_info.columns:
                if col != 'Disease':
                    value = prec_info[col].iloc[0]
                    if pd.notna(value) and str(value).strip():
                        precautions.append(str(value).strip())
        
        return {
            'description': description,
            'precautions': precautions
        }
        
    except Exception as e:
        return {
            'description': "Information not available",
            'precautions': []
        }

def interactive_prediction():
    """
    Interactive disease prediction
    """
    print("🏥 DISEASE PREDICTION SYSTEM")
    print("=" * 40)
    
    # Get available symptoms
    available_symptoms = get_available_symptoms()
    
    if not available_symptoms:
        print("❌ No symptoms list found. Please run the EDA notebook first.")
        return
    
    print(f"\n📋 Available symptoms ({len(available_symptoms)}):")
    for i, symptom in enumerate(available_symptoms[:20]):  # Show first 20
        print(f"   {i+1:2d}. {symptom}")
    
    if len(available_symptoms) > 20:
        print(f"   ... and {len(available_symptoms) - 20} more")
    
    # Get user input
    print(f"\n🔍 Enter symptoms (comma-separated):")
    user_input = input("Symptoms: ").strip()
    
    if not user_input:
        print("❌ No symptoms entered")
        return
    
    # Parse symptoms
    symptoms = [s.strip().lower() for s in user_input.split(',')]
    
    # Make prediction
    prediction, top_predictions, error = predict_from_symptoms(symptoms)
    
    if error:
        print(f"❌ Error: {error}")
        return
    
    # Display results
    print(f"\n🎯 PREDICTION RESULTS")
    print("=" * 30)
    
    if top_predictions:
        print(f"🏆 Top predictions:")
        for i, pred in enumerate(top_predictions):
            print(f"   {i+1}. {pred['disease']} ({pred['probability']:.1%})")
        
        # Get disease info for top prediction
        disease_info = get_disease_info(top_predictions[0]['disease'])
        
        print(f"\n📖 Disease Information:")
        print(f"   Disease: {top_predictions[0]['disease']}")
        print(f"   Description: {disease_info['description']}")
        
        if disease_info['precautions']:
            print(f"   Precautions:")
            for i, precaution in enumerate(disease_info['precautions']):
                print(f"     {i+1}. {precaution}")
    
    print(f"\n✅ Prediction complete!")

if __name__ == "__main__":
    interactive_prediction() 