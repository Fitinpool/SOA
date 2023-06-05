# print('Data : OKgprod\n\n')

# print('Data : OKdbges\n\n')

# print('Data : OKgcate\n\n')


print('\n\nAgregar Producto\n\n')

print('Ingrese el nombre del producto: Polera')
print('Ingrese la descripción del producto: Polera de algodón')
print('Ingrese el precio del producto: 10000')
print('Ingrese el stock del producto: 100')
print('Ingrese la fecha de vencimiento del producto (dd/mm/aaaa) o dejar en blanco: \n\n')

print('Mensaje enviado al servidor: 00054gprodadd:Polera:Polera de algodón:10000:100:01/01/2000\n\n')

print('Respuesta del servidor: 00008gprodOK1\n\n')

print('Presione ENTER para continuar...\n\n')


# print('Data : gprodadd:Polera:Polera de algodón:10000:100:01/01/2000')
# print('query : INSERT INTO Productos (nombre, descripcion, precio, stock, fecha_vencimiento) VALUES (%s,%s,%s,%s,%s)')
# print('Tokens : [Polera, Polera de algodón, 10000, 100, 01/01/2000]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gprodOK1\n\n')

# print('Data : dbges1:INSERT INTO Productos (nombre, descripcion, precio, stock, fecha_vencimiento) VALUES (%s,%s,%s,%s,%s):Polera,Polera de algodón,10000,100,01/01/2000')

# print('Respuesta : 00008dbgesOK1\n\n')


# print('\n\nEditar Producto\n\n')

# print('Ingrese el ID del producto: 1')
# print('Ingrese el nombre del producto: Polera Verde')
# print('Ingrese la descripción del producto: Polera de algodón')
# print('Ingrese el precio del producto: 10000')
# print('Ingrese el stock del producto: 100')
# print('Ingrese la fecha de vencimiento del producto (dd/mm/aaaa) o dejar en blanco: \n\n')

# print('Mensaje enviado al servidor: 00063gprodedit:1:Polera Verde:Polera de algodón:10000:100:01/01/2000\n\n')

# print('Respuesta del servidor: 00008gprodOK1\n\n')

# print('Presione ENTER para continuar...\n\n')

# print('Data : gprodedt:1:Polera Verde:Polera de algodón:10000:100:01/01/2000')
# print('query : UPDATE Productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, fecha_vencimiento = %s WHERE id = %s')
# print('Tokens : [1, Polera Verde, Polera de algodón, 10000, 100, 01/01/2000]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gprodOK1\n\n')

# print('Data : dbges1:UPDATE Productos SET nombre = %s, descripcion = %s, precio = %s, stock = %s, fecha_vencimiento = %s WHERE id = %s:Polera Verde,Polera de algodón,10000,100,01/01/2000,1')

# print('Respuesta : 00008dbgesOK1\n\n')

print('\n\nEliminar Producto\n\n')

print('Ingrese el ID del producto: 1\n\n')

print('Mensaje enviado al servidor: 00010gproddel:1\n\n')

print('Respuesta del servidor: 00008gprodOK1\n\n')

print('Presione ENTER para continuar...\n\n')

# print('Data : gproddel:1')
# print('query : DELETE FROM Productos WHERE id=%s')
# print('Tokens : [1]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gprodOK1\n\n')

# print('Data : dbges1:DELETE FROM Productos WHERE id=%s:1')

# print('Respuesta : 00008dbgesOK1\n\n')

print('\n\nAgrega Categoria\n\n')

print('Ingrese el nombre de la categoria: Frutas\n\n')

print('Mensaje enviado al servidor: 00015gcateadd:Frutas\n\n')

print('Respuesta del servidor: 00008gcateOK1\n\n')

print('Presione ENTER para continuar...\n\n')

# print('Data : gcateadd:Frutas')

# print('query : INSERT INTO Categorias (nombre) VALUES (%s)')

# print('Tokens : [Frutas]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gcateOK1\n\n')

# print('Data : dbges1:INSERT INTO Categorias (nombre) VALUES (%s):Frutas')

# print('Respuesta : 00008dbgesOK1\n\n')

# print('\n\nEditar Categoria\n\n')

# print('Ingrese el ID de la categoria: 1')
# print('Ingrese el nombre de la categoria: Ropa Invierno\n\n')

# print('Mensaje enviado al servidor: 00025gcateedit:1:Ropa Invierno\n\n')

# print('Respuesta del servidor: 00008gcateOK1\n\n')

# print('Presione ENTER para continuar...\n\n')

# print('Data : gcateedit:1:Ropa Invierno')

# print('query : UPDATE Categorias SET nombre = %s WHERE id = %s')

# print('Tokens : [1, Ropa Invierno]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gcateOK1\n\n')

# print('Data : dbges1:UPDATE Categorias SET nombre = %s WHERE id = %s:Ropa Invierno,1')

# print('Respuesta : 00008dbgesOK1\n\n')

print('\n\nUnir Categoria-Producto\n\n')

print('Ingrese el ID de la categoria: 1')
print('Ingrese el ID del producto: 1\n\n')

print('Mensaje enviado al servidor: 00013gcateprod:1:1\n\n')

print('Respuesta del servidor: 00008gcateOK1\n\n')

print('Presione ENTER para continuar...\n\n')

# print('Data : gcateprod:1:1')

# print('query : INSERT INTO Categoria_Producto (id_categoria, id_producto) VALUES (%s,%s)')

# print('Tokens : [1, 1]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gcateOK1\n\n')

# print('Data : dbges1:INSERT INTO Categoria_Producto (id_categoria, id_producto) VALUES (%s,%s):1,1')

# print('Respuesta : 00008dbgesOK1\n\n')

print('\n\nEliminar Categoria\n\n')

print('Ingrese el ID de la categoria: 1\n\n')

print('Mensaje enviado al servidor: 00010gcatedel:1\n\n')

print('Respuesta del servidor: 00008gcateOK1\n\n')

print('Presione ENTER para continuar...\n\n')

# print('Data : gcatedel:1')

# print('query : DELETE FROM Categorias WHERE id=%s')

# print('Tokens : [1]\n\n')

# print('Respuesta de Base de Datos: 00008dbgesOK1\n\n')

# print('Respuesta : 00008gcateOK1\n\n')

# print('Data : dbges1:DELETE FROM Categorias WHERE id=%s:1')

# print('Respuesta : 00008dbgesOK1\n\n')