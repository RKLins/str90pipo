#!/usr/bin/python3


import os
import pathlib
import rockchip_environment
import shutil
import tired.command
import tired.fs
import tired.logging
import tired.git


HERE = pathlib.Path(__file__).resolve().parent
RKBIN = HERE.parent / "rkbin"
LINARO_UBUNTU_ROOTFS_PATH = HERE.parent / 'rootfs'
LINARO_ARCHIVE_PATH = tired.fs.find_unique("linaro*tar.gz", LINARO_UBUNTU_ROOTFS_PATH)
GIT_ROOT = tired.git.get_git_directory_from_nested_context()


def main():
    try:
        os.mkdir("temp")
    except FileExistsError:
        pass

    rockchip_environment.update_env()

    tired.command.execute("sudo apt-get install qemu-user-static binfmt-support")

    # Bootstrap filesystem
    script = " && ".join([
        "sudo rm -rf /mnt/linaro",
        "sudo mkdir -p /mnt/linaro",

        # Create loop device
        "dd if=/dev/zero of=rootfs.ext4 bs=1M count=1024",
        "mkfs.ext4 -F -L linuxroot rootfs.ext4 ",
        "sudo mount -o loop rootfs.ext4 /mnt/linaro",

        # Mount archive
        f'sudo mkdir -p /mnt/linaro',
        f'sudo tar zxvf {LINARO_ARCHIVE_PATH} -C /mnt/linaro',
        f'sudo mv /mnt/linaro/binary/boot/filesystem.dir/* /mnt/linaro',
        f'sudo rm -rf /mnt/linaro/binary',

        # install modules
        "sudo mkdir -p /mnt/linaro/lib/modules",
        f"sudo cp -r {GIT_ROOT}/modules/lib/modules/3.0.36+ /mnt/linaro/lib/modules",

        # Prepare chroot
        "sudo cp /usr/bin/qemu-arm-static /mnt/linaro/usr/bin",
        "sudo modprobe binfmt_misc",
        "sudo mount -t devpts devpts /mnt/linaro/dev/pts",
        "sudo mount -t proc proc /mnt/linaro/proc",

        # According to this instruction (https://wiki.radxa.com/Rock/ubuntu), some additional network packages must be installed ther, some additional network packages must be installed there.

        # Umount
        "sudo umount -t devpts devpts /mnt/linaro/dev/pts",
        "sudo umount -t proc proc /mnt/linaro/proc",
        "sudo umount /mnt/linaro",
    ])

    tired.command.execute(f"bash -c '{script}'")

if __name__ == "__main__":
    main()
