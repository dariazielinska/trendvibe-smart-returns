import pandas as pd
from src.data.data_loader import load_data
from src.pipeline import process


def main():
    df = load_data()
    df = df.head(10)

    auto_results, manual_results = process(df)
    auto_df = pd.DataFrame(auto_results)
    manual_df = pd.DataFrame(manual_results)

    auto_df.to_csv("outputs/raport_automatyczny.csv", index=False)
    manual_df.to_csv("outputs/do_weryfikacji_recznej.csv", index=False)

    print("Saved:")
    print("- outputs/raport_automatyczny.csv")
    print("- outputs/do_weryfikacji_recznej.csv")


if __name__ == "__main__":
    main()