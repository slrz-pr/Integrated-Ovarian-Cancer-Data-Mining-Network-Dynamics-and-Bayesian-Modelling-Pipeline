import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# 1. DATA ACQUISITION & PREPROCESSING
def run_pipeline():
    
    data = {
        'Patient_ID': ['P001', 'P002', 'P003', 'P004', 'P005', 'P006', 'P007', 'P008', 'P009', 'P010'],
        'TP53': [0.12, 0.08, 0.15, 0.95, 1.10, 0.88, 0.10, 0.92, 0.05, 0.85],
        'BRCA1': [4.5, 4.2, 3.8, 0.2, 0.3, 0.1, 4.1, 0.2, 4.6, 0.4],
        'MUC16': [850, 920, 780, 45, 30, 60, 890, 55, 950, 40],
        'VEGFA': [3.2, 3.5, 2.9, 0.5, 0.4, 0.6, 3.1, 0.7, 3.8, 0.5],
        'TOP2A': [4.1, 4.5, 3.9, 0.8, 0.7, 0.9, 4.2, 1.1, 4.8, 0.6],
        'Label': ['High_Risk', 'High_Risk', 'High_Risk', 'Low_Risk', 'Low_Risk', 
                  'Low_Risk', 'High_Risk', 'Low_Risk', 'High_Risk', 'Low_Risk']
    }
    df = pd.DataFrame(data)

    # Labels: High_Risk = 1, Low_Risk = 0
    le = LabelEncoder()
    df['Label_Num'] = le.fit_transform(df['Label'])

    # Features and Target
    features = ['TP53', 'BRCA1', 'MUC16', 'VEGFA', 'TOP2A']
    X = df[features]
    y = df['Label_Num']

    # Scaling data
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    X_scaled_df = pd.DataFrame(X_scaled, columns=features)

    print("--- 1. Data Preprocessing Complete ---")

    # 2. MACHINE LEARNING (Classification)
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.3, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, random_state=42)
    rf.fit(X_train, y_train)
    
    y_pred = rf.predict(X_test)
    print(f"Model Accuracy: {accuracy_score(y_test, y_pred) * 100}%")
    
    # Identify important genes
    importances = rf.feature_importances_
    feat_importances = pd.Series(importances, index=features).sort_values(ascending=False)
    print("\nTop Gene Features:\n", feat_importances)

    # 3. NETWORK ANALYSIS
    print("\n--- 3. Constructing Biological Network ---")
    corr_matrix = X_scaled_df.corr()
    
    G = nx.Graph()
    # Add edges for correlations > 0.7 to identify hubs
    for i in range(len(corr_matrix.columns)):
        for j in range(i):
            if abs(corr_matrix.iloc[i, j]) > 0.7:
                G.add_edge(corr_matrix.columns[i], corr_matrix.columns[j], 
                           weight=corr_matrix.iloc[i, j])

    print(f"Hub Analysis: Node Degrees: {dict(G.degree())}")
    
    # 4. SIMPLE BAYESIAN UNCERTAINTY
    # Estimate P(High_Risk | VEGFA > High_Threshold)
    threshold = X_scaled_df['VEGFA'].mean()
    high_vegfa = df[X_scaled_df['VEGFA'] > threshold]
    
    prob_high_risk = len(high_vegfa[high_vegfa['Label'] == 'High_Risk']) / len(high_vegfa)
    
    print("\n--- 4. Bayesian/Uncertainty Calculation ---")
    print(f"P(High_Risk | High VEGFA): {prob_high_risk:.2f}")
    print("Interpretation: High VEGFA strongly correlates with risk, but results are uncertain due to small sample size.")

    # Visualization
    plt.figure(figsize=(8, 6))
    nx.draw(G, with_labels=True, node_color='skyblue', node_size=2000, edge_color='gray', font_size=12)
    plt.title("Ovarian Cancer Gene Interaction Network")
    plt.show()

if __name__ == "__main__":
    run_pipeline()
