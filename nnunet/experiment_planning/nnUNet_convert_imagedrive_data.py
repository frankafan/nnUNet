from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.utilities.file_endings import remove_trailing_slash
from nnunet.paths import nnUNet_raw_data


def crawl_and_format_data_directory(folder, taskId, taskName):
    folder = remove_trailing_slash(folder)

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.nii.gz'):
                taskFolderName = 'Task' + "{0:03}".format(taskId) + '_' + taskName
                if '_PT' in file:
                    os.replace(os.path.join(root, file), os.path.join(os.path.join(nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTr')), file.replace('_PT', '').replace('.nii.gz', '_0000.nii.gz')))
                elif '_RTSTRUCT' in file:
                    os.replace(os.path.join(root, file), os.path.join(os.path.join(nnUNet_raw_data, os.path.join(taskFolderName, 'labelsTr')), file.replace('_PT', '')))
            

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Convert imagedrive data and format them to be used in nnU-Net")
    parser.add_argument("-i", help="Input folder", required=True)
    parser.add_argument("-t", help="Task ID", default=500, type=int, required=False)
    parser.add_argument("-n", help="Task name", default="TaskName", required=False)
    args = parser.parse_args()

    crawl_and_format_data_directory(args.i, args.t, args.n)


if __name__ == "__main__":
    main()
