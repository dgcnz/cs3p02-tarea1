# Tarea 1

**Integrantes**:

- Maria Lovaton
- Diego Canez

## Instrucciones

**Paso 1: Descargar el ISO**

```sh
python manage.py dowload_iso alpine.iso
```

**Paso 2: Crear el storage**

```sh
python manage.py create_storage storage
```

**Paso 3: Crear las maquinas virtuales**

```sh
python manage.py create_vm source storage.vdi alpine.iso
python manage.py create_vm target storage.vdi alpine.iso
```

**Paso 4: Configurar el teleportation**

```sh
python manage.py setup_teleportation target
```

**Paso 5: Iniciar las maquinas virtuales**

```sh
python manage.py start_vm source
python manage.py start_vm target
```

**Paso 6: Correr daemon con politica de migracion**

```sh
# TODO
```

**Paso 7: Inducir una carga en el host para activar el Live Migration**

```sh
# TODO
```


## Algunas fuentes:

- [Teleporting docs](https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/teleporting.html)
- [Teleportation](http://www.techsologic.com/virtualbox-live-migration.php)
- [Create VM from CLI](https://www.andreafortuna.org/2019/10/24/how-to-create-a-virtualbox-vm-from-command-line/)
