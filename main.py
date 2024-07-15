import os
import shutil
import subprocess
import time

# creating directories needed for script
directories = ["logs", "packages", "images", "mountpoint", "content"]

for directory in directories:
    os.makedirs(directory, exist_ok=True)

# making a list of data packages inside packages directory
os.chdir('packages')
packages = [file for file in os.listdir() if file.endswith(".exe")]
os.chdir('..')

# unpacking all packages one by one
for package in packages:
    print('Extracting', package + '...')

    # creating directories for current package
    package_directory = os.path.splitext(os.path.basename(package))[0]
    os.makedirs(os.path.join('images', package_directory), exist_ok=True)
    os.makedirs(os.path.join('content', package_directory), exist_ok=True)
    os.makedirs(os.path.join('logs', package_directory), exist_ok=True)

    # extracting package with IsXunpack.exe
    isxunpack_path = os.path.join('tools', 'IsXunpack.exe')
    package_path = os.path.join('packages', package)
    main_path = 'main.py'
    logs_path = os.path.join('logs', package_directory, 'isxunpack.log')
    if os.name == 'nt':
        pass
    elif os.name == 'posix':
        isxunpack_path = 'wine ' + isxunpack_path

    command = f'{isxunpack_path} {package_path} < {main_path} > {logs_path}'
    print('IsXunpack command entered:', command)

    print('IsXunpack working...')
    os.system(command)
    print('IsXunpack finished.')

    if os.name == 'posix':
        current_directory = os.getcwd()
        src = os.path.join(current_directory, 'Disk1')
        dst = os.path.join(current_directory, 'packages', 'Disk1')
        print(src)
        print(dst)
        shutil.move(src, dst)

    # coping files to extract InstallShield .cab file
    src = os.path.join('packages', 'Disk1', 'data1.hdr')
    dst = os.path.join('packages', 'Disk1', 'data2.hdr')
    shutil.copy(src, dst)

    # extracting InstallShield .cab file with i6comp.exe
    i6comp_path = os.path.join('tools', 'i6comp.exe')
    cab_path = os.path.join('packages', 'Disk1', 'data2.cab')
    dest_path = os.path.join('packages', 'data2')
    logs_path = os.path.join('logs', package_directory, 'i6comp.log')

    command = f'{i6comp_path} x -rdf {cab_path} * {dest_path} > {logs_path}'
    if os.name == 'posix':
        command = f'wine cmd /c "{command}"'
    print('i6comp command entered:', command)

    print('i6comp working...')
    os.system(command)
    print('i6comp finished.')

    # coping archive.dpc and DPcompactor.exe to images directory
    shutil.copy(os.path.join('packages', 'data2', 'DPcompactor.exe'),
                os.path.join('images', package_directory))
    shutil.copy(os.path.join('packages', 'data2', 'archive.dpc'),
                os.path.join('images', package_directory))

    # extracting .cnt files with DPcompactor.exe
    os.chdir(os.path.join('images', package_directory))

    dpcompactor = 'DPcompactor.exe'
    archive = 'archive.dpc'

    command = f'{dpcompactor} {archive}'
    if os.name == 'posix':
        command = 'wine ' + command
    print('DPcompactor command entered:', command)

    print('DPcompactor working...')
    os.system(command)
    print('DPcompactor finished.')

    print('Removing garbage...')
    # removing archive.dpc and DPcompactor.exe
    os.remove(dpcompactor)
    os.remove(archive)
    os.chdir(os.path.join('..', '..'))

    # making a list of all extracted files
    images = os.listdir(os.path.join('images', package_directory))

    # removing all non-necessary files
    for file in images:
        if 'image' not in file:
            os.remove(os.path.join('images', package_directory, file))

    # making a list of all files containing predefined content
    images = os.listdir(os.path.join('images', package_directory))

    # extracting all images one by one using custom .py file
    print('Extracting all the images...')
    for image in images:
        # creating directories for current image
        image_directory = os.path.splitext(os.path.basename(image))[1][1:]
        os.makedirs(os.path.join('content', package_directory, image_directory), exist_ok=True)

        logs = os.path.join("content", package_directory, 'extract.log')
        with open(logs, "a") as log_file:
            log_file.write(f"{image}\n")

        extract_py_path = 'extract.py'
        image_path = os.path.join('images', package_directory, image)
        dest_path = os.path.join('images', package_directory, image + '.img')

        if os.name == 'nt':
            command = f'python {extract_py_path} {image_path} {dest_path}'
        if os.name == 'posix':
            command = f'python3 {extract_py_path} {image_path} {dest_path}'

        os.system(command)

    images = os.listdir(os.path.join('images', package_directory))

    # removing all non-necessary files
    for file in images:
        extension = os.path.splitext(os.path.join('images', package_directory, file))[-1]
        if extension != '.img':
            os.remove(os.path.join('images', package_directory, file))

    images = os.listdir(os.path.join('images', package_directory))

    # mounting images got by custom .py file and coping all the content to named folder
    print('Coping all the content...')
    for image in images:
        current_image = os.path.join('images', package_directory, image)

        if os.name == 'posix':
            command = f'sudo mount -t vfat -o utf8=1 {current_image} mountpoint'
            os.system(command)
            dest_dir = image.split('.')[-2]
            shutil.copytree('mountpoint',
                            os.path.join('content', package_directory, dest_dir),
                            dirs_exist_ok=True)
            time.sleep(3)
            command = f'sudo umount mountpoint'
            os.system(command)
            command = f'history -c'
            os.system(command)

        if os.name == 'nt':
            command = f'wsl echo "laissez" ^| sudo -S mount -t vfat -o utf8=1 images/{package_directory}/{image} mountpoint'
            os.system(command)
            dest_dir = image.split('.')[-2]
            command = f'wsl cp -a mountpoint/. content/{package_directory}/{dest_dir}'
            os.system(command)
            time.sleep(3)
            command = f'wsl echo "laissez" ^| sudo -S umount mountpoint'
            os.system(command)
            command = f'wsl history -c'
            os.system(command)
