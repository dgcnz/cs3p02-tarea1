# Tarea 1

## 1. Crear un script (bash, libvirt, etc.) que ejecute la operacion de Live Migration.

1.VirtualBox: Teleport
2.KVM: live migration
3.Xen: live migration

## 2.Crear una politica simple que me permita controlar operaciones de live migration

2.1 Ejemplo de politica
CPU > 80% - trigger Live Migration,,,  :   id-1
CPU 85% - Live Migration                      :   id-2
2.2 CPU, memoria> Ejemplo de aplicacion para generar carga
$ apt get install stress-ng
$ sleep 30; stress-ng --cpu 2 –memory : 250MB – i/o
