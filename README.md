# Bluestock Mutual Fund Analytics Capstone

This repository contains the complete 7-Day Capstone Project for the Bluestock Fintech Data Analyst Internship.

## 📂 Project Structure

*   `Day 1/`: Data Ingestion scripts (ETL extraction, API fetching)
*   `Day 2/`: Data Cleaning scripts, SQLite Database setup, and Data Dictionary
*   `Day 3/`: Exploratory Data Analysis (EDA) Jupyter Notebook
*   `Day 4/`: Fund Performance Analytics Notebook (Sharpe, CAGR, Alpha, Beta)
*   `Day 5/`: Interactive **Streamlit** Dashboard (`app.py`)
*   `Day 6/`: Advanced Analytics (VaR, CVaR, Cohort Analysis) and `recommender.py`
*   `Day 7/`: Final Report Template and Presentation resources
*   `data/`: Shared folder containing `raw/`, `processed/`, and `db/` (bluestock_mf.db)

## 🚀 How to Run the Project

1.  **Environment Setup:** Ensure you have Python installed. Install requirements:
    ```bash
    pip install pandas numpy matplotlib seaborn plotly sqlalchemy requests streamlit
    ```

2.  **View the Notebooks:** Open the `.ipynb` files in `Day 3`, `Day 4`, and `Day 6` using Jupyter Notebook, VS Code, or Google Colab.

3.  **Run the Interactive Dashboard (Day 5 Bonus!):**
    Open your terminal/command prompt, navigate to this project folder, and run:
    ```bash
    streamlit run "Day 5/app.py"
    ```
    This will launch a beautiful interactive dashboard in your web browser!

4.  **Fund Recommender:** Run the script in your terminal to see fund recommendations based on risk:
    ```bash
    python "Day 6/recommender.py"
    ```

## 📤 Project Submission Guidelines

The Bluestock submission portal requires you to upload a Google Drive link to a master folder named `YourName_Submission` containing 5 specific sub-folders.

To make this simple, we have provided an automated packager script in the root directory.

### 1. Package the Project
Run this command in your terminal/command prompt:
```bash
python package_submission.py
```
This script will prompt you for your name and automatically create a `Submission_Package/YourName_Submission` folder with the following structure:
*   `Source Code/` (Contains all day scripts, notebooks, and requirements)
*   `Datasets/` (Contains all raw and cleaned CSVs and the SQLite database)
*   `Documentation/` (Contains reports, data dictionary, and READMEs)
*   `PPT_Slides/` (Placeholder directory for your presentation slides)
*   `Demo Video/` (Placeholder directory for your 2-minute walkthrough video)

### 2. Finalize and Submit
1.  Add your presentation PowerPoint slides to the `PPT_Slides/` folder.
2.  Add your 2-minute project walkthrough video to the `Demo Video/` folder.
3.  Upload the entire `YourName_Submission` folder to your **Google Drive**.
4.  Right-click the folder on Google Drive -> **Share** -> Set access to **"Anyone with the link"** as **Viewer**.
5.  Copy the link and paste it into your Bluestock Project Submission page!

