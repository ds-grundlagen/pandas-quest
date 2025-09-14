import argparse
from pathlib import Path
import pickle
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    args = parser.parse_args()
    
    print("🔭 Checking your solution...")
    
    if not Path(args.file).exists():
        print(f"⚠️ The file does not exist: {args.file}")
        return

    try:
        df = pd.read_csv(args.file)
    except Exception as e:
        print(f"⚠️ Error reading the file: {e}")
        return

    # Check 1: there are only 3 columns named "HIP", "d_ly", and "sp_class"
    assert len(df.columns) == 3, "⚠️ There are not exactly 3 columns, did you forget to exclude the index column?"
    assert df.columns.tolist() == ["HIP", "d_ly", "sp_class"], "⚠️ Columns are not the three columns we expect. Did you forget to exclude the index column?"
    
    print("✅ [1/6] Columns included look ok")
    
    # Check 2: There are exactly 113278 rows
    assert len(df) == 113278, "⚠️ There are not the correct number of rows, did you save the filtered dataset?"
    print("✅ [2/6] Number of rows look ok")
    
    # Check 3: The "HIP" column is unique
    assert df["HIP"].is_unique, "⚠️ The \"HIP\" column is not unique, did you duplicate any rows somewhere?"
    print("✅ [3/6] \"HIP\" column is unique")
    
    # Check 4: d_ly has a mean between 1100 and 1200
    assert df["d_ly"].mean() >= 1100 and df["d_ly"].mean() <= 1200, "⚠️ The mean of the \"d_ly\" column looks off, did you compute the distance correctly?"
    print("✅ [4/6] \"d_ly\" column has a mean between 1100 and 1200")
    
    # Check 5: sp_class has a value count of 8
    assert df["sp_class"].value_counts().shape[0] == 8, "⚠️ The number of unique values in the \"sp_class\" column is not 8, did you forget to include the \"Other\" class?"
    print("✅ [5/6] \"sp_class\" column has a value count of 8")
    
    # Check_6: sp_class has the right counts
    # find out if other is capitalized or lowercase (both are ok but we need to know)
    unqiue_classes = df["sp_class"].unique()
    
    if "other" in unqiue_classes:
        other_word = "other"
    elif "Other" in unqiue_classes:
        other_word = "Other"
    else:
        print(f"⚠️ The \"sp_class\" column contains does not contain an \"Other\" class, did you forget to include it?")
        return
    
    counts = df["sp_class"].value_counts()
    assert counts["A"] == 18191, "⚠️ The number of stars in each spectral class is not correct"
    assert counts["B"] == 9469, "⚠️ The number of stars in each spectral class is not correct"
    assert counts[other_word] == 2921, "⚠️ The number of stars in each spectral class is not correct"
    print("✅ [6/6] \"sp_class\" column has the right counts")
    
    o_counts = counts["O"]
    shift = int(o_counts/4 + 12.75)
    
    with open("data/secret-word.pkl", "rb") as f:
        we = pickle.load(f)

    wd = "".join([chr(ord(c) - shift) for c in we])

    print("\n\n✨💫🔭 Congrats 🔭💫✨\n")
    print(wd)
    

if __name__ == "__main__":
    main()
