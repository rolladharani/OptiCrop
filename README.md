# Opti-Crop: ML-Powered Crop Recommendation & Soil Health Platform

Opti-Crop is an intelligent decision support system designed to help farmers, agricultural researchers, and extension offices optimize crop yields. Using historical soil-nutrient and meteorological datasets, it runs a 94%-accurate Logistic Regression model to recommend optimal crops based on N-P-K ratios, pH levels, temperature, humidity, and rainfall, alongside detailed organic and chemical soil correction procedures.

This repository follows the **AI, ML, and GenAI Track Project Template** structure.

---

## 📂 Repository Structure

The project deliverables are organized into the following phases:

### [1. Brainstorming & Ideation](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation)
Scoping user needs, defining problem statements, and mapping user empathy:
- [Brainstorming & Idea Prioritization](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Brainstorming%20%26%20Idea%20Prioritization.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Brainstorming%20%26%20Idea%20Prioritization.pdf))
- [Define Problem Statements](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Define%20Problem%20Statements%20.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Define%20Problem%20Statements%20.pdf))
- [Empathy Map](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Empathy%20Map.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/1.%20Brainstorming%20%26%20Ideation/Empathy%20Map.pdf))

### [2. Requirement Analysis](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis)
User journey analysis, system data flows, functional/non-functional criteria, and technology stacks:
- [Customer Journey Map](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Customer%20Journey%20Map.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Customer%20Journey%20Map.pdf))
- [Data Flow Diagram](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Data%20Flow%20Diagram.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Data%20Flow%20Diagram.pdf))
- [Solution Requirements](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Solution%20Requirements.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Solution%20Requirements.pdf))
- [Technology Stack](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Technology%20Stack.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/2.%20Requirement%20Analysis/Technology%20Stack.pdf))

### [3. Project Design Phase](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase)
System design, architectural design, database schemas, and product-market fit:
- [Problem-Solution Fit](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Problem-Solution%20Fit.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Problem-Solution%20Fit.pdf))
- [Proposed Solution Specifications](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Proposed%20Solution.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Proposed%20Solution.pdf))
- [Solution Architecture](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Solution%20Architecture.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/3.%20Project%20Design%20Phase/Solution%20Architecture.pdf))

### [4. Project Planning Phase](file:///c:/Users/muram/Documents/AntiGravity/4.%20Project%20Planning%20Phase)
Timelines, sprints, and milestones:
- [Project Planning](file:///c:/Users/muram/Documents/AntiGravity/4.%20Project%20Planning%20Phase/Project%20Planning.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/4.%20Project%20Planning%20Phase/Project%20Planning.pdf))

### [5. Project Development Phase](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase)
This directory contains the core source code of the web application along with development reviews:
- **Code Reviews:**
  - [Code-Layout, Readability and Reusability](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/Code-Layout,%20Readability%20and%20Reusability.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/Code-Layout,%20Readability%20and%20Reusability.pdf))
  - [Coding & Solution Highlights](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/Coding%20%26%20Solution.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/Coding%20%26%20Solution.pdf))
  - [No. of Functional Features Included](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/No.%20of%20Functional%20Features%20Included%20in%20the%20Solution.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/5.%20Project%20Development%20Phase/No.%20of%20Functional%20Features%20Included%20in%20the%20Solution.pdf))
- **Application Executables:**
  - `app.py`: Main Flask server entry point.
  - `database.py`: Schema constructor and seeding utilities.
  - `train_model.py`: Model fitting, cleaning, and analytics graphics generator.
  - `Crop_recommendation.csv`: Primary agricultural data table.
  - `static/` & `templates/`: Interface assets and dynamic HTML templates.

### [6. Project Testing](file:///c:/Users/muram/Documents/AntiGravity/6.Project%20Testing)
Machine Learning validation stats and route performance testing:
- [Performance Testing Reports](file:///c:/Users/muram/Documents/AntiGravity/6.Project%20Testing/Performance%20Testing.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/6.Project%20Testing/Performance%20Testing.pdf))

### [7. Project Documentation](file:///c:/Users/muram/Documents/AntiGravity/7.Project%20Documentation)
Installation instructions and comprehensive guide:
- [Project Executable Files Installation Guide](file:///c:/Users/muram/Documents/AntiGravity/7.Project%20Documentation/Project%20Executable%20Files.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/7.Project%20Documentation/Project%20Executable%20Files.pdf))
- [Sample Project Documentation](file:///c:/Users/muram/Documents/AntiGravity/7.Project%20Documentation/Sample%20Project%20Documentation.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/7.Project%20Documentation/Sample%20Project%20Documentation.pdf))

### [8. Project Demonstration](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration)
Demonstration scripts, organizational divisions, risk mitigation, and scaling guides:
- [Communication & Slide Layout](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Communication.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Communication.pdf))
- [Demonstration of Proposed Features](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Demonstration%20of%20Proposed%20Features.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Demonstration%20of%20Proposed%20Features.pdf))
- [Project Demo Planning Checklist](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Project%20Demo%20Planning.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Project%20Demo%20Planning.pdf))
- [Scalability & Future Scope Roadmap](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Scalability%20%26%20Future%20Plan.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Scalability%20%26%20Future%20Plan.pdf))
- [Team Involvement in Demonstration](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Team%20Involvement%20in%20Demonstration.md) (and [PDF version](file:///c:/Users/muram/Documents/AntiGravity/8.Project%20Demonstration/Team%20Involvement%20in%20Demonstration.pdf))

---

## 🚀 Quick Start Guide

To run the application locally:

1. **Install Dependencies:**
   ```bash
   pip install -r "5. Project Development Phase/requirements.txt"
   ```

2. **Initialize Database:**
   ```bash
   python "5. Project Development Phase/database.py"
   ```

3. **Train Model & Generate Charts:**
   ```bash
   python "5. Project Development Phase/train_model.py"
   ```

4. **Start Application Server:**
   ```bash
   python "5. Project Development Phase/app.py"
   ```
   Open `http://127.0.0.1:5000/` in your browser.
