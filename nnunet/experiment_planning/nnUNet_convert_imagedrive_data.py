from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.utilities.file_endings import remove_trailing_slash


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert imagedrive data and format them to be used in nnU-Net")
    parser.add_argument("-i", help="Input folder", required=True)
    args = parser.parse_args()


if __name__ == "__main__":
    main()
