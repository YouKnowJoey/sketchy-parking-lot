from pathlib import Path
import pandas as pd
from sketchy_tokenizer import SketchyTokenizer
from sketchy_features import SketchyFeatures
from sketchy_unsupervised_models import UnsupervisedSketchyModels

def tokenizer_pipeline(data_dir: Path) -> pd.DataFrame:
    print("Running tokenizer pipeline...")

    tokenizer = SketchyTokenizer(data_location=str(data_dir))

    try:
        sketchy_df = tokenizer.load_all_jsonl()
        sketchy_df = tokenizer.build_text_features()

        print("\nPipeline complete")
        print(f"Total rows:  {len(sketchy_df)}")
        print(sketchy_df[["raw_text", "clean_text", "tokens", "bigrams", "trigrams"]].head(3))

    except Exception as e:
        print(f"Pipeline failed: {e}")

    return sketchy_df

def feature_engineering_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("Running feature engineering pipeline...")

    # feature engineering
    sketchy_features = SketchyFeatures(df)
    sketchy_df = sketchy_features.extract_features()

    print("\nFeature engineering complete")
    print(sketchy_df[["ad_score", "parked_score", "suspicious_score", \
              "lang", "avg_redirect_jaccard", "min_redirect_jaccard"]].head(3))

    return sketchy_df

def unsupervised_model_pipeline(df: pd.DataFrame) -> pd.DataFrame:
    print("Running unsupervised model pipeline...")

    unsupervised_models = UnsupervisedSketchyModels(df)
    sketchy_df = unsupervised_models.sketchy_fitting(n_clusters=3, n_estimators=100, contamination=0.01)
    
    print("\nUnsupervised modeling complete")
    print(sketchy_df[["kmeans_cluster", "iforest_score", "iforest_score_normalized"]].head(3))

    return sketchy_df

def main():
    print("Container is running...")

    data_dir = Path("/app/data/parked_suspicious")
    outputs_dir = Path("/app/outputs")

    # Ensure output directory exists
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Data dir exists: {data_dir.exists()}")
    print(f"Outputs dir exists: {outputs_dir.exists()}")

    # Run pipeline
    df = tokenizer_pipeline(data_dir)
    df = feature_engineering_pipeline(df)
    df = unsupervised_model_pipeline(df)

    # Docker dataframe output
    output_file = outputs_dir / "results.csv"
    df.to_csv(output_file, index=False)

    print(f"Wrote file: {output_file}")


if __name__ == "__main__":
    main()
