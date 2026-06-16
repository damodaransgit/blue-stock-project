"""
Day 7 - Generate Final Report PDF
Generates a professional 15+ page Final Report for the Bluestock MF Capstone.
"""
import os
from fpdf import FPDF

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(SCRIPT_DIR, '..')
OUTPUT_PATH = os.path.join(SCRIPT_DIR, 'Final_Report.pdf')

# Check for dashboard screenshots
SCREENSHOT_DIR = os.path.join(PROJECT_ROOT, 'Day 5', 'Dashboard_img')


class ReportPDF(FPDF):
    """Custom PDF class with header/footer branding."""

    def header(self):
        if self.page_no() > 1:
            self.set_draw_color(0, 102, 204)
            self.set_line_width(0.5)
            self.line(10, 10, 200, 10)
            self.ln(6)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 16)
        self.set_text_color(0, 51, 102)
        self.cell(0, 12, title, new_x="LMARGIN", new_y="NEXT")
        self.set_draw_color(0, 102, 204)
        self.set_line_width(0.8)
        self.line(10, self.get_y(), 120, self.get_y())
        self.ln(6)

    def section_title(self, title):
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(0, 76, 153)
        self.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")
        self.ln(2)

    def body_text(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.multi_cell(0, 6, text)
        self.ln(3)

    def bullet(self, text):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        x = self.get_x()
        self.cell(6, 6, '-')
        self.multi_cell(0, 6, text)
        self.ln(1)

    def bold_bullet(self, bold_part, normal_part):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(30, 30, 30)
        self.cell(6, 6, '-')
        self.set_font('Helvetica', 'B', 10)
        self.write(6, bold_part)
        self.set_font('Helvetica', '', 10)
        self.write(6, normal_part)
        self.ln(8)

    def add_screenshot(self, img_path, caption):
        if os.path.exists(img_path):
            self.ln(4)
            avail_w = self.w - self.l_margin - self.r_margin
            self.image(img_path, x=self.l_margin, w=avail_w)
            self.ln(2)
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(80, 80, 80)
            self.cell(0, 6, caption, align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(4)
        else:
            self.set_font('Helvetica', 'I', 9)
            self.set_text_color(150, 150, 150)
            self.cell(0, 6, f'[Screenshot not found: {caption}]', align='C', new_x="LMARGIN", new_y="NEXT")
            self.ln(4)


def build_report():
    pdf = ReportPDF()
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)

    # ====== COVER PAGE ======
    pdf.add_page()
    pdf.ln(40)
    pdf.set_font('Helvetica', 'B', 28)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 14, 'Bluestock Mutual Fund', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 14, 'Analytics Capstone', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)
    pdf.set_draw_color(0, 102, 204)
    pdf.set_line_width(1.2)
    pdf.line(60, pdf.get_y(), 150, pdf.get_y())
    pdf.ln(10)
    pdf.set_font('Helvetica', '', 14)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, 'End-to-End Data Engineering, Dashboarding & Risk Analysis', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(60, 60, 60)
    pdf.cell(0, 8, 'Submitted To: Bluestock Fintech', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Submitted By: Damodara P | Data Analyst Intern', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Email: pdamodaran2000@gmail.com', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Date: June 2026', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(30)
    pdf.set_font('Helvetica', 'I', 9)
    pdf.set_text_color(150, 150, 150)
    pdf.cell(0, 6, 'Confidential - For Internal Review Only', align='C', new_x="LMARGIN", new_y="NEXT")

    # ====== TABLE OF CONTENTS ======
    pdf.add_page()
    pdf.chapter_title('Table of Contents')
    pdf.ln(4)
    toc_items = [
        ('1.', 'Executive Summary'),
        ('2.', 'Data Architecture & Ingestion'),
        ('3.', 'ETL Process & Data Cleaning'),
        ('4.', 'Exploratory Data Analysis (EDA)'),
        ('5.', 'Fund Performance Analytics'),
        ('6.', 'Advanced Risk Metrics & Modeling'),
        ('7.', 'Dashboard Implementation'),
        ('8.', 'Fund Recommendation Engine'),
        ('9.', 'Strategic Recommendations'),
        ('10.', 'Limitations & Future Scope'),
    ]
    for num, title in toc_items:
        pdf.set_font('Helvetica', '', 12)
        pdf.set_text_color(30, 30, 30)
        pdf.cell(12, 10, num)
        pdf.set_font('Helvetica', '', 12)
        pdf.cell(0, 10, title, new_x="LMARGIN", new_y="NEXT")

    # ====== CHAPTER 1: EXECUTIVE SUMMARY ======
    pdf.add_page()
    pdf.chapter_title('1. Executive Summary')
    pdf.body_text(
        'This report details the end-to-end development of the Bluestock Mutual Fund Analytics '
        'platform, a comprehensive 7-day capstone project. The primary objective was to architect '
        'a robust data pipeline capable of ingesting, cleaning, and analyzing massive volumes of '
        'mutual fund data, ultimately surfacing actionable insights through interactive dashboards '
        'and recommendation algorithms.'
    )
    pdf.body_text(
        'Over the course of the project, 17 raw datasets comprising over 127,000 rows of data '
        'were ingested from AMFI public sources. A local SQLite database (bluestock_mf.db) was '
        'engineered using a Star Schema design to act as the single source of truth. Leveraging '
        'Python (Pandas, NumPy, SciPy), advanced financial metrics - including Sharpe Ratios, '
        'Value at Risk (VaR), and Alpha/Beta - were calculated for 40 mutual fund schemes.'
    )
    pdf.body_text(
        'Finally, an interactive 4-page Power BI dashboard was deployed, accompanied by a '
        'Python-based algorithmic fund recommendation engine capable of suggesting optimized '
        'funds based on investor risk profiles.'
    )
    pdf.section_title('Key Achievements')
    pdf.bold_bullet('Data Pipeline: ', 'Automated ETL processing 127,000+ rows across 17 datasets.')
    pdf.bold_bullet('Database: ', 'Star-schema SQLite DB with 11 validated tables and 100% row-count match.')
    pdf.bold_bullet('Analytics: ', 'Calculated CAGR, Sharpe, Sortino, Alpha, Beta, VaR, CVaR, and HHI for all funds.')
    pdf.bold_bullet('Dashboard: ', '4-page interactive Power BI dashboard with drill-through and slicers.')
    pdf.bold_bullet('Recommender: ', 'Algorithmic engine mapping risk profiles to Top 3 funds by Sharpe Ratio.')

    # ====== CHAPTER 2: DATA ARCHITECTURE ======
    pdf.add_page()
    pdf.chapter_title('2. Data Architecture & Ingestion')
    pdf.body_text(
        'The foundation of the analytics platform relies on diverse data sources, simulating '
        'real-world API pulls and batch file drops from financial institutions. A total of 10 '
        'core CSV datasets were sourced from the Association of Mutual Funds in India (AMFI) '
        'and supplementary financial data providers.'
    )
    pdf.section_title('2.1 Data Sources')
    pdf.bold_bullet('Fund Master (01_fund_master.csv): ',
                     'Core metadata mapping AMFI codes to Scheme Names, Categories, Fund Houses, '
                     'Expense Ratios, and SEBI Risk Categories for 40 schemes.')
    pdf.bold_bullet('Historical NAV (02_nav_history.csv): ',
                     'Daily Net Asset Values spanning Jan 2022 to Dec 2025 for rolling return '
                     'and volatility calculations. Contains 64,320 cleaned records.')
    pdf.bold_bullet('AUM by Fund House (03_aum_by_fund_house.csv): ',
                     'Monthly Assets Under Management aggregated by AMC, used for market share analysis.')
    pdf.bold_bullet('SIP Inflows (04_monthly_sip_inflows.csv): ',
                     'Monthly SIP contribution data including active accounts, new registrations, and YoY growth.')
    pdf.bold_bullet('Category Inflows (05_category_inflows.csv): ',
                     'Net inflow/outflow data segmented by fund category (Equity, Debt, Hybrid) by month.')
    pdf.bold_bullet('Industry Folios (06_industry_folio_count.csv): ',
                     'Monthly folio counts broken down by asset class.')
    pdf.bold_bullet('Investor Transactions (08_investor_transactions.csv): ',
                     'Granular transaction logs (32,778 records) with demographics, geography, and payment modes.')
    pdf.bold_bullet('Benchmark Indices (10_benchmark_indices.csv): ',
                     'NIFTY 50 and NIFTY 100 daily closing values for comparative performance benchmarking.')

    pdf.section_title('2.2 Data Ingestion Pipeline')
    pdf.body_text(
        'A Python-based ingestion script (data_ingestion.py) was developed to automatically '
        'scan the data/raw/ directory, validate file integrity, detect column types, and produce '
        'a comprehensive data quality report. The script performed cross-validation of AMFI codes '
        'across all tables, achieving a 100% match rate between the Fund Master and NAV History.'
    )

    # ====== CHAPTER 3: ETL ======
    pdf.add_page()
    pdf.chapter_title('3. ETL Process & Data Cleaning')
    pdf.body_text(
        'Raw financial data is notoriously noisy. A strict Extract, Transform, Load (ETL) pipeline '
        'was developed in Python to enforce data integrity before any analytics were performed.'
    )
    pdf.section_title('3.1 Transformation Steps')
    pdf.bold_bullet('Column Standardization: ',
                     'All column names were converted to snake_case. Date strings were parsed '
                     'into proper datetime objects with timezone-naive formatting.')
    pdf.bold_bullet('Anomaly Resolution: ',
                     'Missing AMFI codes and invalid zero-NAV entries were systematically '
                     'identified and removed. Transaction amounts below Rs.100 were flagged as potential errors.')
    pdf.bold_bullet('Dimensional Modeling: ',
                     'A dim_date table was dynamically generated with 1,608 rows encompassing '
                     'Year, Quarter, Month, Day-of-Week, and Fiscal Year flags to support '
                     'advanced time-series slicing in BI tools.')
    pdf.bold_bullet('Deduplication: ',
                     'Duplicate NAV records (same fund, same date) were removed using a '
                     'keep-last strategy to retain the most recent correction.')

    pdf.section_title('3.2 Database Loading')
    pdf.body_text(
        'The cleaned Pandas DataFrames were mapped to appropriate SQL data types and pushed '
        'into bluestock_mf.db (SQLite) across 11 distinct tables. An automated validation '
        'step compared the row count in each SQL table against the source DataFrame, achieving '
        'a perfect 100% match across all tables.'
    )
    pdf.section_title('3.3 Star Schema Design')
    pdf.body_text(
        'The database follows a Star Schema architecture with fact tables (fact_nav, '
        'fact_transactions, fact_performance) surrounded by dimension tables (dim_fund, dim_date). '
        'This design enables efficient OLAP-style queries and seamless integration with BI dashboards.'
    )

    # ====== CHAPTER 4: EDA ======
    pdf.add_page()
    pdf.chapter_title('4. Exploratory Data Analysis')
    pdf.body_text(
        'Initial exploration of the cleaned datasets was performed in a Jupyter Notebook '
        '(03_eda_analysis.ipynb) using Matplotlib and Seaborn for static visualizations and '
        'Plotly for interactive charts.'
    )
    pdf.section_title('4.1 Industry AUM Trends')
    pdf.body_text(
        'The Total Industry AUM crossed Rs.81 Lakh Crore by end of 2025, representing a '
        'compound annual growth rate of approximately 18% over the 4-year observation window. '
        'The Top 10 AMCs command over 80% of total industry AUM, indicating a highly '
        'concentrated market structure dominated by SBI, HDFC, and ICICI Prudential.'
    )
    pdf.section_title('4.2 The SIP Revolution')
    pdf.body_text(
        'Systematic Investment Plan (SIP) inflows demonstrated exponential growth throughout '
        'the observation period, reaching an all-time high of Rs.31,002 Crore in monthly inflows '
        'by December 2025. Active SIP accounts surpassed 26 Crore, with Year-over-Year growth '
        'rates consistently exceeding 15%. This confirms a structural shift in Indian retail '
        'investor behavior from lumpsum to disciplined, automated investing.'
    )
    pdf.section_title('4.3 Demographic Insights')
    pdf.body_text(
        'Analysis of the 32,778 investor transaction records revealed several key demographic patterns:'
    )
    pdf.bold_bullet('Age Distribution: ',
                     'The 26-35 age cohort dominates SIP investments, contributing the highest '
                     'average ticket size among all groups.')
    pdf.bold_bullet('Geographic Spread: ',
                     'While Maharashtra and Delhi NCR remain the largest contributors by volume, '
                     'Tier-2 and Tier-3 cities are showing the fastest growth rates, suggesting '
                     'deepening financial inclusion.')
    pdf.bold_bullet('Transaction Split: ',
                     'SIPs account for the majority of transactions by volume, though Lumpsum '
                     'investments dominate by total value, particularly during market correction periods.')

    # ====== CHAPTER 5: PERFORMANCE ======
    pdf.add_page()
    pdf.chapter_title('5. Fund Performance Analytics')
    pdf.body_text(
        'To evaluate true fund quality beyond simple trailing returns, a quantitative scorecard '
        'was engineered using daily NAV histories. All calculations were performed in Python '
        '(04_performance_analytics.ipynb) using Pandas and NumPy.'
    )
    pdf.section_title('5.1 CAGR (Compound Annual Growth Rate)')
    pdf.body_text(
        'CAGR was calculated over 1-year, 3-year, and 5-year horizons using the formula: '
        'CAGR = (NAV_end / NAV_start)^(1/n) - 1. This metric normalizes returns across '
        'different time periods, enabling fair comparison between funds with different launch dates.'
    )
    pdf.section_title('5.2 Sharpe Ratio')
    pdf.body_text(
        'The Sharpe Ratio measures risk-adjusted returns: Sharpe = (Rp - Rf) / Std(Rp), '
        'where Rp is the portfolio return, Rf is the risk-free rate (set to 6.5% based on '
        'RBI repo rate proxy), and Std(Rp) is the standard deviation of daily returns. '
        'Annualization was performed using sqrt(252) trading days. A higher Sharpe indicates '
        'better return per unit of risk taken.'
    )
    pdf.section_title('5.3 Sortino Ratio')
    pdf.body_text(
        'The Sortino Ratio refines the Sharpe by focusing exclusively on downside risk: '
        'Sortino = (Rp - Rf) / Downside_Std, where Downside_Std uses only negative return days. '
        'This is particularly valuable for risk-averse investors who are primarily concerned '
        'about losses rather than overall volatility.'
    )
    pdf.section_title('5.4 Alpha & Beta')
    pdf.body_text(
        'Alpha and Beta were calculated via linear regression (scipy.stats.linregress) of '
        'each fund\'s daily returns against the NIFTY 100 benchmark. Beta measures market '
        'sensitivity (Beta > 1 = more volatile than the market), while Alpha measures excess '
        'return generated by the fund manager\'s skill independent of market movements. '
        'Positive Alpha indicates genuine outperformance.'
    )
    pdf.section_title('5.5 Maximum Drawdown')
    pdf.body_text(
        'Maximum Drawdown measures the largest peak-to-trough decline in NAV during the '
        'observation period. This metric is critical for understanding worst-case scenarios '
        'for lump-sum investors. Funds with drawdowns exceeding 25% were flagged for heightened volatility risk.'
    )

    # ====== CHAPTER 6: ADVANCED RISK ======
    pdf.add_page()
    pdf.chapter_title('6. Advanced Risk Metrics & Modeling')
    pdf.body_text(
        'Beyond standard performance metrics, advanced risk analytics were integrated into the '
        'Day 6 pipeline to protect theoretical investor capital and identify hidden portfolio risks.'
    )
    pdf.section_title('6.1 Value at Risk (VaR) & Conditional VaR')
    pdf.body_text(
        'Historical VaR at the 95% confidence level was calculated as the 5th percentile of '
        'the daily return distribution. This identifies the maximum expected single-day loss '
        'under normal market conditions. For example, a VaR of -2.1% means there is only a 5% '
        'chance that the fund will lose more than 2.1% in a single trading day.'
    )
    pdf.body_text(
        'Conditional VaR (CVaR), also known as Expected Shortfall, was calculated as the mean '
        'of all returns falling below the VaR threshold. This measures the average severity of '
        'tail-risk events - answering the question: "When things go wrong, how bad do they get?"'
    )
    pdf.section_title('6.2 Rolling 90-Day Sharpe Ratio')
    pdf.body_text(
        'A rolling 90-day Sharpe Ratio was computed for 5 representative funds to visualize '
        'how risk-adjusted performance evolved over time. This analysis revealed periods of '
        'significant Sharpe compression during market corrections (e.g., mid-2022 global rate '
        'hike cycle) followed by recovery during bull market phases.'
    )
    pdf.section_title('6.3 Sector Concentration (HHI)')
    pdf.body_text(
        'The Herfindahl-Hirschman Index (HHI) was calculated across portfolio holdings using '
        'the formula: HHI = sum(weight_i^2). An HHI above 0.25 indicates a highly concentrated '
        'portfolio with excessive exposure to a single sector. Funds with elevated HHI scores '
        'were flagged for diversification risk in the final scorecard.'
    )
    pdf.section_title('6.4 Investor Cohort Analysis')
    pdf.body_text(
        'Investors were segmented into cohorts based on their first transaction year (2022, 2023, '
        '2024, 2025). Analysis revealed that newer cohorts (2024-2025) tend to invest smaller '
        'average SIP amounts but show higher frequency, while legacy cohorts (2022) have larger '
        'ticket sizes but higher attrition rates.'
    )
    pdf.section_title('6.5 SIP Continuity Analysis')
    pdf.body_text(
        'For investors with 6 or more SIP transactions, the average gap between consecutive '
        'transactions was computed. Investors with gaps exceeding 35 days were flagged as '
        '"at-risk" for SIP discontinuity. This early warning system can power automated '
        'retention campaigns to prevent churn.'
    )

    # ====== CHAPTER 7: DASHBOARD ======
    pdf.add_page()
    pdf.chapter_title('7. Dashboard Implementation')
    pdf.body_text(
        'A highly interactive, 4-page Business Intelligence dashboard was developed using '
        'Power BI to democratize these insights for non-technical stakeholders. Each page '
        'features slicers, tooltips, and drill-through capabilities for self-service exploration.'
    )

    pdf.section_title('Page 1: Industry Overview')
    pdf.body_text(
        'High-level KPI cards displaying Total AUM, SIP Inflows, Total Folios, and Number of '
        'Schemes. A historical line chart tracks Industry AUM growth from 2022-2025, while a '
        'clustered bar chart ranks the Top 10 Fund Houses by Assets Under Management.'
    )
    page1_img = os.path.join(SCREENSHOT_DIR, 'page1.png')
    pdf.add_screenshot(page1_img, 'Figure 1: Industry Overview Dashboard Page')

    pdf.section_title('Page 2: Fund Performance')
    pdf.body_text(
        'Features a dynamic scatter plot mapping Return (X-axis) vs Risk (Y-axis) for all 40 '
        'funds, a sortable scorecard table with drill-through to individual NAV charts, and '
        'slicers for Fund House, Category, and Plan type.'
    )
    page2_img = os.path.join(SCREENSHOT_DIR, 'page2.png')
    pdf.add_screenshot(page2_img, 'Figure 2: Fund Performance Dashboard Page')

    pdf.add_page()
    pdf.section_title('Page 3: Investor Analytics')
    pdf.body_text(
        'Geospatial and demographic visualizations including transaction volume by state, '
        'a donut chart splitting SIP vs Lumpsum vs Redemption, age group analysis of average '
        'SIP ticket sizes, and monthly transaction volume trends.'
    )
    page3_img = os.path.join(SCREENSHOT_DIR, 'page3.png')
    pdf.add_screenshot(page3_img, 'Figure 3: Investor Analytics Dashboard Page')

    pdf.section_title('Page 4: SIP & Market Trends')
    pdf.body_text(
        'A dual-axis chart correlating monthly SIP inflows (bars) against NIFTY 50 closing '
        'values (line) from 2022-2025. A matrix heatmap visualizes category-level inflows by '
        'month, and a bar chart highlights the Top 5 categories by net inflow for FY25.'
    )
    page4_img = os.path.join(SCREENSHOT_DIR, 'page4.png')
    pdf.add_screenshot(page4_img, 'Figure 4: SIP & Market Trends Dashboard Page')

    # ====== CHAPTER 8: RECOMMENDER ======
    pdf.add_page()
    pdf.chapter_title('8. Fund Recommendation Engine')
    pdf.body_text(
        'A programmatic fund recommendation engine (recommender.py) was deployed to simulate '
        'Robo-Advisory capabilities. The engine operates in three steps:'
    )
    pdf.bold_bullet('Input: ', 'Accepts an investor\'s self-reported Risk Appetite (Low, Moderate, or High).')
    pdf.bold_bullet('Filter: ', 'Cross-references the SEBI risk_category field in the Fund Master '
                     'to identify eligible funds matching the investor\'s tolerance band.')
    pdf.bold_bullet('Rank: ', 'Sorts the eligible universe by calculated Sharpe Ratio (highest first) '
                     'and outputs the Top 3 optimal funds.')

    pdf.section_title('Sample Recommendations')
    pdf.body_text('LOW Risk Profile:')
    pdf.bullet('1. ICICI Pru Liquid Fund (Sharpe: 0.50)')
    pdf.bullet('2. Kotak Liquid Fund (Sharpe: -0.09)')
    pdf.bullet('3. SBI Magnum Gilt Fund (Sharpe: -0.23)')
    pdf.ln(2)
    pdf.body_text('MODERATE Risk Profile:')
    pdf.bullet('1. Mirae Asset Large Cap Fund (Sharpe: 1.45)')
    pdf.bullet('2. Kotak Flexicap Fund (Sharpe: 1.31)')
    pdf.bullet('3. SBI Bluechip Fund (Sharpe: 1.21)')
    pdf.ln(2)
    pdf.body_text('HIGH Risk Profile:')
    pdf.bullet('1. Mirae Asset Tax Saver Fund - ELSS (Sharpe: 1.23)')
    pdf.bullet('2. ICICI Pru Midcap Fund (Sharpe: 1.18)')
    pdf.bullet('3. DSP Midcap Fund (Sharpe: 1.13)')

    # ====== CHAPTER 9: RECOMMENDATIONS ======
    pdf.add_page()
    pdf.chapter_title('9. Strategic Recommendations')
    pdf.body_text(
        'Based on the synthesized data and analytics performed across all 7 days of the capstone, '
        'the following strategic actions are recommended for Bluestock Fintech:'
    )
    pdf.bold_bullet('1. Targeted SIP Marketing: ',
                     'Given the high retention rate of SIPs in the 26-35 demographic, marketing '
                     'spend should be aggressively allocated to digital channels targeting '
                     'millennials in Tier-2 cities, where growth rates are highest.')
    pdf.bold_bullet('2. Highlight Risk-Adjusted Performers: ',
                     'Retail investors often chase trailing 1-year returns. Bluestock\'s platform '
                     'should default to sorting funds by Sharpe and Sortino ratios to protect '
                     'clients from high-Beta traps during market corrections.')
    pdf.bold_bullet('3. Proactive Churn Prevention: ',
                     'Utilize the SIP Continuity analysis logic to trigger automated email/SMS '
                     'reminders to "at-risk" investors who have missed an expected SIP installment '
                     'by more than 30 days.')
    pdf.bold_bullet('4. Diversification Alerts: ',
                     'Integrate the HHI sector concentration scores into fund detail pages. '
                     'Funds with HHI > 0.25 should display a visible "Concentrated Portfolio" '
                     'warning badge to help investors make informed decisions.')
    pdf.bold_bullet('5. Expand Data Sources: ',
                     'Integrate real-time NAV feeds from the AMFI API and NSE/BSE market data '
                     'to enable intraday analytics and live dashboard refreshes.')

    # ====== CHAPTER 10: LIMITATIONS ======
    pdf.add_page()
    pdf.chapter_title('10. Limitations & Future Scope')
    pdf.section_title('10.1 Current Limitations')
    pdf.bold_bullet('Static Data: ',
                     'The current architecture relies on batch CSV ingestion. Data freshness '
                     'is limited to the last manual download cycle.')
    pdf.bold_bullet('Sample Size: ',
                     'The analysis covers 40 representative mutual fund schemes out of 1,900+ '
                     'in the Indian market. Results may not generalize to niche or sectoral funds.')
    pdf.bold_bullet('Rule-Based Recommender: ',
                     'The current recommendation engine is purely rule-based (historical Sharpe). '
                     'It does not account for changing market regimes or macroeconomic conditions.')
    pdf.bold_bullet('Single Benchmark: ',
                     'Alpha and Beta were calculated against NIFTY 100 only. Multi-benchmark '
                     'regression would provide more nuanced risk attribution.')

    pdf.section_title('10.2 Future Scope')
    pdf.bold_bullet('Real-Time Pipelines: ',
                     'Implement Apache Airflow or Prefect-orchestrated DAGs to stream daily '
                     'NAV updates directly from the AMFI API into the SQLite/PostgreSQL database.')
    pdf.bold_bullet('Machine Learning: ',
                     'Train supervised ML models (Random Forest, XGBoost) to predict future '
                     'quartile rankings based on macroeconomic indicators, fund flows, and '
                     'momentum features.')
    pdf.bold_bullet('Cloud Deployment: ',
                     'Migrate the SQLite database to a cloud-hosted PostgreSQL instance and '
                     'deploy the Streamlit dashboard on platforms like Streamlit Cloud or AWS.')
    pdf.bold_bullet('NLP Sentiment: ',
                     'Integrate NLP-based sentiment analysis on financial news headlines to '
                     'create a Market Mood Index as an additional input to the recommender engine.')

    # ====== FINAL PAGE ======
    pdf.add_page()
    pdf.ln(60)
    pdf.set_font('Helvetica', 'B', 20)
    pdf.set_text_color(0, 51, 102)
    pdf.cell(0, 12, 'Thank You', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(8)
    pdf.set_font('Helvetica', '', 12)
    pdf.set_text_color(80, 80, 80)
    pdf.cell(0, 8, 'Bluestock Mutual Fund Analytics Capstone', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 8, 'Damodara P | Data Analyst Intern | June 2026', align='C', new_x="LMARGIN", new_y="NEXT")
    pdf.ln(20)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 8, 'For queries, please contact: pdamodaran2000@gmail.com', align='C', new_x="LMARGIN", new_y="NEXT")

    # Save
    pdf.output(OUTPUT_PATH)
    print(f"Final Report generated successfully: {OUTPUT_PATH}")
    print(f"Total pages: {pdf.page_no()}")


if __name__ == '__main__':
    build_report()
