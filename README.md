# Tarea 1

[**Video del uso**](docs/recording.mp4)

**Integrantes**:

- Diego Canez
- Maria Lovaton

## Instrucciones

**Paso 0: Previos**

Usar Python3, e instalar requerimientos:
```sh
pip install -r requirements.txt
```

Documentacion:
```sh
python manage.py --help
python manage.py [command] --help
```

**Paso 1: Descargar el ISO**

```sh
python manage.py download_iso alpine.iso
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

# Este comando se quedara esperando a la migracion
python manage.py start_vm target
```

**Paso 6: Correr daemon con politica de migracion**

Politica configurable:
1. `CPU_USAGE` (80.0, en el ejemplo)
2. `MEMORY_USAGE` (30.0% en el ejemplo)
3. `TIME_THRESHOLD` (5 segundos en el ejemplo)

```sh
# Este comando se quedara esperando a que la politica se active y se migre source
python manage.py monitor source 80.0 30.0 5
```

**Paso 7: Inducir una carga en el host para activar el Live Migration**

```sh
stress --cpu 2 --io 4 --vm 2 --hdd 1 --timeout 15s
```

## Algunas fuentes:

- [Teleporting docs](https://docs.oracle.com/en/virtualization/virtualbox/6.0/admin/teleporting.html)
- [Teleportation](http://www.techsologic.com/virtualbox-live-migration.php)
- [Create VM from CLI](https://www.andreafortuna.org/2019/10/24/how-to-create-a-virtualbox-vm-from-command-line/)
