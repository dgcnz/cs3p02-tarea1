# Tarea 1

## 1. Crear un script (bash, libvirt, etc.) que ejecute la operacion de Live Migration.

1. VirtualBox: Teleport
2. KVM: live migration
3. Xen: live migration

**VirtualBox Teleport:**

- [Teleporting docs](https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/teleporting.html)
- [Ubuntu Server VDI](https://www.osboxes.org/ubuntu-server/)
- [Teleportation](http://www.techsologic.com/virtualbox-live-migration.php)

**Procedure**

1. Create `SOURCE` and `TARGET` VM. Both must share exactly the same specs and storage.
2. `VBoxManage modifyvm TARGET --teleporter on --teleporterport PORT`
    - `PORT` is a TCP/IP port used on both `SOURCE` and `TARGET`.
3. Start `TARGET`. It will wait for a teleport request.
4. Start `SOURCE`.
5. `VBoxManage controlvm SOURCE teleport --host TARGETHOST --port PORT`
    - `TARGETHOST` is the host or IP name of the target host on which `TARGET` is running.
    - `PORT` is the same as step 2.

## 2.Crear una politica simple que me permita controlar operaciones de live migration

1. Ejemplo de politica
    - CPU > 80% - trigger Live Migration,,,  :   id-1
    - CPU 85% - Live Migration                      :   id-2
2.  CPU, memoria> Ejemplo de aplicacion para generar carga
    - `$ apt get install stress-ng`
    - `$ sleep 30; stress-ng --cpu 2 –memory : 250MB –i/o`

## Instructions

**Step 1: Download iso**

```sh
python manage.py dowload_iso alpine.iso
```

**Step 2: Create storage**

```sh
python manage.py create_storage storage
```

**Step 3: Create vms**

```sh
python manage.py create_vm source storage.vdi alpine.iso
python manage.py create_vm target storage.vdi alpine.iso
```

**Step 4: Setup teleportation**

```sh
python manage.py setup_teleportation target
```

**Step 5: Start source and target vms**

```sh
python manage.py start_vm source
python manage.py start_vm target
```

**Step 6: Teleport**

```sh
python teleport source
```
