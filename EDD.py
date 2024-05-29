class Paciente:
    def __init__(self, numero_paciente, genero, nombre, edad, triaje):
        self.numero_paciente = numero_paciente
        self.genero = genero
        self.nombre = nombre
        self.edad = edad
        self.triaje = triaje

    def __lt__(self, other):
        return self.triaje < other.triaje

    def __str__(self):
        return f"Paciente({self.numero_paciente}, {self.nombre}, {self.genero}, {self.edad}, Triaje: {self.triaje})"

class Queue:
    def __init__(self):
        self.queue = []

    def enqueue(self, data):
        self.queue.append(data)

    def dequeue(self):
        if len(self.queue) == 0:
            return None
        return self.queue.pop(0)

    def is_empty(self):
        return len(self.queue) == 0

class MinHeap:
    def __init__(self, data=None):
        self.data = data
        self.leftchild = None
        self.rightchild = None

    def insertar(self, paciente):
        if self.data is None:
            self.data = paciente
        else:
            aux_queue = Queue()
            aux_queue.enqueue(self)
            while not aux_queue.is_empty():
                current = aux_queue.dequeue()
                if current.leftchild is None:
                    current.leftchild = MinHeap(paciente)
                    self.heapify_up(current.leftchild)
                    break
                else:
                    aux_queue.enqueue(current.leftchild)
                if current.rightchild is None:
                    current.rightchild = MinHeap(paciente)
                    self.heapify_up(current.rightchild)
                    break
                else:
                    aux_queue.enqueue(current.rightchild)

    def heapify_up(self, node):
        if node is None or node.data is None:
            return
        parent = self.obtener_padre(node)
        if parent and node.data < parent.data:
            node.data, parent.data = parent.data, node.data
            self.heapify_up(parent)

    def obtener_padre(self, node):
        aux_queue = Queue()
        aux_queue.enqueue(self)
        while not aux_queue.is_empty():
            current = aux_queue.dequeue()
            if current.leftchild == node or current.rightchild == node:
                return current
            if current.leftchild:
                aux_queue.enqueue(current.leftchild)
            if current.rightchild:
                aux_queue.enqueue(current.rightchild)
        return None

    def heapify_down(self, node):
        if node is None:
            return
        smallest = node
        if node.leftchild and node.leftchild.data < smallest.data:
            smallest = node.leftchild
        if node.rightchild and node.rightchild.data < smallest.data:
            smallest = node.rightchild
        if smallest != node:
            node.data, smallest.data = smallest.data, node.data
            self.heapify_down(smallest)

    def consultar_proximo(self):
        if self.data:
            return self.data
        else:
            return "No hay pacientes en la cola de prioridad."
        
    def atender_siguiente(self):
        if self.data:
            paciente_atendido = self.data
            last_node, last_parent = self.obtenernodo_y_padre()
            if last_node == self:
                self.data = None
            else:
                self.data = last_node.data
                if last_parent.rightchild == last_node:
                    last_parent.rightchild = None
                else:
                    last_parent.leftchild = None
                self.heapify_down(self)
            return paciente_atendido
        else:
            return None

    def obtenernodo_y_padre(self):
        aux_queue = Queue()
        aux_queue.enqueue((self, None))
        last_node, last_parent = None, None
        while not aux_queue.is_empty():
            current, parent = aux_queue.dequeue()
            last_node, last_parent = current, parent
            if current.leftchild:
                aux_queue.enqueue((current.leftchild, current))
            if current.rightchild:
                aux_queue.enqueue((current.rightchild, current))
        return last_node, last_parent

    def imprimir_pacientes_en_espera(self):
        aux_queue = Queue()
        if self.data:
            aux_queue.enqueue(self)
            print("Pacientes en espera:")
            while not aux_queue.is_empty():
                current = aux_queue.dequeue()
                print(current.data)
                if current.leftchild:
                    aux_queue.enqueue(current.leftchild)
                if current.rightchild:
                    aux_queue.enqueue(current.rightchild)
        else:
            print("No hay pacientes en la cola de prioridad.")

    def imprimir_pacientes_por_triaje(self, triaje):
        aux_queue = Queue()
        if self.data:
            aux_queue.enqueue(self)
            print(f"Pacientes en espera con triaje {triaje}:")
            encontrado = False
            while not aux_queue.is_empty():
                current = aux_queue.dequeue()
                if current.data.triaje == triaje:
                    print(current.data)
                    encontrado = True
                if current.leftchild:
                    aux_queue.enqueue(current.leftchild)
                if current.rightchild:
                    aux_queue.enqueue(current.rightchild)
            if not encontrado:
                print(f"No hay pacientes con triaje {triaje} en la cola de prioridad.")
        else:
            print("No hay pacientes en la cola de prioridad.")

    def eliminar_paciente(self, id_paciente=None, nombre_paciente=None):
        if not self.data:
            print("No hay pacientes en la cola de prioridad.")
            return False

        def busqueda_eliminacion(heap, id_paciente, nombre_paciente):
            if heap is None:
                return None, False
            if (id_paciente is not None and heap.data.numero_paciente == id_paciente) or \
               (nombre_paciente is not None and heap.data.nombre == nombre_paciente):
                last_node, last_parent = self.obtenernodo_y_padre()
                if last_node == heap:
                    return None, True
                heap.data = last_node.data
                if last_parent.rightchild == last_node:
                    last_parent.rightchild = None
                else:
                    last_parent.leftchild = None
                self.heapify_down(heap)
                return heap, True
            heap.leftchild, deleted = busqueda_eliminacion(heap.leftchild, id_paciente, nombre_paciente)
            if deleted:
                return heap, True
            heap.rightchild, deleted = busqueda_eliminacion(heap.rightchild, id_paciente, nombre_paciente)
            return heap, deleted

        self, deleted = busqueda_eliminacion(self, id_paciente, nombre_paciente)
        if deleted:
            print(f"Paciente con {'ID ' + str(id_paciente) if id_paciente else 'nombre ' + nombre_paciente} eliminado con éxito.")
            return True
        else:
            print(f"Paciente con {'ID ' + str(id_paciente) if id_paciente else 'nombre ' + nombre_paciente} no encontrado.")
            return False

    def printTree(self, prefix="", is_left=True):
        if self.rightchild:
            self.rightchild.printTree(prefix + ("│ " if is_left else " "), False)
        print(prefix + ("└── " if is_left else "┌── ") + str(self.data))
        if self.leftchild:
            self.leftchild.printTree(prefix + (" " if is_left else "│ "), True)

