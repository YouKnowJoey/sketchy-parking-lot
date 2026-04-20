'''
Project Name: Sketchy Parking Lot
Authors: Joey Garcia and Reilly Rodriguez Spencer

Purpose: This file contains the SketchyTokenizer class, which is responsible for preprocessing and tokenizing the input text for the Sketchy Parking Lot project. The tokenizer will convert the input text into a format that can be used by the features enginneering and unsupervised machine learning models.
'''

import os
import re
import json
import pandas as pd
import nltk
from nltk.corpus import stopwords

class SketchyTokenizer:
    def __init__(self, data_location="../data/parked_suspicious/"):
        self.data_location = data_location
        self.text = None
        self.combined_df = None

        # regex patterns for cleaning text
        self.url_re = re.compile(r"https?://\S+|www\.\S+", flags=re.I)
        self.domain_re = re.compile(r"\b(?:[a-z0-9-]+\.)+[a-z]{2,}\b", flags=re.I)
        self.number_re = re.compile(r"\b\d+(?:\.\d+)?\b")
        self.non_letter_re = re.compile(r"[^a-z\s]")
        self.whitespace_re = re.compile(r"\s+")

        nltk.download("stopwords")
        self.stop_words = set(stopwords.words("english"))

    # -------------------------
    # DATA LOADING
    # -------------------------
    def load_all_jsonl(self):
        """Recursively load all JSONL files based on summary file"""
        # check if data_location is set
        if self.data_location is None:
            raise ValueError("data_location must be set")

        # load summary
        summary_path = os.path.join(self.data_location, "_summary.json")
        if not os.path.exists(summary_path):
            raise FileNotFoundError(f"Missing summary file: {summary_path}")

        with open(summary_path, "r") as f:
            summary = json.load(f)

        dfs = []
        # Iterate over summary labels to combine all JSONL files
        for label in summary.keys():
            clean_label = label.replace(":", "-")
            filename = os.path.join(self.data_location, f"{clean_label}.jsonl")

            if not os.path.exists(filename):
                print(f"Missing: {filename}")
                continue

            try:
                df = pd.read_json(filename, lines=True)
                dfs.append(df)
                print(f"Loaded {filename} ({len(df)} rows)")
            except ValueError as e:
                print(f"Error reading {filename}: {e}")

        if not dfs:
            raise ValueError("No JSONL files were loaded")

        self.combined_df = pd.concat(dfs, ignore_index=True)

        print("\nTotal rows:", len(self.combined_df))
        print("\nServices:\n", self.combined_df["service"].value_counts())

        return self.combined_df

    # -------------------------
    # TEXT CLEANING AND PREPROCESSING
    # -------------------------
    def clean_text(self, text):
        text = str(text).lower()
        text = self.url_re.sub(" ", text)
        text = self.domain_re.sub(" ", text)
        text = self.number_re.sub(" ", text)
        text = self.non_letter_re.sub(" ", text)
        text = self.whitespace_re.sub(" ", text).strip()

        tokens = [
            t for t in text.split()
            if t not in self.stop_words and len(t) > 1
        ]

        return " ".join(tokens)

    # -------------------------
    # TOKENIZATION
    # -------------------------
    def tokenize_text(self, text):
        cleaned = self.clean_text(text)
        return cleaned.split()

    def get_bigrams(self, tokens):
        return list(zip(tokens, tokens[1:]))
    
    def get_trigrams(self, tokens):
        return list(zip(tokens, tokens[1:], tokens[2:]))

    # -------------------------
    # APPLY TO DATAFRAME
    # -------------------------
    def build_text_features(self):
        if self.combined_df is None:
            raise ValueError("Run load_all_jsonl() first")

        text_cols = [c for c in ["title", "textSnippet"] if c in self.combined_df.columns]

        # Combine raw text
        self.combined_df["raw_text"] = (
            self.combined_df[text_cols]
            .fillna("")
            .agg(" ".join, axis=1)
            .str.strip()
        )

        # Clean text
        self.combined_df["clean_text"] = self.combined_df["raw_text"].apply(self.clean_text)

        # Tokenize
        self.combined_df["tokens"] = self.combined_df["clean_text"].apply(lambda x: x.split())

        # Generate bigrams and trigrams
        self.combined_df["bigrams"] = self.combined_df["tokens"].apply(self.get_bigrams)
        self.combined_df["trigrams"] = self.combined_df["tokens"].apply(self.get_trigrams)

        return self.combined_df
