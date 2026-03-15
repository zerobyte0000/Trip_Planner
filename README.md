# Trip Planner

## Travel Budget Planner (Flask Web App)

This is a **Flask-based web application** that helps users plan and manage travel budgets efficiently. The application allows users to create an account, set a trip budget, plan daily expenses, select destinations, and estimate overall travel costs.

The system organizes trip planning by calculating expenses for **food, accommodation, emergency funds, and travel duration**, helping users stay within their budget.

---

## Features

### 1. User Authentication
- Sign up and login functionality  
- Session-based authentication  
- Secure user data stored in JSON  

### 2. Budget Planning
- Enter total trip budget  
- Select trip start and end dates  
- Set number of travel days  

### 3. Expense Estimation
Calculate daily costs for:
- Food  
- Accommodation  
- Emergency funds  

Additional features:
- Automatic estimation of total trip cost  
- Remaining budget calculation  

### 4. Travel Planning
- Plan places to visit for each day  
- Suggest transport options based on remaining budget  

### 5. Transport Planning
Input travel details such as:
- Starting place  
- Destination  
- Travel date  
- Number of adults, seniors, and children  

### 6. Hotel Booking (Prototype)
- Choose number of rooms  
- Select room type  
- Manage number of guests  
- Sample hotel options included  

### 7. Trip Summary
- View all planned trip details in one place  

---

## Tech Stack

### Backend
- Python  
- Flask  

### Frontend
- HTML Templates (Jinja2)

### Data Storage
- JSON files  

### Session Management
- Flask Sessions  

---

## Project Structure

```
project/
│
├── app.py
│
├── data/
│   └── users.json
│
├── templates/
│   ├── login.html
│   ├── signin.html
│   ├── budget.html
│   ├── plan.html
│   ├── home.html
│   ├── flight_train.html
│   ├── hotel.html
│   └── my_trip.html
```

---

## Future Improvements

- Integrate real **flight and train APIs**
- Connect to **hotel booking APIs**
- Use **database (MySQL/PostgreSQL)** instead of JSON
- Add **expense analytics and charts**
- Implement **secure password hashing**
- Improve **transport suggestions using AI logic**

---

## How to Run

### 1. Install Flask

```bash
pip install flask
```

### 2. Run the Application

```bash
python app.py
```

### 3. Open in Browser

```
http://127.0.0.1:5000
```

---
