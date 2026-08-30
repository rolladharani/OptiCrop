# OptiCrop: Smart Agricultural Production Optimization Engine

**Live Demo:** https://opticrop-agricultureguide.onrender.com/  
**GitHub Repository:** [https://github.com/rolladharani/OptiCrop](https://github.com/rolladharani/OptiCrop)

---

## Overview

OptiCrop is a **Smart Agricultural Production Optimization Engine** designed to provide data-driven insights for agricultural decision-making.

The system analyzes important soil and environmental factors such as **Nitrogen (N), Phosphorous (P), Potassium (K), temperature, humidity, pH, and rainfall** to recommend suitable crops and assess crop suitability under given conditions.

The project combines **data preprocessing, machine learning, clustering, data visualization, and a Flask-based web application** to transform agricultural data into useful recommendations and insights.

---

## Problem Statement

Agricultural production depends significantly on soil quality and environmental conditions. Selecting a suitable crop without considering these factors can affect productivity and resource utilization.

OptiCrop addresses this problem by analyzing agricultural and environmental parameters and providing data-driven recommendations to support better crop selection and agricultural planning.

---

## Objectives

| No. | Objective |
|-----|-----------|
| 1 | Recommend suitable crops based on soil and environmental conditions. |
| 2 | Evaluate the suitability of a selected crop under given conditions. |
| 3 | Analyze crop-environment relationships using agricultural data. |
| 4 | Apply machine learning techniques to agricultural data. |
| 5 | Provide a web-based platform for agricultural decision support. |
| 6 | Support better production decisions and resource efficiency. |

---

## Key Features

| Feature | Description |
|---------|-------------|
| Crop Recommendation | Recommends a suitable crop using soil and environmental parameters. |
| Crop Suitability Assessment | Evaluates whether conditions are suitable for a selected crop. |
| Data Preprocessing | Processes the agricultural dataset and handles outliers before training. |
| Machine Learning | Uses Logistic Regression for crop classification. |
| K-Means Clustering | Analyzes groups of similar agricultural conditions. |
| Data Analysis | Performs correlation and feature distribution analysis. |
| Visualization | Generates analytical graphs including correlation and clustering visualizations. |
| Web Application | Provides an interactive interface using Flask. |
| User Authentication | Provides registration and login functionality. |

---

## Use Cases

### 1. Smart Crop Recommendation for Farmers

A farmer enters soil and environmental information such as Nitrogen, Phosphorous, Potassium, temperature, humidity, pH, and rainfall.

OptiCrop analyzes the provided parameters and recommends a suitable crop based on the trained model.

### 2. Crop Suitability and Environmental Assessment

A user can evaluate whether the current soil and environmental conditions are suitable for a particular crop.

The system analyzes the provided conditions and provides a crop suitability assessment.

### 3. Agricultural Research and Policy Planning

Agricultural researchers and stakeholders can use the system to analyze crop-environment relationships and identify patterns that can support data-driven agricultural planning.

---

## Input Parameters

| Parameter | Description |
|-----------|-------------|
| Nitrogen (N) | Soil nitrogen level |
| Phosphorous (P) | Soil phosphorous level |
| Potassium (K) | Soil potassium level |
| Temperature | Environmental temperature |
| Humidity | Environmental humidity |
| pH | Soil acidity/alkalinity level |
| Rainfall | Rainfall measurement |

---

## Machine Learning

### Data Preprocessing

The agricultural dataset is processed before model training. The project performs preprocessing and handles outliers to prepare the data for machine learning.

### Logistic Regression

OptiCrop uses **Logistic Regression** for multi-class crop classification. The trained model is saved as:

    model.pkl

### K-Means Clustering

The project uses **K-Means Clustering** to analyze groups of similar agricultural conditions.

An **Elbow Method** analysis is also generated as part of the clustering process.

### Generated Model Files

| File | Purpose |
|------|---------|
| `model.pkl` | Trained crop classification model |
| `crop_ranges.pkl` | Crop parameter range information |
| `cluster_insights.pkl` | Clustering-related insights |

---

## Dataset

The project uses the following agricultural dataset:

    Crop_recommendation.csv

The dataset contains soil and environmental parameters used for crop recommendation and model training.

| Dataset Attribute | Description |
|-------------------|-------------|
| N | Nitrogen |
| P | Phosphorous |
| K | Potassium |
| Temperature | Temperature condition |
| Humidity | Humidity condition |
| pH | Soil pH |
| Rainfall | Rainfall condition |
| Label | Crop category |

---

## Technology Stack

| Category | Technologies |
|----------|--------------|
| Programming Language | Python 3.11 |
| Web Framework | Flask |
| Machine Learning | Scikit-learn |
| Data Processing | Pandas, NumPy |
| Scientific Computing | SciPy |
| Data Visualization | Matplotlib, Seaborn |
| Database | SQLite |
| Frontend | HTML, CSS, JavaScript |
| Version Control | Git, GitHub |
| Deployment | Render |

---

## System Architecture

    User
      |
      v
    Web Interface
      |
      v
    Flask Application
      |
      +---------------------------+
      |                           |
      v                           v
    Input Processing          Database
      |
      v
    Machine Learning Model
      |
      +---------------------------+
      |                           |
      v                           v
    Crop Recommendation     Suitability Assessment
      |
      v
    Agricultural Insights

---

## Project Workflow

1. User provides soil and environmental parameters.
2. The Flask application receives the input.
3. The input is processed according to the project's data-processing workflow.
4. The trained machine learning model analyzes the parameters.
5. The application provides crop recommendations or suitability results.
6. Additional agricultural and clustering insights can be viewed through the application.

---


## Local Installation

### Prerequisites

| Requirement | Specification |
|-------------|---------------|
| Operating System | Windows / Linux / macOS |
| Python | Python 3.x |
| Recommended Python Version | Python 3.11 |
| IDE | Visual Studio Code or equivalent |
| Internet Connection | Required for installing dependencies |

### 1. Clone the Repository

    git clone https://github.com/rolladharani/OptiCrop.git
    cd OptiCrop

### 2. Install Dependencies

    pip install -r "5. Project Development Phase/requirements.txt"

For Windows with Python 3.11:

    py -3.11 -m pip install -r "5. Project Development Phase/requirements.txt"

### 3. Initialize the Database

    py -3.11 "5. Project Development Phase/database.py"

### 4. Train the Model

    py -3.11 "5. Project Development Phase/train_model.py"

### 5. Start the Application

    py -3.11 "5. Project Development Phase/app.py"

The application will run locally at:

    http://127.0.0.1:5000/

---

## Application Modules

| Module | Description |
|--------|-------------|
| Home | Main entry point of the OptiCrop application. |
| Find Your Crop | Accepts agricultural parameters and provides crop recommendations. |
| Suitability | Evaluates the suitability of a selected crop. |
| Insights | Provides agricultural data and machine learning insights. |
| Register | Provides user registration functionality. |
| Login | Provides user authentication functionality. |

---

## Project Documentation

Detailed project deliverables are available in:

    7. Project Documentation/

The documentation includes:

| Document | Description |
|----------|-------------|
| Project Executable Files | Installation and execution guide |
| Sample Project Documentation | System documentation and technical guide |

