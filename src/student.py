import tkinter as tk
import psycopg2 as psy

raiz = tk.Tk()
raiz.title("Crud Postgres")

canvas = tk.Canvas(raiz, height=380, width=400)
canvas.pack()

frame = tk.Frame()
frame.place(relx=0.1, rely = 0.1, relwidth=0.8, relheight=0.8)
label = tk.Label(frame, text="Agrega un estudiante")
label.grid(row=0, column=1)

#-------------funciones----------
def save_student(entry_list):
    #----------conexión a la base de datos-------------------
    con = psy.connect(dbname = 'postgres',
                user = 'postgres',
                password = 'hello1234',
                host = 'localhost',
                port = '5432')
    cursor = con.cursor()
    query = '''INSERT INTO students (name, age, direccion, grupo, matricula) VALUES(%s, %s, %s, %s, %s)'''
    # se crea lista de vlores extrayendo cada valor de la lista entry_list mediante ciclo for--------
    values = [entry.get() for entry in entry_list]
    cursor.execute(query, values) # se ejecuta el query pasando consulta y datos
    con.commit() #se rectifica la inserción
    cursor.close() # se cierra el cursor
    con.close()
    print('Datos insertados')
    dislay_students()


def search(id):
    con = psy.connect(dbname = 'postgres',
        user = 'postgres',
        password = 'hello1234',
        host = 'localhost',
        port = '5432')
    cursor = con.cursor()
    query = '''SELECT name, age, direccion, grupo, matricula FROM students
    WHERE ID = %s'''
    cursor.execute(query, (id))
    row = cursor.fetchone()
    display_search(row)

    con.commit()
    cursor.close()
    con.close()

def display_search(row):

    listbox = tk.Listbox(frame, width=20, height=1 )
    listbox.grid(row=10, columnspan=4, sticky=tk.W+tk.E)
    try:
        listbox.insert(tk.END, row)
    except:
        listbox.insert("No se encontró resultado", tk.END)
    

def dislay_students():
    con = psy.connect(dbname = 'postgres',
        user = 'postgres',
        password = 'hello1234',
        host = 'localhost',
        port = '5432')
    cursor = con.cursor()
    query = '''SELECT name, age, direccion, grupo, matricula FROM students'''
    cursor.execute(query)
    row = cursor.fetchall()
    listbox = tk.Listbox(frame, width=20, height=10)
    listbox.grid(row=11, columnspan=4, sticky=tk.W+tk.E)
    for x in row:
        listbox.insert(tk.END, x)  
    con.commit()
    cursor.close()
    con.close()
    #refresh estudiantes
    
#-------------labels para datos de estudiatess------------- ------
labels = [
    ('Nombre', 1, 0),
    ('Edad',2,0),
    ('Dirección',3,0),
    ('Grupo',4,0),
    ('Matricula',5,0)
]

for valor, fila, columna in labels:
    label = tk.Label(frame, text=valor)
    label.grid(row=fila, column=columna)

#------------entrys para datos báscos de los estudiantes------------
entry_list = []
entrys = [
    (1,1),
    (2,1),
    (3,1),
    (4,1),
    (5,1)
]

for rows, columns in entrys:
    entry = tk.Entry(frame)
    entry.grid(row = rows, column=columns)
    entry_list.append(entry)
    

#--------------botón save-----------

boton = tk.Button(frame, text='Agregar', command=lambda:save_student(entry_list))
boton.grid(row = 6,column=1, sticky=tk.W+tk.E)
#-------------BUSCAR-------------------
label = tk.Label(frame, text='Busca Datos')
label.grid(row=7, column=1, sticky=tk.W+tk.E)
label = tk.Label(frame, text='Busca por id')
label.grid(row=8, column=0)

id_search = tk.Entry(frame)
id_search.grid(row=8, column=1)

boton = tk.Button(frame, text='Buscar', command=lambda: search(id_search.get()))
boton.grid(row=9, column=1, sticky=tk.W+tk.E)
dislay_students()
raiz.mainloop()