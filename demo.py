import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from fastapi import FastAPI

# Simulated Task Dataset
def generate_task_data(num_tasks=100, num_users=10):
    np.random.seed(42)  # For reproducibility
    data = {
        "user_id": np.random.randint(1, num_users + 1, num_tasks),  # Assigning tasks to users
        "task_id": range(1, num_tasks + 1),
        "task_description": ["Task " + str(i) for i in range(1, num_tasks + 1)],
        "due_days": np.random.randint(1, 30, num_tasks),  # Days until due
        "completed_days": np.random.randint(0, 40, num_tasks),  # Days taken to complete
        "past_overdue": np.random.choice([0, 1], num_tasks, p=[0.7, 0.3])  # 30% were overdue before
    }
    df = pd.DataFrame(data)
    df["overdue"] = (df["completed_days"] > df["due_days"]).astype(int)
    return df

df = generate_task_data()

# Features & Target
X = df[["user_id", "due_days", "completed_days", "past_overdue"]]
y = df["overdue"]

# Train/Test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Model Training
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print("Model Accuracy:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred))

# FastAPI Setup
app = FastAPI()

@app.post("/predict")
def predict_task(user_id: int, due_days: int, completed_days: int, past_overdue: int):
    input_data = np.array([[user_id, due_days, completed_days, past_overdue]])
    prediction = model.predict(input_data)[0]
    if prediction == 1:
        priority = "High"
    elif abs(due_days - completed_days) <= 3:
        priority = "Medium"
    else:
        priority = "Low"
    return {"user_id": user_id, "overdue_prediction": bool(prediction), "priority": priority}

@app.post("/create_task")
def create_task(user_id: int, task_description: str, due_days: int, completed_days: int, past_overdue: int):
    global df  # Move global declaration to the top
    
    task_id = len(df) + 1
    new_task = pd.DataFrame({
        "user_id": [user_id],
        "task_id": [task_id],
        "task_description": [task_description],
        "due_days": [due_days],
        "completed_days": [completed_days],
        "past_overdue": [past_overdue],
        "overdue": [(completed_days > due_days)]
    })
    
    df = pd.concat([df, new_task], ignore_index=True)
    return {"message": "Task created successfully", "task_id": task_id}


@app.get("/get_tasks")
def get_tasks(user_id: int):
    user_tasks = df[df["user_id"] == user_id].to_dict(orient="records")
    return {"user_id": user_id, "tasks": user_tasks}

# Run with: uvicorn filename:app --reload
