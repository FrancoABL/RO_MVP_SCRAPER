import csv
from datetime import datetime

def es_del_dia(fecha_str):
    """Verifica si la fecha es del día actual."""
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d %H:%M:%S")
    return fecha.date() == datetime.today().date()

def leer_csv(filepath):
    """Lee el archivo CSV y devuelve una lista de diccionarios."""
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return list(reader)

def escribir_csv(filepath, data):
    """Escribe una lista de diccionarios en un archivo CSV."""
    with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["MVP Name", "MVP Time", "MVP MAP"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)

def filtrar_y_ordenar_mvp(mvp_list):
    """Filtra los MVP que no son del día actual y elimina duplicados dejando el más reciente de cada mapa."""
    mvp_dict = {}
    for mvp in mvp_list:
        if es_del_dia(mvp["MVP Time"]) and mvp["MVP MAP"] != "rentb3":
            name = mvp["MVP Name"]
            map_ = mvp["MVP MAP"]
            time = datetime.strptime(mvp["MVP Time"], "%Y-%m-%d %H:%M:%S")
            key = (name, map_)
            if key not in mvp_dict or time > mvp_dict[key]["time"]:
                mvp_dict[key] = {"time": time, "data": mvp}
    return [mvp["data"] for mvp in mvp_dict.values()]

# Leer el archivo CSV
mvp_list = leer_csv("mvp_names.csv")

# Filtrar y ordenar los MVP
mvp_list_filtrada = filtrar_y_ordenar_mvp(mvp_list)

# Escribir el archivo CSV actualizado
escribir_csv("mvp_names.csv", mvp_list_filtrada)

print("Archivo CSV actualizado.")