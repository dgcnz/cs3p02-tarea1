import argparse
import os
import re
import shlex
import subprocess
import sys
import time


def monitor(args):
    while True:
        cmd = ["vmstat", "-a"]
        result = subprocess.run(cmd, capture_output=True, universal_newlines=True)

        if result.stderr:
            raise Exception("vmstat failed")

        raw_metrics = re.split(" +", result.stdout.split("\n")[2].strip())
        metrics = [int(i) for i in raw_metrics]
        cpu_usage = metrics[12]
        vm_usage = (metrics[5] / (metrics[4] + metrics[5])) * 100

        maxed_out_cpu = args.max_cpu_usage < cpu_usage
        maxed_out_vm = args.max_vm_usage < vm_usage
        if maxed_out_cpu or maxed_out_vm:
            print("time to do something")
            break

        time.sleep(3)


def download_iso(args):
    cmd = f"wget https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-10.9.0-amd64-netinst.iso -O {args.iso_path}"
    subprocess.run(shlex.split(cmd))


def setup_teleportation(args):
    cmd = f"VBoxManage modifyvm {args.target_vm} --teleporter on --teleporterport 12345"
    subprocess.run(shlex.split(cmd))


def teleport(args):
    cmd = (
        f"VBoxManage controlvm {args.source_vm} teleport --host localhost --port 12345"
    )
    subprocess.run(shlex.split(cmd))


def start_vm(args):
    cmd = f"VBoxManage startvm {args.vm_name} --type headless"
    subprocess.run(shlex.split(cmd))


def run(args):
    cmd = f"VBoxManage --nologo guestcontrol {args.vm_name} run --exe {args.command} --wait-stdout"
    result = subprocess.run(
        shlex.split(cmd), capture_output=True, universal_newlines=True
    )
    print(result.stdout)
    print(result.stderr)


def create_vm(args):
    commands = [
        f'VBoxManage createvm --name {args.vm_name} --ostype "Debian_64" --register --basefolder {os.getcwd()}',
        f"VBoxManage modifyvm {args.vm_name} --ioapic on",
        f"VBoxManage modifyvm {args.vm_name} --memory 1024 --vram 128",
        f"VBoxManage modifyvm {args.vm_name} --nic1 nat",
        f'VBoxManage storagectl {args.vm_name} --name "SATA Controller {args.vm_name}" --add sata --controller IntelAhci',
        f'VBoxManage storageattach {args.vm_name} --storagectl "SATA Controller {args.vm_name}" --port 0 --device 0 --type hdd --medium {args.storage_name}',
        f'VBoxManage storagectl {args.vm_name} --name "IDE Controller {args.vm_name}" --add ide --controller PIIX4',
        f'VBoxManage storageattach {args.vm_name} --storagectl "IDE Controller {args.vm_name}" --port 1 --device 0 --type dvddrive --medium {args.iso_path}',
        f"VBoxManage modifyvm {args.vm_name} --boot1 dvd --boot2 disk --boot3 none --boot4 none",
        f"VBoxManage modifyvm {args.vm_name} --vrde on",
        f"VBoxManage modifyvm {args.vm_name} --vrdemulticon on --vrdeport 10001",
    ]
    for cmd in commands:
        subprocess.run(shlex.split(cmd))


def create_storage(args):
    cmd = (
        f"VBoxManage createhd --filename {args.storage_name} --size 80000 --format VDI"
    )
    subprocess.run(shlex.split(cmd))


def main():
    parser = argparse.ArgumentParser(description="Manager.")
    subparsers = parser.add_subparsers()

    parser_create_storage = subparsers.add_parser("create_storage")
    parser_create_storage.set_defaults(func=create_storage)
    parser_create_storage.add_argument(
        "storage_name", type=str, help="The name of the storage."
    )

    parser_create_vm = subparsers.add_parser("create_vm")
    parser_create_vm.set_defaults(func=create_vm)
    parser_create_vm.add_argument(
        "vm_name", type=str, help="The name of the virtual machine."
    )
    parser_create_vm.add_argument(
        "storage_name", type=str, help="The name of the storage."
    )
    parser_create_vm.add_argument("iso_path", type=str, help="Path to iso downloaded.")

    parser_download_iso = subparsers.add_parser("download_iso")
    parser_download_iso.set_defaults(func=download_iso)
    parser_download_iso.add_argument(
        "iso_path", type=str, help="Path to download iso to."
    )

    parser_start_vm = subparsers.add_parser("start_vm")
    parser_start_vm.set_defaults(func=start_vm)
    parser_start_vm.add_argument(
        "vm_name", type=str, help="The name of the virtual machine."
    )

    parser_run = subparsers.add_parser("run")
    parser_run.set_defaults(func=run)
    parser_run.add_argument(
        "vm_name", type=str, help="The name of the virtual machine."
    )
    parser_run.add_argument(
        "command", type=str, help="Command to run on virtual machine."
    )

    parser_setup_teleportation = subparsers.add_parser("setup_teleportation")
    parser_setup_teleportation.set_defaults(func=setup_teleportation)
    parser_setup_teleportation.add_argument(
        "target_vm", type=str, help="The name of the target virtual machine."
    )

    parser_teleport = subparsers.add_parser("teleport")
    parser_teleport.set_defaults(func=teleport)
    parser_teleport.add_argument(
        "source_vm", type=str, help="the name of the source virtual machine."
    )

    parser_monitor = subparsers.add_parser("monitor")
    parser_monitor.set_defaults(func=monitor)
    parser_monitor.add_argument("max_cpu_usage", type=int, help="Max CPU usage.")
    parser_monitor.add_argument(
        "max_vm_usage", type=int, help="Max virtual memory usage."
    )

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
