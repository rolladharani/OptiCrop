import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for server environments
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.cluster import KMeans
from sklearn.metrics import classification_report

# Ensure directories exist
os.makedirs('static/images', exist_ok=True)

# Set style matching FiveThirtyEight style from requirements
plt.style.use('fivethirtyeight')

# 1. Read Dataset
print("Loading dataset...")
df = pd.read_csv('Crop_recommendation.csv')

# 2. Rename columns
df.rename(columns={'N': 'nitrogen', 'P': 'phosphorous', 'K': 'potassium'}, inplace=True)

# 3. Handle Outliers for Phosphorous (as per page 10 screenshot)
print("Preprocessing and handling outliers...")
Q1 = df['phosphorous'].quantile(0.25)
Q3 = df['phosphorous'].quantile(0.75)
IQR = Q3 - Q1
phosphorous_filter = (df['phosphorous'] >= Q1 - 1.5 * IQR) & (df['phosphorous'] <= Q3 + 1.5 * IQR)
df = df.loc[phosphorous_filter]
print(f"Data shape after outlier removal: {df.shape}")

# Prepare features and target
y = df['label']
x = df.drop(['label'], axis=1)

# Save original ranges for Suitability Analysis
ranges = {}
for col in x.columns:
    ranges[col] = {
        'min': float(x[col].min()),
        'max': float(x[col].max()),
        'mean': float(x[col].mean()),
        'q1': float(x[col].quantile(0.25)),
        'q3': float(x[col].quantile(0.75))
    }

# Also calculate crop-specific ranges (for Scenario 2 suitability assessments)
crop_ranges = {}
for crop in y.unique():
    crop_df = df[df['label'] == crop]
    crop_ranges[crop] = {}
    for col in x.columns:
        crop_ranges[crop][col] = {
            'min': float(crop_df[col].min()),
            'max': float(crop_df[col].max()),
            'mean': float(crop_df[col].mean()),
            'std': float(crop_df[col].std()) if len(crop_df) > 1 else 1.0
        }

# Save metadata ranges for app usage
with open('crop_ranges.pkl', 'wb') as f:
    pickle.dump(crop_ranges, f)

# 4. Run KMeans Clustering & Generate Elbow Graph (Scenario 3)
print("Running KMeans and generating Elbow graph...")
wcss = []
for i in range(1, 11):
    km = KMeans(n_clusters=i, init='k-means++', max_iter=300, n_init=10, random_state=0)
    km.fit(x)
    wcss.append(km.inertia_)

plt.figure(figsize=(10, 5))
plt.plot(range(1, 11), wcss, marker='o', color='#2ecc71')
plt.title('The Elbow Method', fontsize=18)
plt.xlabel('No of clusters')
plt.ylabel('wcss')
plt.tight_layout()
plt.savefig('static/images/elbow_graph.png')
plt.close()

# Train a 4-cluster KMeans for cluster labeling insights
km4 = KMeans(n_clusters=4, init='k-means++', max_iter=300, n_init=10, random_state=0)
clusters = km4.fit_predict(x)
df_clustered = df.copy()
df_clustered['cluster'] = clusters

cluster_insights = {}
for c in range(4):
    cluster_crops = list(df_clustered[df_clustered['cluster'] == c]['label'].unique())
    cluster_insights[c] = cluster_crops

with open('cluster_insights.pkl', 'wb') as f:
    pickle.dump(cluster_insights, f)

# 5. Generate Other Research Visualization Assets
print("Generating correlation heatmap...")
plt.figure(figsize=(8, 6))
# Exclude target variable for correlation
sns.heatmap(x.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5)
plt.title('Correlation Matrix of Soil & Climate Parameters', fontsize=14)
plt.tight_layout()
plt.savefig('static/images/correlation_heatmap.png')
plt.close()

print("Generating feature distributions...")
fig, axes = plt.subplots(3, 3, figsize=(15, 10))
axes = axes.flatten()
cols = list(x.columns)
for idx, col in enumerate(cols):
    sns.histplot(x[col], ax=axes[idx], kde=True, color='#3498db')
    axes[idx].set_title(f'Distribution of {col.capitalize()}', fontsize=12)
    axes[idx].set_xlabel('')
    axes[idx].set_ylabel('')

# Clear unused subplots
for idx in range(len(cols), 9):
    fig.delaxes(axes[idx])

plt.tight_layout()
plt.savefig('static/images/feature_distributions.png')
plt.close()

# 6. Train Logistic Regression Model
print("Training Logistic Regression model...")
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)
model = LogisticRegression(max_iter=200) # Slightly increased to converge better, still matching logic
model.fit(x_train, y_train)

# Evaluate
y_pred = model.predict(x_test)
report = classification_report(y_test, y_pred)
print("Classification Report:")
print(report)

# Save model
print("Saving model to model.pkl...")
with open('model.pkl', 'wb') as f:
    pickle.dump(model, f)

print("Model training complete. All files saved successfully.")
