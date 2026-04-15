from flask import Flask, render_template, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)


df = pd.read_csv('train.csv')
if 'Student_ID' in df.columns: df = df.drop('Student_ID', axis=1)


le = LabelEncoder()
for col in df.select_dtypes(include='object').columns:
    df[col] = le.fit_transform(df[col])


X = df.drop('Placement_Status', axis=1)
y = df['Placement_Status']

model = RandomForestClassifier(random_state=42)
model.fit(X, y)

@app.route('/', methods=['GET', 'POST'])
def home():
    prediction_text = ""
    
    if request.method == 'POST':
        try:
            
            age = int(request.form['age'])
            cgpa = float(request.form['cgpa'])
            backlogs = int(request.form['backlogs'])
            comm = int(request.form['communication'])
            coding = int(request.form['coding'])  
            
            
            input_data = pd.DataFrame({
                'Age': [age],
                'Gender': [0], 'Degree': [0], 'Branch': [0],
                'CGPA': [cgpa],
                'Internships': [1], 'Projects': [2], 
                'Coding_Skills': [coding],        
                'Communication_Skills': [comm],
                'Aptitude_Test_Score': [70], 'Soft_Skills_Rating': [4.0],
                'Certifications': [0], 'Backlogs': [backlogs]
            })
            
            pred = model.predict(input_data)
            
            if pred[0] == 1:
                prediction_text = " You are likely to be PLACED!"
            else:
                prediction_text = " You might NOT get placed."
                
        except Exception as e:
            prediction_text = f"Error: {e}"

    return render_template('index.html', prediction_text=prediction_text)

if __name__ == '__main__':
    app.run(debug=True)