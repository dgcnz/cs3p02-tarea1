# Tarea 1

## 1. Crear un script (bash, libvirt, etc.) que ejecute la operacion de Live Migration.

1. VirtualBox: Teleport
2. KVM: live migration
3. Xen: live migration

**VirtualBox Teleport:**

- [Teleporting docs](https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/teleporting.html)

## 2.Crear una politica simple que me permita controlar operaciones de live migration

1. Ejemplo de politica
    - CPU > 80% - trigger Live Migration,,,  :   id-1
    - CPU 85% - Live Migration                      :   id-2
2.  CPU, memoria> Ejemplo de aplicacion para generar carga
    - `$ apt get install stress-ng`
    - `$ sleep 30; stress-ng --cpu 2 –memory : 250MB –i/o`
