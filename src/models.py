#!/usr/bin/env python3
"""
Model definitions for disease prediction
"""

from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


def get_all_models():
    """
    Get all models for training
    """
    models = {
        'RandomForest': RandomForestClassifier(n_estimators=100, random_state=42),
        'LogisticRegression': LogisticRegression(max_iter=1000, random_state=42),
        'SVC': SVC(kernel='rbf', random_state=42, probability=True),
        'DecisionTree': DecisionTreeClassifier(random_state=42)
    }
    return models 