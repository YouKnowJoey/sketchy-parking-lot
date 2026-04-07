from pathlib import Path

def main():
    print("Container is running.")

    data_dir = Path("/app/data")
    outputs_dir = Path("/app/outputs")

    print(f"Data dir exists: {data_dir.exists()}")
    print(f"Outputs dir exists: {outputs_dir.exists()}")

    test_file = outputs_dir / "test.txt"
    test_file.write_text("Docker is writing to outputs\n")

    print(f"Wrote file: {test_file}")

if __name__ == "__main__":
    main()