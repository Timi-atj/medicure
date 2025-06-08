MedMind — AI-Powered Symptom-Based Disease Prediction System
________________________________________
🏫 Institution:
Redeemer’s University, Ede, Nigeria
Department of Computer Engineering
👨‍💻 Team Members:
•	Anigioro Timilehin 
•	Egbule Ebubechukwu
•	Olaoluwa Israel
________________________________________
Project Overview
MedMind is a smart, AI-enhanced web application designed to revolutionize healthcare empower individuals through artificial intelligence by offering intelligent disease prediction based on reported symptoms, offering in home remedies for immediate medical attention and also connecting to close by health services for easy access to health Facilities through machine learning and an intuitive and user-friendly interface. So basically users receive a list of likely conditions, confidence scores, and recommended home remedies — all while also being able to ask general health diagnosis using built-in AI capabilities.
MedMind doesn't replace doctors — instead, it puts accessible, AI-powered health support at your fingertips, especially for those in underserved or remote regions.
________________________________________
Objectives
•	Provide a smart, accessible symptom-checking tool.
•	Predict likely diseases with confidence scores.
•	Recommend basic home remedies for immediate relief.
•	Support users with AI-driven Q&A.
•	Assist, not replace, healthcare professionals.
________________________________________

Key Features
•	Symptom-Based Prediction
. Takes symptoms as input from user
. Gives user co-occurring symptoms to streamline accuracy of set of diseases
. Returns an accurate set of diseases related to the given symptoms with confidence scores
. the user-interface is friendly and easily navigable

•	AI Chat for Health Queries
. Integrated a chatbot in the home page for asking medical related issues
. Offers motivational quotes to help with users 
. Engages users in intuitive and friendly conversations 
. Streamlined to focus on health and Medical Support
. Gives AI driven suggestions

•	Home Remedies and First Aid Suggestions
. Gives Home remedies for each disease for immediate medical attention
. Shows readily available materials that can be used to support the users health condition

•	Web Interface Built with Flask



________________________________________
Technical Stack
Component	Technology
Frontend Framework	HTML, CSS, Javascript
Language	Python
Backend Framework	Flask
ML Models	Logistic Regression, SVM, MLP, ANN, XGBoost
Data Handling	Pandas, NumPy
Deployment	Docker, AWS EC2, WAF, Load Balancer
AI Interface	Integrated LLM-based Q&A
________________________________________
Project Structure
•	app.py: Routes and handles user requests
•	Model_latest.py: Core ML prediction logic
•	Treatment.py: Maps predictions to remedies
•	Preprocess.py: Data cleaning pipeline
•	templates/static/: Frontend assets
•	requirements.txt: Dependency management
________________________________________
Dataset Details
•	Source: Kaggle
•	Rows: 8,836 | Columns: 489
•	Diseases: 261 distinct conditions
•	Symptom combinations were generated to simulate realistic user inputs and increase model robustness.



________________________________________
Model Pipeline & Performance
1. Preprocessing
•	One-hot encoding for symptoms
•	Synthetic data augmentation for minority classes
•	Removal of noise and missing entries
2. Model Selection
•	Best model: Random Forest
•	Accuracy: ~94%
•	Models compared: Naive Bayes, XGBoost, ANN, SVM
3. Prediction Sample
{
  "symptoms": ["headache", "fatigue", "nausea"],
  "top_predictions": [
    {"name": "Migraine", "probability": 0.72},
    {"name": "Dengue", "probability": 0.65},
    {"name": "Anemia", "probability": 0.62}
  ]
}
________________________________________
Testing & Validation
•	Validated symptom combinations through research
•	Cross-validated model using stratified k-fold
•	Unit-tested all API endpoints for stability
•	Simulated 50+ real-life user sessions
________________________________________
Usage
 Example Flow:
1.	User Visit → Access TotalCURE via browser
2.	Input Symptoms → e.g., "headache, vomiting, dizziness"
3.	Prediction Returned → Likely diseases with confidence levels
4.	Remedy Displayed → Home care guidance provided
5.	Ask AI a Question → "What should I eat for migraines?"
👥 Ideal For:
•	Individuals in remote/rural areas
•	Telemedicine platforms
•	Mobile health teams & NGOs
•	Medical students practicing diagnostics
________________________________________
Project Impact
•	Accessibility: Provides basic diagnostic support to areas with few medical professionals
•	Awareness: Encourages users to understand symptoms early
•	Portability: Designed to eventually scale to mobile devices
•	Collaboration: Can assist community health workers as a decision-support tool
•	Triage Support: Reduces hospital load by guiding users before they panic or self-medicate
________________________________________
Deployment Strategy
STEP	TOOL
CONTAINERIZATION	Docker
CLOUD HOSTING	AWS EC2
SECURITY	AWS WAF + Load Balancer
FUTURE PLANS	Mobile App via React Native
________________________________________

Disclaimer
MedMind is not a substitute for professional medical advice, diagnosis, or treatment.
It is intended to assist healthcare decisions — not replace healthcare providers.
Always consult a qualified medical professional for serious health concerns.
________________________________________
Acknowledgment
We thank our the open-source community for their invaluable guidance and resources. Special thanks to Kaggle for dataset access and GitHub for enabling collaborative development.
