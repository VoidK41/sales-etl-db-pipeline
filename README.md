
# 📈 Sales ETL + DB Pipeline

An interactive **Python ETL pipeline** for cleaning sales data, saving to a database, and generating summary reports.

---

## 📊 Features

✅ **ETL Process**
- Load messy multi-CSV (monthly sales data)
- Clean data (remove NaN, standardize Sales as numeric)
- Add month info column automatically based on file name

✅ **Database Integration**
- Save to SQLite database
- Auto-create index on Product column for faster queries
- Query total sales per product

✅ **Reports**
- Export sales summary (DB query version)
- Export sales summary (Pandas DataFrame version)
- Full logging to `etl.log` for traceability

---

## 🌍 Use Case

This project helps **small business owners, analysts, and data teams**:
- Automate consolidation of monthly sales data
- Generate clean, queryable sales database
- Create summary reports for business decision-making

---

## 🚀 Files Generated

- `output/sales_data.db` → SQLite database file  
- `output/sales_summary.csv` → Summary report (DB query version)  
- `output/sales_summary_v2.csv` → Summary report (Pandas DataFrame version)  
- `output/etl.log` → ETL process log  

---

## ⚙ How to Run

1️⃣ **Set up virtual environment**  

2️⃣ **Install requirements**
```bash
pip install -r requirements.txt
```

3️⃣ **Run ETL**
```bash
python etl/main.py
```

---

## 📌 Dependencies

- 🐍 Python 3.x  
- 📦 Pandas  
- ⚙ SQLAlchemy  

---

## 💡 Notes

Built using **Python 3, Pandas, SQLAlchemy** — modular and production-ready.  
Feel free to contact me for enhancements or to integrate this ETL with dashboards!

---

## 👨‍💻 Author

**Khairu Ikramendra**  
Available for freelance dashboard & data analytics projects.  
Let’s connect on [LinkedIn](https://www.linkedin.com/in/khairuikramendra/)  
Or explore more on [Upwork](https://www.upwork.com/freelancers/~017002e8546494c6e9?mp_source=share)
