from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.utilities.file_endings import remove_trailing_slash
from nnunet.paths import nnUNet_raw_data


def crawl_and_format_data_directory(folder):
    folder = remove_trailing_slash(folder)

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.nii.gz'):
                if '_PT' in file:
                    os.replace(os.path.join(root, file), os.path.join(os.path.join(nnUNet_raw_data, 'imagesTr'), file.replace('_PT', '').replace('.nii.gz', '_0000.nii.gz')))
                elif '_RTSTRUCT' in file:
                    os.replace(os.path.join(root, file), os.path.join(os.path.join(nnUNet_raw_data, 'labelsTr'), file.replace('_PT', '')))
            

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert imagedrive data and format them to be used in nnU-Net")
    parser.add_argument("-i", help="Input folder", required=True)
    args = parser.parse_args()

    crawl_and_format_data_directory(args.i)


if __name__ == "__main__":
    main()
