import os
import django
import pandas as pd

# 1. Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from activos.models import ImpresoraInstalada, ModeloImpresora


def cargar_datos():
    # 2. Buscar el archivo Excel en la carpeta raíz
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    archivo = os.path.join(BASE_DIR, 'Impresoras.xlsx')

    if not os.path.exists(archivo):
        print(f"Error: No se encontró el archivo {archivo}")
        print(
            "Asegúrate de que 'Impresoras_2.xlsx' esté guardado en la misma"
            " carpeta que manage.py"
        )
        return

    # 3. Leer y limpiar nombres de columnas
    df = pd.read_excel(archivo)
    df.columns = [col.strip() for col in df.columns]

    print(f"Leyendo datos desde {archivo}...")
    cargados = 0

    for _, row in df.iterrows():
        nombre_modelo = str(row['Modelo']).strip()
        sn = str(row['numero_serie']).strip()
        oficina = str(row['Oficina']).strip()
        ubicacion = str(row['Ubicación']).strip()

        # Crear o buscar el modelo base de impresora (HP)
        modelo_obj, _ = ModeloImpresora.objects.get_or_create(
            modelo=nombre_modelo, defaults={'marca': 'HP', 'tecnologia': 'Láser'}
        )

        # Crear o actualizar la impresora en la oficina
        obj, created = ImpresoraInstalada.objects.update_or_create(
            numero_serie=sn,
            defaults={
                'modelo': modelo_obj,
                'oficina': oficina,
                'ubicacion': ubicacion,
            },
        )
        if created:
            cargados += 1

    print(f"¡Éxito! Se registraron {cargados} impresoras instaladas.")


if __name__ == '__main__':
    cargar_datos()