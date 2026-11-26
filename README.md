# Personal Finance CSV Reporter

**Project #20 – LocalImpact Challenge**

## Requirements
- Python 3.10 or newer
- Matplotlib (only needed for charts)

## Run in VS Code
1. Extract the ZIP file.
2. Open the extracted `Personal_Finance_CSV_Reporter` folder in VS Code.
3. Open Terminal → New Terminal.
4. (Optional) Create a virtual environment:
   - Windows: `py -m venv .venv` then `.venv\\Scripts\\activate`
   - macOS/Linux: `python3 -m venv .venv` then `source .venv/bin/activate`
5. Install chart library: `python -m pip install -r requirements.txt`
6. Run: `python app.py` (Windows can also use `py app.py`).

## Demo
- Choose option 2 and import `sample_transactions.csv` (enter its full path, or copy it into the folder and enter `sample_transactions.csv`).
- Choose option 4 to show income, expenses and balance.
- Choose option 7 to create a category expense chart.
- Choose option 6 to export a text report.
- Choose option 8 to exit. Records are saved in `data/transactions.csv` and `data/transactions.json`.

## CSV format
Required column names: `date,type,category,description,amount`
- Date format: YYYY-MM-DD
- Type: income or expense
- Amount: positive number

The program validates imported rows and skips invalid entries. All data is stored locally.
