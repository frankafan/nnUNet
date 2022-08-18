from batchgenerators.utilities.file_and_folder_operations import *
from nnunet.utilities.file_endings import remove_trailing_slash
from nnunet.paths import nnUNet_raw_data
from nnunet.dataset_conversion.utils import generate_dataset_json


def generate_task_folder_name(taskId, taskName):
    return 'Task' + "{0:03}".format(taskId) + '_' + taskName


def crawl_and_format_data_directory(training_folder, testing_folder, taskId, taskName):
    training_folder = remove_trailing_slash(training_folder)
    taskFolderName = generate_task_folder_name(taskId, taskName)

    if not os.path.exists(os.path.join(
            nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTs'))):
        os.makedirs(os.path.join(
            nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTs')))

    for root, dirs, files in os.walk(training_folder):
        for file in files:
            if file.endswith('.nii.gz'):
                newFileName = '_'.join(file.split('_')[:-1])
                if '_PET' in file:
                    fileDir = os.path.join(
                        nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTr'))
                    if not os.path.exists(fileDir):
                        os.makedirs(fileDir)
                    os.replace(os.path.join(root, file), os.path.join(
                        fileDir, newFileName + '_0000.nii.gz'))
                elif '_GTV' in file:
                    fileDir = os.path.join(
                        nnUNet_raw_data, os.path.join(taskFolderName, 'labelsTr'))
                    if not os.path.exists(fileDir):
                        os.makedirs(fileDir)
                    os.replace(os.path.join(root, file), os.path.join(
                        fileDir, newFileName + '.nii.gz'))

    for root, dirs, files in os.walk(training_folder):
        for file in files:
            if file.endswith('.nii.gz'):
                if '_PET' in file:
                    fileDir = os.path.join(
                        nnUNet_raw_data, os.path.join(taskFolderName, 'imagesTs'))
                    if not os.path.exists(fileDir):
                        os.makedirs(fileDir)
                    os.replace(os.path.join(root, file), os.path.join(
                        fileDir, file))



def main():
    import argparse
    parser = argparse.ArgumentParser(
        description="Convert HECKTOR data and format them to be used in nnU-Net")
    parser.add_argument("-tr", help="Training data folder", required=True)
    parser.add_argument("-ts", help="Testing data folder", required=True)
    parser.add_argument("-t", help="Task ID", default=500,
                        type=int, required=False)
    parser.add_argument("-n", help="Task name",
                        default="Hecktor", required=False)
    args = parser.parse_args()

    crawl_and_format_data_directory(args.tr, args.ts, args.t, args.n)
    taskFolderPath = os.path.join(
        nnUNet_raw_data, generate_task_folder_name(args.t, args.n))
    generate_dataset_json(os.path.join(taskFolderPath, 'dataset.json'), os.path.join(taskFolderPath, 'imagesTr'), os.path.join(taskFolderPath, 'imagesTs'), ('PT'),
                          labels={0: 'background', 1: 'label'}, dataset_name=generate_task_folder_name(args.t, args.n))


if __name__ == "__main__":
    main()
