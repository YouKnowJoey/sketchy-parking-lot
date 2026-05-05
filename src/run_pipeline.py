from pathlib import Path
import pandas as pd
from sketchy_tokenizer import SketchyTokenizer

def tokenizer_pipeline(data_dir: Path, outputs_dir: Path):
    print("Running tokenizer pipeline...")

    tokenizer = SketchyTokenizer(data_location=str(data_dir))

    try:
        df = tokenizer.load_all_jsonl()
        df = tokenizer.build_text_features()

        print("\nPipeline complete")
        print(f"Total rows:  {len(df)}")
        print(df[["raw_text", "clean_text", "tokens", "bigrams", "trigrams"]].head(3))

        # Save processed output
        output_file = outputs_dir / "processed_data.parquet"
        df.to_parquet(output_file, index=False)
        print(f"Saved dataset to: {output_file}")

    except Exception as e:
        print(f"Pipeline failed: {e}")

    return df


def main():
    print("Container is running...")

    data_dir = Path("/app/data")
    outputs_dir = Path("/app/outputs")

    # Ensure output directory exists
    outputs_dir.mkdir(parents=True, exist_ok=True)

    print(f"Data dir exists: {data_dir.exists()}")
    print(f"Outputs dir exists: {outputs_dir.exists()}")

    # Run pipeline
    df = tokenizer_pipeline(data_dir, outputs_dir)

    # Docker dataframe output
    output_file = outputs_dir / "results.csv"
    df.to_csv(output_file, index=False)

    print(f"Wrote file: {output_file}")


if __name__ == "__main__":
    main()
