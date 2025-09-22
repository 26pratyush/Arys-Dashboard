
# 🚗 Arys Garage Sales Dashboard  

An interactive **Sales Dashboard** built for **Arys Garage Pvt. Ltd.** to visualize:  
- Sales trends over time  
- Product line contributions  
- Country-wise performance  
- Order status distributions  
- KPIs (Total Sales, Total Orders, Avg Order Value)  
- Top 5 Customers by sales  

The project uses:  
- **Python (Pandas, NumPy, Faker)** – dataset generation & preprocessing  
- **Flask** – backend APIs  
- **Streamlit + Plotly** – frontend dashboard  
- **Render** – deployment platform  

---

## 🌍 Live Demo  

The dashboard is hosted on **Render**:  
👉 [https://arys-frontend.onrender.com/](https://arys-frontend.onrender.com/)  

⚠️ *Note*: Since this is hosted on Render’s **free tier**, the server goes to sleep after ~15 minutes of inactivity.  
It may take 1–2 minutes to restart when you open the link. If it doesn’t load immediately, try refreshing or opening in a new tab.  

---
## Screenshots  

Below are some key views of the dashboard:
![WhatsApp Image 2025-09-22 at 17 07 25_ca348b4c](https://github.com/user-attachments/assets/926b5ae5-bf86-4252-b32e-3a4bcfc35224)
![WhatsApp Image 2025-09-22 at 17 08 13_de44ff91](https://github.com/user-attachments/assets/62e51187-14ab-42cc-8509-0232faeca7bb)
![WhatsApp Image 2025-09-22 at 17 08 47_3724e5eb](https://github.com/user-attachments/assets/026c5b13-2199-4f9e-b2ae-f4c6d5934652)
![WhatsApp Image 2025-09-22 at 17 16 45_8a23239f](https://github.com/user-attachments/assets/2c621fc5-44ca-4cc4-bbe3-ad67d1d9c056)
![WhatsApp Image 2025-09-22 at 17 09 43_7036960b](https://github.com/user-attachments/assets/ef6caaff-6c91-4a38-9c69-e3f5366c5651)
![WhatsApp Image 2025-09-22 at 17 10 03_44aa8d56](https://github.com/user-attachments/assets/6ccc8e88-d5b4-48f4-85cc-313f9f7d678a)







## 📂 Project Structure  

```

Arys-Dashboard/
│
├── backend/                # Flask backend with APIs
│   ├── app.py
│   └── ...
│
├── frontend/               # Streamlit dashboard
│   ├── dashboard.py
│   └── ...
│
├── data/                   # Raw and processed datasets
│   ├── sales\_data.csv
│   ├── sales\_data\_cleaned.csv
│   └── ...
│
├── notebooks/              # Preprocessing Jupyter notebooks
│   └── data\_preprocessing.ipynb
├── requirements.txt        # Python dependencies
├── Procfile                # For Render deployment
├── render.yaml             # Render service definition
└── README.md               # Project documentation

````

---

## 🛠 Run Locally  

If you prefer to run the dashboard locally, follow these steps:  

### 1. Clone Repository  
```bash
git clone https://github.com/26pratyush/Arys-Dashboard
cd Arys-Dashboard
pip install -r requirements.txt
````

### 2. Update API URL

```bash
cd frontend
```

Open `dashboard.py` and change the API URL from:

```python
API_URL = "https://arys-backend.onrender.com"
```

to

```python
API_URL = "http://127.0.0.1:5000/"
```

### 3. Start Backend

```bash
cd ..
cd backend
python app.py
```

### 4. Start Frontend

In a **new terminal**, run:

```bash
cd frontend
python -m streamlit run dashboard.py
```

### 5. View Dashboard

Open [http://localhost:8501/](http://localhost:8501/) in your browser, while the application is still running.

---

## 📞 Support

If you face any issues, please reach out: **9741576165**


