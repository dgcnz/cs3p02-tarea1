import sys
import os
import argparse
import subprocess


def download_iso(args):
    cmd = f'wget http://releases.ubuntu.com/raring/ubuntu-13.04-server-amd64.iso -O {args.iso_path}'
    subprocess.run(cmd.split())


def setup_teleportation(args):
    # TODO argparse
    cmd = f'VBoxManage modifyvm {args.target_vm} --teleporter on --teleporterport {args.port}'
    subprocess.run(cmd.split())


def teleport(args):
    # TODO argparse
    cmd = f'VBoxManage controlvm {args.source_vm} teleport --host {args.target_host} --port {args.port}'
    subprocess.run(cmd.split())


def run(args):
    # TODO argparse
    cmd = f'VBoxManage --nologo guestcontrol {args.vm_name} run --exe {args.command} --wait-exit --wait-stdout'
    result = subprocess.run(cmd.split(),
                            capture_output=True,
                            universal_newlines=True)
    print(result.stdout)
    print(result.stderr)


def create_vm(args):
    commands = [
        f'VBoxManage createvm --name {args.vm_name} --ostype "Ubuntu_64" --register --basefolder {os.getcwd()}',
        f'VBoxManage modifyvm {args.vm_name} --ioapic on',
        f'VBoxManage modifyvm {args.vm_name} --memory 1024 --vram 128',
        f'VBoxManage modifyvm {args.vm_name} --nic1 nat',
        f'VBoxManage storagectl {args.vm_name} --name "SATA Controller" --add sata --controller IntelAhci',
        f'VBoxManage storageattach {args.vm_name} --storagectl "SATA Controller" --port 0 --device 0 --type hdd --medium {args.storage_name}',
        f'VBoxManage storagectl {args.vm_name} --name "IDE Controller" --add ide --controller PIIX4',
        f'VBoxManage storageattach {args.vm_name} --storagectl "IDE Controller" --port 1 --device 0 --type dvddrive --medium {args.iso_path}',
        f'VBoxManage modifyvm {args.vm_name} --boot1 dvd --boot2 disk --boot3 none --boot4 none',
        f'VBoxManage modifyvm {args.vm_name} --vrde on',
        f'VBoxManage modifyvm {args.vm_name} --vrdemulticon on --vrdeport 10001'
    ]
    for cmd in commands:
        subprocess.run(cmd.split())


def create_storage(args):
    cmd = f"VBoxManage createhd --filename {args.storage_name} --size 80000 --format VDI"
    subprocess.run(cmd.split())


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Manager.')
    subparsers = parser.add_subparsers()

    parser_create_storage = subparsers.add_parser('create_storage')
    parser_create_storage.set_defaults(func=create_storage)
    parser_create_storage.add_argument('storage_name',
                                       type=str,
                                       help='The name of the storage.')

    parser_create_vm = subparsers.add_parser('create_vm')
    parser_create_vm.set_defaults(func=create_vm)
    parser_create_vm.add_argument('vm_name',
                                  type=str,
                                  help='The name of the virtual machine.')
    parser_create_vm.add_argument('storage_name',
                                  type=str,
                                  help='The name of the storage.')

    parser_create_vm.add_argument('iso_path',
                                  type=str,
                                  help='Path to iso downloaded.')

    parser_download_iso = subparsers.add_parser('download_iso')
    parser_download_iso.set_defaults(func=download_iso)
    parser_download_iso.add_argument('iso_path',
                                     type=str,
                                     help='Path to download iso to.')
    args = parser.parse_args()
    args.func(args)
