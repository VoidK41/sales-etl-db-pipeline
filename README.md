
# 📈 Sales ETL + DB Pipeline

An interactive **Python ETL pipeline** for cleaning messy sales data, saving to a database, generating summary reports, and visualizing sales trends.

---

## 📊 Features

✅ **ETL Process**
- Load multi-CSV (monthly sales data)
- Clean data: handle NaN, convert messy `Sales` column to numeric, remove outliers
- Add `Month` column automatically based on file name

✅ **Database Integration**
- Save cleaned data to SQLite database
- Auto-create index on `Product` column for faster queries
- Run SQL queries for total sales per product & month

✅ **Reports & Visualization**
- Export sales summary CSV from DB query
- Generate bar chart of total sales per month (`output/sales_per_month.png`)
- Full logging to `output/etl.log` for traceability

---

## 🌍 Use Case

This project helps **small businesses, analysts, and data teams**:
- Automate monthly sales data consolidation
- Build a clean, queryable sales database
- Generate reports & visual insights for better decisions

---

## 🚀 Generated Files

- `output/sales_data.db` → SQLite database file  
- `output/monthly_sales_summary.csv` → Sales summary (DB query)  
- `output/sales_per_month.png` → Bar chart of sales by month  
- `output/etl.log` → Detailed ETL process log  

---

## ⚙ How to Run

1️⃣ **(Recommended)** Set up virtual environment  
```bash
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

2️⃣ **Install dependencies**
```bash
pip install -r requirements.txt
```

3️⃣ **Run ETL pipeline**
```bash
python etl/main.py
```

---

## 📌 Dependencies

- 🐍 Python 3.x  
- 📦 Pandas  
- ⚙ SQLAlchemy  
- 📈 Matplotlib  

---

## 💡 Notes

Built with clean, modular code — ready for production or extension into dashboards.  
✅ You can easily integrate this pipeline into **Streamlit**, **BI tools**, or cloud databases.

---

## 👨‍💻 Author

**Khairu Ikramendra**  
💼 *Freelance Dashboard & Data Analytics Developer*  
🔗 [LinkedIn](https://www.linkedin.com/in/khairuikramendra/)  
🔗 [Upwork](https://www.upwork.com/freelancers/~017002e8546494c6e9?mp_source=share)  

---

💬 *Need help customizing this ETL for your business? Feel free to reach out!*  