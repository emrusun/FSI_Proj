
import os
import pandas as pd
import matplotlib.pyplot as plt
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter

# Define the base directory where the 10-K filings are stored
base_dir = 'sec_files'
tickers = ['BK', 'LAZ', 'JPM']

# Initialize DistilBERT tokenizer and model
tokenizer = DistilBertTokenizer.from_pretrained('distilbert-base-uncased')
model = DistilBertForSequenceClassification.from_pretrained('distilbert-base-uncased', num_labels=10)

# Define risk factor groups
risk_factor_groups = {
    "Financial": ["debt", 'interest', 'currency'],
    "Strategic": ['competition', 'competitor', 'partnerships', 'merger', 'acquisition'],
    "Daily Operations": ['production', 'manufacturing', 'supply chain'],
    "Reputation": ['brand reputation', 'perception', 'social media', 'retention'],
    "Safety": ['breach', 'privacy', 'attack', 'security'],
}

# Initialize DataFrame to store risk factor data
risk_factors_dataframe = pd.DataFrame(columns=["Company", "Year", "Risk Factor", "Frequency"])

# Iterate over tickers 
risk_factors_dataframe["Year"] = pd.to_numeric(risk_factors_dataframe["Year"])
for ticker in tickers:
    company_dir = os.path.join(base_dir, ticker, '10-K')
    if not os.path.exists(company_dir):
        continue
    for filing in os.listdir(company_dir):
        filing_dir = os.path.join(company_dir, filing)
        if not os.path.isdir(filing_dir):
            continue
        for filename in os.listdir(filing_dir):
            if filename.endswith('full-submission.txt'):
                with open(os.path.join(filing_dir, filename), 'r', encoding='utf-8') as f:
                    filing_text = f.read()
                # print("Filing Text:", filing_text)

                # Extract risk factors
                risk_factors_stuff = ''
                start_extraction = False
                for line in filing_text.split('\n'):
                    if 'Item 1A.' in line:
                        start_extraction = True
                        print("start extract")
                        continue
                    if start_extraction:
                        if line.strip() == '':
                            break
                        risk_factors_stuff += line + ' '
                # for line in filing_text.split('\n')[filing_text.split('\n').index(line):]:
                #     if line.strip() == '':
                #         break
                #     risk_factors_stuff += line + ''
                # print("Risk Factors Extracted:", risk_factors_stuff)  # Check if risk factors

                # Tokenize, lemmatize, count
                tokens = word_tokenize(risk_factors_stuff.lower())
                stop_words = set(stopwords.words('english'))
                lemmatizer = WordNetLemmatizer()
                tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
                risk_factor_freq = Counter(tokens)

                #Data to drame
                risk_factors_dataframe = pd.concat([risk_factors_dataframe, pd.DataFrame({
                    "Company": [ticker]*len(risk_factor_freq),
                    "Year": [filing.split('-')[1]]*len(risk_factor_freq),  # Extract year from filing name
                    "Risk Factor": list(risk_factor_freq.keys()),
                    "Frequency": list(risk_factor_freq.values()),
                })])
                # print("Risk factors DataFrame:", risk_factors_dataframe)  

# Group them
risk_factors_dataframe["Risk Group"] = risk_factors_dataframe["Risk Factor"].apply(
    lambda x: next((group for group, activations in risk_factor_groups.items() if any(activation in x.lower() for activation in activations)), "Other")
)
# print("DataFrame after assigning risk factor groups:", risk_factors_dataframe)

# Check if DataFrame is empty
if risk_factors_dataframe.empty:
    print("DataFrame 'risk_factors_dataframe' is empty. No data to plot.")
else:
    # Plot
    for ticker in tickers:
        plt.figure(figsize=(15, 8))
        filtered_data = risk_factors_dataframe[(risk_factors_dataframe["Company"] == ticker) & (risk_factors_dataframe["Risk Group"] != "Other")]
    for category, groups in filtered_data.groupby("Risk Group"):
        plt.plot(groups["Year"], groups["Frequency"], label=category)
    plt.xlabel("Year")
    plt.ylabel("Frequency")
    plt.title(f"Historical Risk Factor Trends for {ticker}")
    plt.legend()
    plt.show()

