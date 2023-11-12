from utils.parser import parse_files

if __name__ == "__main__":
    parse_files(
        base_folder="data/pdf_raw/", dst_folder="data/extracted", skip_on_err=True
    )
