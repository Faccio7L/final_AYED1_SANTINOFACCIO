from tabulate import tabulate
import json
import re
def importar_datos(datos:dict)->list[str]:
    """
    Se lee un csv y se importa en forma de diccionario.
    pre: recibe un diccionario vacio
    post: retorna los encabezados, los cuales seran utiles para exportar.
    """
    plataformas_compatibles = ("Wii","PS2","PS3","DS")
    cant_juegos = 0
   # anios_compatibles = ("2006","2007","2008","2009","2010","2011","2012","2013","2014","2015")
    try:
        with open("final.csv","rt",encoding="utf-8") as arch:
            encabezado = arch.readline()
            
            while True:
                linea = arch.readline()
                if not linea:
                    break
                else:
                    
                    linea = linea.strip().split(",")
                    linea = [elemento.strip() for elemento in linea]
                    try:
                        linea[3] = float(linea[3])
                    except Exception as e:
                        continue
                    
                    if linea[2] in plataformas_compatibles and linea[3] >= 2006 and linea[3] <= 2015 and len(linea) == 11:
                        cant_juegos += 1
                        key = linea[2] #la plataforma va a ser el key.
                        linea[3] = str(linea[3]) #nuevamente str por el futuro json.
                        a_agregar = linea[0:2]
                        a_agregar.extend(linea[2:])
                        if key in datos:
                            datos[key].append(a_agregar)
                        else:
                            datos[key] = [a_agregar] #el value es una lista de listas.
    except Exception as e:
        print(f"Ha ocurrido un error: {e}")
    else:
        print("Datos importados con exito.")
        print(f"Se han importado un total de:{cant_juegos} juegos")
        return encabezado


def salir(datos:dict[list],encabezados:list[str])->None:
   """
   Funcion que se ejecuta de manera previa antes de salir del sistema, en caso de que haya datos importados, los exporta a un nuevo csv.
   pre: recibe el diccionario de datos y los encabezados del csv origianl.
   post: No retorna nada, exporta los datos en caso de corresponder.
   
   
   """
   try:
        with open("juegos_filtrados.csv","wt",encoding="utf-8")as arch:
            arch.write(encabezados)
            for key,value in datos.items():
                for data in value:
                    a_exportar = data[0:2] +[key] + data[3:]
                    a_exportar = (",").join(a_exportar)
                    arch.write(f"{a_exportar} \n")
   except Exception as e:
     
      print(f"ha ocurrido un error{e}")
   else:
       print("Datos exportados con exito")
    


def select_plataforma(datos:dict[list])->str:
    """
    Utiidad para dos funciones, se selecciona una de las 4 plataformas importadas del csv.
    pre: recibe el diccionario con los datos importados.
    post: Retorna la opcion seleccionada.
    """
    
    opciones = list(datos.keys())
   
    for i , o in enumerate(opciones):
        print(f"{i+1}.{o}")
    while True:
        try:
            select = int(input("Ingrese un numero:"))
            select = opciones[select-1]
        except Exception as e:
            print("Opcion invalida.")
        else:
            return select

def buscar_por_nombre_plat(datos:dict[list])->None:
    """
    Se crea una  tabla para mostrar informacion sobre una plataforma especifica.
    pre: recibe el diccionario con los datos importados.
    post: No retorna nada, muestra la tabla.
    

    """

    headers = ("name","year","genre","publisher")
    select = select_plataforma(datos)
   
    if select:
        a_mostrar = [(data[1],data[2],data[3],data[4]) for key,value in datos.items() for data in value if key == select ]
        tabla = tabulate(a_mostrar,headers=headers)
        print(tabla)
        #print(type(select))
    else:
        pass



def exportar_por_plataforma(datos:dict[list])->None:
    """
    Exporta a un json en forma de lista de diccionarios la informacion de una consola especifica.
    pre: Recibe el diccionario importado
    post: No retorna nada, pero genera el archivo.
    
    """

    select = select_plataforma(datos)
    if select:
        a_exportar = [{key:data}for key,value in datos.items() for data in value if select == key]
        
        try:
            with open(f"{select}.json","wt",encoding="utf-8") as arch:
                json.dump(a_exportar,arch,indent=4,ensure_ascii=False)
        except Exception as e:
            print(f"Ha ocurrido un error:{e}")
        else:
            print("Exportacion realizada con exito.")    
    else:
        pass

def precio_de_venta_global_pokemon(datos:dict[list]):
    """
    Contabiliza las ventas globales de pokemon
    pre: Recibe como parametro el diccionario con los datos importados.
    post:No retorna nada, muestra en pantalla el monto total de ventas de pokemon.
    """
    total = 0
    for value in datos.values():
        for data in value:
            if re.compile("p[oó]k[eé]m[oó]n",re.IGNORECASE):
                try:
                    total += float(data[10])
                except Exception as e:
                    continue
    print(f"El Monto total de las ventas de Pokemon es de: ${total}")

def main()->None:
    """
    Funcion principal del sistema, invoca al resto de funciones, contiene al diccionario de datos (inicia vacio)
    pre:No recibe nada.
    post:No retorna nada, solo invoca otras funciones.
    
    """
    datos = dict()
    opciones = ("a.Importar datos","b-Buscar juegos por nombre de plataforma",
                "c.Exportar por plataforma","d-precio de venta globales pokemon","z-Salir")
    
    for op in opciones:
        print(op)
    while True:
        select = input("Ingrese una opcion:").lower()
        if select == "a":
            if not datos:
               encabezados = importar_datos(datos)
            else:
                print("Datos ya importados.")
        elif select == "z":
            if not datos:
                print("No hay datos importados")
                print("Hasta luego!")
                break
            else:
                salir(datos,encabezados)
        elif not datos:
            print("Primero debe importar los datos.")
            continue
        elif select == "b":
            buscar_por_nombre_plat(datos)
        
        elif select == "c":
            exportar_por_plataforma(datos)
        
        elif select == "d":
            precio_de_venta_global_pokemon(datos)
        else:
            print("Opcion incorrecta.")

main()