def mostrar_menu():
    print("---- Menú de Gestión de Pacientes ----")
    print("1. Agregar paciente")
    print("2. Consultar próximo paciente")
    print("3. Atender siguiente paciente")
    print("4. Consultar pacientes en espera")
    print("5. Consultar pacientes en espera por triaje")
    print("6. Eliminar paciente")
    print("7. Imprimir árbol de pacientes")
    print("8. Salir")

def main():
    heap = MinHeap()
    while True:
        mostrar_menu()
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            numero_paciente = int(input("Número de paciente: "))
            genero = input("Género: ")
            nombre = input("Nombre: ")
            edad = int(input("Edad: "))
            triaje = int(input("Nivel de triaje (1-5): "))
            paciente = Paciente(numero_paciente, genero, nombre, edad, triaje)
            heap.insertar(paciente)
            print("Paciente agregado con éxito.")
        elif opcion == "2":
            proximo = heap.consultar_proximo()
            if proximo:
                print(f"El próximo paciente es: {proximo}")
            else:
                print("No hay pacientes en la cola de prioridad.")
        elif opcion == "3":
            atendido = heap.atender_siguiente()
            if atendido:
                print(f"Atendiendo al paciente: {atendido}")
            else:
                print("No hay pacientes en la cola de prioridad.")
        elif opcion == "4":
            heap.imprimir_pacientes_en_espera()
        elif opcion == "5":
            triaje = int(input("Ingrese el nivel de triaje (1-5): "))
            heap.imprimir_pacientes_por_triaje(triaje)
        elif opcion == "6":
            criterio = input("Eliminar por (1) ID o (2) Nombre: ")
            if criterio == "1":
                id_paciente = int(input("Ingrese el ID del paciente: "))
                heap.eliminar_paciente(id_paciente=id_paciente)
            elif criterio == "2":
                nombre_paciente = input("Ingrese el nombre del paciente: ")
                heap.eliminar_paciente(nombre_paciente=nombre_paciente)
            else:
                print("Criterio no válido.")
        elif opcion == "7":
            heap.printTree()
        elif opcion == "8":
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida, por favor seleccione nuevamente.")

if __name__ == "__main__":
    main()


