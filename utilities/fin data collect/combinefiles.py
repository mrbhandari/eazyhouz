import glob

read_files = glob.glob("*.csv")


with open("result.csv", "wb") as outfile:
    for f in read_files:
        with open(f, "rb") as infile:
            outfile.write(infile.read())
            