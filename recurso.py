#--------------------------------------------------------------------
# Autor: Treius
# Fecha: 12/12/2023
#
# Descripción:  Programa que a partir del primer parámetro cree el directorio (si no existe)
#               y genere un recurso compartido en el archivo de configuración smb.conf.
#               Además, solo los usuarios del dominio tendrán permisos de escritura
#-------------------------------------------------------------------

import os
import sys

argumentosTotales = len(sys.argv)

# Checkea si se han ingresado el nº de args necesarios
if argumentosTotales<2:
    print("Es necesario especificar el nombre del recurso")
    sys.exit(1)
elif argumentosTotales>2:
    print("Solo hay que usar un parámetro")
    sys.exit(1)
recurso = sys.argv[1]

# Si no existe /opt/{recurso} lo crea y hace su enlace simbólico
if not os.path.exists(f"/opt/{recurso}"):
    os.system(f"mkdir /opt/{recurso}")
    os.system(f"mkdir /recursos")
    os.symlink(f"/opt/{recurso}", f"/recursos/{recurso}")    # Hace un enlace simbólico de /opt/{recurso} a /recursos/{recurso}

# Cambia los permisos y propietario del enlace simbólico para que los Usuarios del dominio sean el grupo propietario y tengan permisos rwx
os.chmod(f"/recursos/{recurso}", 0o000)
os.chmod(f"/recursos/{recurso}", 0o770)
os.system(f"chown :'Usuarios del dominio' /recursos/{recurso}")

# Añade la configuración al final de smb.conf
config_line = f"\n[{recurso}]\n   path = /recursos/{recurso}\n   valid users = @'Usuarios del dominio'\n   writable = yes\n"
with open('/etc/samba/smb.conf', 'a') as smb_conf:
    smb_conf.write(config_line)

#os.system('pause')
