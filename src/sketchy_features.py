'''
Project Name: Sketchy Parking Lot
Authors: Joey Garcia and Reilly Rodriguez Spencer

Purpose: This file is strictly meant for feature engineering and data manipulation. The goal is to transform raw data into feature extraction. 
'''

import numpy as np
import pandas as pd
from collections import Counter # Text analysis
import tldextract # Domain parsing
import sketchy_lang_id # FastText Language identification

class SketchyFeatures:
    def __init__(self, df: pd.DataFrame):
        self.df = df
        self.all_ngrams = set()
        self.lang_id = sketchy_lang_id.SketchyLangID()

        # Initial defined keywords 
        self.ad_keywords = {
            "ad", "ads", "advertisement", "sponsored", "promotion",
            "click", "offer", "sale", "buy", "discount"
        }
        self.parked_keywords = {
            "domain for sale", "buy this domain", "this domain is for sale",
            "parked", "coming soon", "under construction", "related links", "related searches", 
            "search results", "powered by", "ads by", "privacy policy", "this webpage was generated",
            "domain parked free", "listing expired"
        }
        self.suspicious_keywords = {
            "virus", "malware", "warning", "security alert", "download now", "install", 
            "verify", "urgent", "your computer", "system alert", "scan now", "risk detected",
            "click here to continue", "enable notifications"
        }

    # -------------------------
    # COMBINE FEATURE ENGINEERING METHODS
    # -------------------------
    def extract_features(self):
        """
        Build n-gram vocabulary, expand keyword sets,
        then score each row. Extract domain parts, language identification, and analyze redirect chains.
        """

        # Step 1: Build n-grams automatically
        if len(self.all_ngrams) == 0:
            self.build_ngram_vocabulary()

        # Step 2: Expand keyword sets
        self.ad_keywords = self.expand_keywords(
            self.ad_keywords, self.all_ngrams
        )
        self.parked_keywords = self.expand_keywords(
            self.parked_keywords, self.all_ngrams
        )
        self.suspicious_keywords = self.expand_keywords(
            self.suspicious_keywords, self.all_ngrams
        )

        # Step 3: Score rows
        self.df["ad_score"] = self.df["tokens"].apply(
            lambda x: self.keyword_score(x, self.ad_keywords)
        )
        self.df["parked_score"] = self.df["tokens"].apply(
            lambda x: self.keyword_score(x, self.parked_keywords)
        )
        self.df["suspicious_score"] = self.df["tokens"].apply(
            lambda x: self.keyword_score(x, self.suspicious_keywords)
        )

        # Step 4: Extract domain parts
        # change domain to domain_full to preserve original domain for tldextract
        self.df["domain_full"] = self.df["domain"]
        self.df.drop("domain", axis=1, inplace=True)

        self.df[["subdomain", "domain_name", "tld"]] = self.df["domain_full"].apply(self.extract_domain_parts)

        # Step 5: Language identification and TLD mismatch analysis
        self.df[["lang", "lang_confidence"]] = self.df["raw_text"].apply(
            lambda x: pd.Series(self.lang_id.detect_language(x))
        )
        self.tld_lang_map()
        self.lang_tld_mismatch()

        # Step 6: Analyze redirect chains
        redirect_features = self.df["redirectChain"].apply(self.analyze_redirect_chain)
        redirect_df = pd.DataFrame(list(redirect_features))
        self.df = pd.concat([self.df, redirect_df], axis=1)

        return self.df

    # -------------------------
    # KEYWORD EXPANSION AND SCORING
    # -------------------------
    def expand_keywords(self, seed_keywords, ngrams):
        # Expand keyword sets using pattern matching
        expanded = set(seed_keywords)
        
        for phrase in ngrams:
            for keyword in seed_keywords:
                if keyword in phrase:
                    expanded.add(phrase)
        
        return expanded

    def build_ngram_vocabulary(self, top_n=100):
        """
        Build searchable n-gram vocabulary from dataframe columns:
        - bigrams
        - trigrams

        Stores result in self.all_ngrams
        """

        total_bigrams = Counter()
        total_trigrams = Counter()

        # Aggregate bigrams
        if "bigrams" in self.df.columns:
            for bigram_list in self.df["bigrams"]:
                if isinstance(bigram_list, list):
                    total_bigrams.update(bigram_list)

        # Aggregate trigrams
        if "trigrams" in self.df.columns:
            for trigram_list in self.df["trigrams"]:
                if isinstance(trigram_list, list):
                    total_trigrams.update(trigram_list)

        # Convert tuples into searchable strings
        bigram_list = [
            " ".join(bg) if isinstance(bg, tuple) else str(bg)
            for bg, _ in total_bigrams.most_common(top_n)
        ]

        trigram_list = [
            " ".join(tg) if isinstance(tg, tuple) else str(tg)
            for tg, _ in total_trigrams.most_common(top_n)
        ]

        self.all_ngrams = set(bigram_list + trigram_list)

        return self.all_ngrams
    
    def keyword_score(self, tokens, keyword_set):
        '''
        Score a list of tokens based on their presence in a keyword set.
        '''
        text = " ".join(tokens)
        return sum(1 for kw in keyword_set if kw in text)

    # -------------------------
    # LANGUAGE IDENTIFICATION AND TLD MISMATCH ANALYSIS 
    # -------------------------

    def tld_lang_map(self):
        tld_lang_map = (
            self.df.groupby("tld")["language"]
            .agg(lambda x: x.value_counts().index[0])
            .to_dict()
        )

        self.df["tld_expected_lang"] = self.df["tld"].map(tld_lang_map)

    def lang_tld_mismatch(self):
        self.df["lang_tld_mismatch"] = (
            self.df["language"] != self.df["tld_expected_lang"]
        ).astype(int)

        self.df["lang_tld_mismatch_strong"] = (
            (self.df["lang_tld_mismatch"] == 1) &
            (self.df["lang_confidence"] > 0.6)
        ).astype(int)

    # -------------------------
    # ANALYZE REDIRECT CHAINS
    # -------------------------
    def jaccard_similarity(self, a, b):
        '''
        Jaccard similarity to compare token sets of original domain and redirected domains
        
        - 0 is completely different, 1 is identical
        '''
        set_a = set(a)
        set_b = set(b)
        
        if not set_a and not set_b:
            return 1.0
        
        return len(set_a & set_b) / len(set_a | set_b)


    def extract_domain_parts(self, domain):
        '''
        extract TLD, domain and subdomain using tldextract

        Parse the full domain for analysis.

        REMARK: Process is based on the tldextract library, which is a widely used tool for parsing domain names.
        '''
        ext = tldextract.extract(domain)
        return pd.Series({
            "subdomain": ext.subdomain,
            "domain_name": ext.domain,
            "tld": ext.suffix
        })

    def domain_to_tokens(self, parts):
        ''' 
        parts is dict with keys: subdomain, domain_name, tld from extract_domain_parts() function
        '''
        tokens = []
        
        if parts["subdomain"]:
            tokens.extend(parts["subdomain"].split('.'))
        
        if parts["domain_name"]:
            tokens.append(parts["domain_name"])
        
        if parts["tld"]:
            tokens.extend(parts["tld"].split('.'))
        
        return tokens

    def analyze_redirect_chain(self, chain, min_similarity_threshold=0.3):
        if not isinstance(chain, list) or len(chain) == 0:
            return {
                "num_redirects": 0,
                "final_domain": None,
                "avg_redirect_jaccard": 1.0,
                "min_redirect_jaccard": 1.0,
                "low_redirect_similarity_flag": 0
            }
        
        token_sets = []
        
        for step in chain:
            url = step.get("to", "")
            parts = self.extract_domain_parts(url)
            tokens = self.domain_to_tokens(parts)
            if tokens:
                token_sets.append(tokens)
        
        if len(token_sets) < 2:
            return {
                "num_redirects": len(chain),
                "final_domain": None,
                "avg_redirect_jaccard": 1.0,
                "min_redirect_jaccard": 1.0,
                "low_redirect_similarity_flag": 0
            }
        
        similarities = []
        
        for i in range(1, len(token_sets)):
            sim = self.jaccard_similarity(token_sets[i-1], token_sets[i])
            similarities.append(sim)
        
        avg_sim = sum(similarities) / len(similarities)
        min_sim = min(similarities)
        
        # Flag strong domain shift
        low_similarity_flag = int(min_sim < min_similarity_threshold)
        
        final_parts = self.extract_domain_parts(chain[-1].get("to", ""))
        final_domain = f"{final_parts['domain_name']}.{final_parts['tld']}"
        
        return {
            "num_redirects": len(chain),
            "final_domain": final_domain,
            "avg_redirect_jaccard": avg_sim,
            "min_redirect_jaccard": min_sim,
            "low_redirect_similarity_flag": low_similarity_flag
        }


    def original_vs_final_similarity(self, chain):
        '''
        Compare original full_domain to last redirected domain usign jaccard similarity.
        '''
        if not chain:
            return 1.0
        
        first = self.extract_domain_parts(chain[0].get("from", ""))
        last = self.extract_domain_parts(chain[-1].get("to", ""))
        
        tokens_first = self.domain_to_tokens(first)
        tokens_last = self.domain_to_tokens(last)
        
        return self.jaccard_similarity(tokens_first, tokens_last)
