import pandas as pd
import os

def recommend_funds(risk_appetite, top_n=3):
    """
    Recommends top mutual funds based on the investor's risk appetite.
    Uses the fund_master (for risk grade) and fund_scorecard (for sharpe ratio ranking).
    """
    print(f"\\n--- Fund Recommendations for {risk_appetite.upper()} Risk Profile ---")
    
    # Fix paths to be relative to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    master_path = os.path.join(script_dir, '..', 'data', 'raw', '01_fund_master.csv')
    score_path = os.path.join(script_dir, '..', 'data', 'processed', 'fund_scorecard.csv')
    
    if not os.path.exists(master_path) or not os.path.exists(score_path):
        print("Required datasets not found. Please ensure Day 1 and Day 4 ETL/Analytics are complete.")
        return
        
    df_master = pd.read_csv(master_path)
    df_score = pd.read_csv(score_path)
    
    # Merge datasets on AMFI code
    # Assuming fund_scorecard has 'amfi_code' and 'sharpe_ratio'
    # Fallback column names just in case the generated scorecard used different index
    if 'amfi_code' not in df_score.columns:
        df_score = df_score.reset_index().rename(columns={'index': 'amfi_code'})
        
    df_merged = pd.merge(df_master, df_score, on='amfi_code', how='inner')
    
    # Map input risk to SEBI risk categories roughly
    if risk_appetite.lower() == 'low':
        target_risks = ['Low', 'Low to Moderate']
    elif risk_appetite.lower() == 'moderate':
        target_risks = ['Moderate', 'Moderately High']
    elif risk_appetite.lower() == 'high':
        target_risks = ['High', 'Very High']
    else:
        print("Invalid risk appetite. Choose: Low, Moderate, High.")
        return
        
    # Filter by risk
    recommended = df_merged[df_merged['risk_category'].isin(target_risks)]
    
    # Sort by Sharpe Ratio (Highest is best)
    if 'sharpe_ratio' in recommended.columns:
        recommended = recommended.sort_values(by='sharpe_ratio', ascending=False)
        
    if recommended.empty:
        print(f"No funds found matching risk profile: {risk_appetite}")
        return
        
    top_funds = recommended.head(top_n)
    
    for i, row in top_funds.iterrows():
        print(f"{i+1}. {row.get('scheme_name', 'Unknown Fund')} (AMFI: {row['amfi_code']})")
        print(f"   Category: {row.get('sub_category', 'Unknown')}")
        print(f"   Sharpe Ratio: {row.get('sharpe_ratio', 0):.2f}\\n")

if __name__ == "__main__":
    # Test cases
    recommend_funds('low')
    recommend_funds('moderate')
    recommend_funds('high')
