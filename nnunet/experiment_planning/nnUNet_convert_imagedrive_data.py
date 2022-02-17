from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.utilities.file_endings import remove_trailing_slash
from nnunet.paths import nnUNet_raw_data
from nnunet.dataset_conversion.utils import generate_dataset_json


def generate_task_folder_name(taskId, taskName):
    return 'Task' + "{0:03}".format(taskId) + '_' + taskName


def crawl_and_format_data_directory(folder, taskId, taskName):
    folder = remove_trailing_slash(folder)
    taskFolderName = generate_task_folder_name(taskId, taskName)

    if not os.path.exists(os.path.join(
            nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTs'))):
        os.makedirs(os.path.join(
            nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTs')))

    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.endswith('.nii.gz'):
                newFileName = ''
                for i in range(len(file)):
                    if file[i+1] != '_':
                        newFileName.append(file[i])
                if '_PT' in file:
                    fileDir = os.path.join(
                        nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTr'))
                    if not os.path.exists(fileDir):
                        os.makedirs(fileDir)
                    os.replace(os.path.join(root, file), os.path.join(
                        fileDir, newFileName.replace('.nii.gz', '_0000.nii.gz')))
                elif '_RTSTRUCT' in file:
                    fileDir = os.path.join(
                        nnUNet_raw_data, os.path.join(taskFolderName, 'labelsTr'))
                    if not os.path.exists(fileDir):
                        os.makedirs(fileDir)
                    os.replace(os.path.join(root, file), os.path.join(
                        fileDir, newFileName))


def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert imagedrive data and format them to be used in nnU-Net")
    parser.add_argument("-i", help="Input folder", required=True)
    parser.add_argument("-t", help="Task ID", default=500,
                        type=int, required=False)
    parser.add_argument("-n", help="Task name",
                        default="TaskName", required=False)
    args = parser.parse_args()

    crawl_and_format_data_directory(args.i, args.t, args.n)
    taskFolderPath = os.path.join(
        nnUNet_raw_data, generate_task_folder_name(args.t, args.n))
    generate_dataset_json(os.path.join(taskFolderPath, 'dataset.json'), os.path.join(taskFolderPath, 'imagesTr'), os.path.join(taskFolderPath, 'imagesTs'), ('PT'),
                          labels={0: 'background', 1: 'label'}, dataset_name=generate_task_folder_name(args.t, args.n))


if __name__ == "__main__":
    main()
