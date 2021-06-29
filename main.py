from tkinter import ttk
from tkinter import font
from tkinter import *
from math import ceil
from proceso import Proceso

c = []
cBloqueados = []
cListos = []
cFinalizados = []
cSuspendidos = []

class Ventana:

    def __init__(self, window):

        self.wind = window
        self.wind.title("Procesos")
        
        self.procesoActual = 0          # Sirve para validar que proceso se esta procesando y que no de error al momento de querer usar un proceso que no existe en la cola
        self.contador = 0               # Contador de procesos
        self.pausado = False            # El programa esta pausado o no
        self.errorProceso = False       # Si se preciona E cambiara a True, es el error en el proceso 
        self.ejecutar = False           # Bandera la cual ejecuta el proceso
        self.procesosAEjectar = 0       # Variable que almacena el numero de procesos digitados en un inicio
        self.quantum = 0                # Valor del quantum
        self.quantumContador = 0        # Variable que se utilizara para realizar el carrusel
        self.marcosDisponibles = 42     # Marcos disponibles
        self.primero = True

#################################### Registrar Proceso ######################################################

        # Contenedor Frame
        frame = LabelFrame(self.wind, text = "Registra nuevos procesos")
        frame.grid(row = 0, column = 0, columnspan = 5, pady = 15, padx = 10, sticky = W + E)
        
        # Entada de numero de procesos
        Label(frame, text = "Numero de procesos: ").grid(row = 0, column = 0, sticky = W)
        self.numeroProcesos = Entry(frame, width = 70)
        self.numeroProcesos.focus()
        self.numeroProcesos.grid(row = 0, column = 1, sticky = W + E)

        # Quantum
        Label(frame, text = "Quantum: ").grid(row = 0, column = 2, sticky = W, padx = 2)
        self.quantumEntry = Entry(frame, width = 30)
        self.quantumEntry.focus()
        self.quantumEntry.grid(row = 0, column = 3, sticky = W + E)

        # Boton
        self.botonGuardar = ttk.Button(frame, text = "Guardar", command = self.agregarProcesos, width = 34)
        self.botonGuardar.grid(row = 0, column = 4, columnspan = 2, sticky = W + E, padx = 3)

        # Mensaje
        self.mensaje = Label(text = "", fg = "red")
        self.mensaje.grid(row = 3, column = 0, columnspan = 3, sticky = W + E)

#############################################################################################################

########################################### Procesos nuevos #################################################

        self.textProcesosNuevos = StringVar()
        self.textProcesosNuevos.set("Procesos nuevos:   Id siguiente:   Tamaño: ")
        self.procesosNuevosLabel = Label(self.wind, textvariable = self.textProcesosNuevos)
        self.procesosNuevosLabel.grid(row = 3, column = 0, sticky = W, padx = 10, columnspan=2)  

#############################################################################################################

########################################## Paginacion #######################################################

        framePaginacion = LabelFrame(self.wind, text = "Memoria")
        framePaginacion.grid(row = 6, column = 1, padx = 10, pady = 5, sticky = W + E + N, rowspan=2)
        
        # Tabla
        self.tablaPaginacion1 = ttk.Treeview(framePaginacion, height = 23, columns = ("espacio1", "id1", "estado1"))
        self.tablaPaginacion1.grid(row = 6, column = 0)
        self.tablaPaginacion1.heading("#0", text = "Marco", anchor = W)
        self.tablaPaginacion1.column("#0", minwidth = 0, width = 50, stretch=NO)
        self.tablaPaginacion1.heading("espacio1", text = "Espacio", anchor = CENTER)
        self.tablaPaginacion1.column("espacio1", minwidth = 0, width = 70, stretch=NO)
        self.tablaPaginacion1.heading("id1", text = "Id", anchor = CENTER)
        self.tablaPaginacion1.column("id1", minwidth = 0, width = 50, stretch=NO)
        self.tablaPaginacion1.heading("estado1", text = "Estado", anchor = CENTER)
        self.tablaPaginacion1.column("estado1", minwidth = 0, width = 70, stretch=NO)

        self.tablaPaginacion2 = ttk.Treeview(framePaginacion, height = 23, columns = ("espacio2", "id2", "estado2"))
        self.tablaPaginacion2.grid(row = 6, column = 1)
        self.tablaPaginacion2.heading("#0", text = "Marco", anchor = CENTER)
        self.tablaPaginacion2.column("#0", minwidth = 0, width = 50, stretch=NO)
        self.tablaPaginacion2.heading("espacio2", text = "Espacio", anchor = CENTER)
        self.tablaPaginacion2.column("espacio2", minwidth = 0, width = 70, stretch=NO)
        self.tablaPaginacion2.heading("id2", text = "Id", anchor = CENTER)
        self.tablaPaginacion2.column("id2", minwidth = 0, width = 50, stretch=NO)
        self.tablaPaginacion2.heading("estado2", text = "Estado", anchor = CENTER)
        self.tablaPaginacion2.column("estado2", minwidth = 0, width = 70, stretch=NO)

#############################################################################################################

########################################## Procesos listos ##################################################

        frame2 = LabelFrame(self.wind, text = "Procesos listos")
        frame2.grid(row = 6, column = 0, padx = 10, pady = 5, sticky = W + E + N)
        
        # Tabla
        self.tabla = ttk.Treeview(frame2, columns = ("TME", "TT"))
        self.tabla.grid(row = 6, column = 0)
        self.tabla.heading("#0", text = "Id", anchor = W)
        self.tabla.column("#0", minwidth = 0, width = 75, stretch=NO)
        self.tabla.heading("TME", text = "TME", anchor = CENTER)
        self.tabla.column("TME", minwidth = 0, width = 75, stretch=NO)
        self.tabla.heading("TT", text = "TT", anchor = CENTER)
        self.tabla.column("TT", minwidth = 0, width = 75, stretch=NO)

#############################################################################################################

########################################## Procesos Bloqueados ##############################################

        frame5 = LabelFrame(self.wind, text = "Procesos bloqueados")
        frame5.grid(row = 7, column = 0, padx = 10, pady = 5, sticky = W + E + N)
        
        # Tabla
        self.tabla4 = ttk.Treeview(frame5, columns = ("TTB"))
        self.tabla4.grid(row = 6, column = 0)
        self.tabla4.heading("#0", text = "Id", anchor = W)
        self.tabla4.column("#0", minwidth = 0, width = 112, stretch=NO)
        self.tabla4.heading("TTB", text = "TTB", anchor = CENTER)
        self.tabla4.column("TTB", minwidth = 0, width = 113, stretch=NO)

#############################################################################################################

######################################### Proceso en ejecucion ##############################################

        self.frame3 = LabelFrame(self.wind, text = "Proceso en ejecucion")
        self.frame3.grid(row = 6, column = 2, padx = 0, pady = 5, sticky = W + E + N, ipadx = 5)

        Label(self.frame3, text = "Operacion: ").grid(row = 1, column = 1, sticky = W)
        Label(self.frame3, text = "Id: ").grid(row = 2, column = 1, sticky = W)
        Label(self.frame3, text = "TME: ").grid(row = 3, column = 1, sticky = W)
        Label(self.frame3, text = "TT: ").grid(row = 4, column = 1, sticky = W)
        Label(self.frame3, text = "TR: ").grid(row = 5, column = 1, sticky = W)
        Label(self.frame3, text = "Quantum: ").grid(row = 6, column = 1, sticky = W)
        Label(self.frame3, text = "Tamaño: ").grid(row = 7, column = 1, sticky = W)
        Label(self.frame3, text = "Num paginas: ").grid(row = 8, column = 1, sticky = W)

        self.textOp = StringVar()
        self.textOp.set("Operacion")
        self.opLabel = Label(self.frame3, textvariable = self.textOp)
        self.opLabel.grid(row = 1, column = 2, sticky = W)
        self.textId = StringVar()
        self.textId.set("Id")
        self.idLabel = Label(self.frame3, textvariable = self.textId)
        self.idLabel.grid(row = 2, column = 2, sticky = W)
        self.textTME = StringVar()
        self.textTME.set("TME")
        self.TMELabel = Label(self.frame3, textvariable = self.textTME)
        self.TMELabel.grid(row = 3, column = 2, sticky = W)
        self.textTT = StringVar()
        self.textTT.set("TT")
        self.TTLabel = Label(self.frame3, textvariable = self.textTT)
        self.TTLabel.grid(row = 4, column = 2, sticky = W)
        self.textTR = StringVar()
        self.textTR.set("TR")
        self.TRLabel = Label(self.frame3, textvariable = self.textTR)
        self.TRLabel.grid(row = 5, column = 2, sticky = W)
        self.textQuantum = StringVar()
        self.textQuantum.set("Quantum")
        self.QuantumLabel = Label(self.frame3, textvariable = self.textQuantum)
        self.QuantumLabel.grid(row = 6, column = 2, sticky = W)
        self.textTam = StringVar()
        self.textTam.set("Tamaño")
        self.TamLabel = Label(self.frame3, textvariable = self.textTam)
        self.TamLabel.grid(row = 7, column = 2, sticky = W)
        self.textNumPaginas = StringVar()
        self.textNumPaginas.set("Num paginas")
        self.numPaginasLabel = Label(self.frame3, textvariable = self.textNumPaginas)
        self.numPaginasLabel.grid(row = 8, column = 2, sticky = W)

#############################################################################################################

####################################### Procesos finalizados ################################################

        frame4 = LabelFrame(self.wind, text = "Procesos finalizados")
        frame4.grid(row = 7, column = 2, padx = 10, pady = 5, sticky = W + E + N)
        
        # Tabla
        self.tabla3 = ttk.Treeview(frame4, columns = ("op", "res"))
        self.tabla3.grid(row = 6, column = 1)
        self.tabla3.heading("#0", text = "Id", anchor = CENTER)
        self.tabla3.column("#0", minwidth = 0, width = 75, stretch=NO)
        self.tabla3.heading("op", text = "Operacion", anchor = CENTER)
        self.tabla3.column("op", minwidth = 0, width = 75, stretch=NO)
        self.tabla3.heading("res", text = "Resultado", anchor = CENTER)
        self.tabla3.column("res", minwidth = 0, width = 75, stretch=NO)

#############################################################################################################

        self.insertarTabla()
        self.eventosPorTeclado()

################################# Boton iniciar procesamiento y contador ####################################

        # Boton iniciar proceso
        self.inciarProcesamiento = ttk.Button(self.wind, text = "Iniciar procesamiento", command = self.procesamiento)
        self.inciarProcesamiento.grid(row = 8, columnspan = 3, pady = 10)
        self.inciarProcesamiento["state"] = DISABLED

        self.textContador = StringVar()
        self.textContador.set("Contador:")
        self.contadorLabel = Label(self.wind, textvariable = self.textContador)
        self.contadorLabel.grid(row = 8, column = 0, sticky = W, padx = 10)

        self.textProcesosSuspendidos = StringVar()
        self.textProcesosSuspendidos.set("Id siguiente suspendido:   Tamaño: ")
        self.procesosSuspendidosLabel = Label(self.wind, textvariable = self.textProcesosSuspendidos)
        self.procesosSuspendidosLabel.grid(row = 8, column = 2, sticky = W, padx = 10, columnspan=2)  

#############################################################################################################

################################## Prueba eventos teclado ###################################################

    def eventosPorTeclado(self):

        self.pruebaLabel = Label(self.wind, text = "Hola")
        self.pruebaLabel.grid(row = 3, column = 2, sticky = S)

    def teclaPulsadaP(self, event):

        self.pruebaLabel["text"] = "Programa pausado"
        self.pausado = True

    def teclaPulsadaC(self, event):

        if self.pausado == True:

            self.pruebaLabel["text"] = "Programa reanudado"
            self.pausado = False
            self.insertarFrameProceso()

            try:
                self.top.destroy()
            except:
                pass

    def teclaPulsadaI(self, event):
        
        if self.pausado != True:
            if len(cListos) > 0:
                self.pruebaLabel["text"] = "Proceso interrumpido"

                aux = cListos[0]
                cBloqueados.append(aux)
                cListos.pop(0)
                registros = self.tabla.get_children()
                try:
                    self.tabla.delete(registros[0])
                except:
                    pass
                self.limpiarTablaPaginacion()
                self.insertarTablaPaginacion()
                self.limpiarTablaBloqueados()
                self.tabla4.insert("", END, text = aux.id, values = (aux.TTB))
                self.quantumContador = self.quantum

    def teclaPulsadaE(self, event):

        if self.pausado != True:

            self.pruebaLabel["text"] = "Error en el proceso"
            self.ejecutar = True
            self.errorProceso = True
    
    def teclaPulsadaN(self, event):

        if self.pausado != True:

            self.pruebaLabel["text"] = "Nuevo proceso agregado"
            self.procesosAEjectar += 1
            proc = Proceso(self.procesosAEjectar)
            c.append(proc)

            if self.marcosDisponibles > 0 and len(c) == 1:
                if self.marcosDisponibles - c[0].paginas >= 0:
                    c[0].TLlegada = self.contador
                    cListos.append(c[0])
                    self.marcosDisponibles -= c[0].paginas
                    c.pop(0)
                    self.tabla.insert("", END, text = cListos[-1].id, values = (cListos[-1].TME, cListos[-1].TT))
                    self.limpiarTablaPaginacion()
                    self.insertarTablaPaginacion()
                
    def teclaPulsadaB(self, event):

        if self.pausado != True:

            self.pruebaLabel["text"] = "BCP"
            self.pausado = True
            for fila in cListos:                                 
                fila.TServicio = fila.TT
                fila.TRetorno = self.contador - fila.TLlegada
                fila.TEspera = fila.TRetorno - fila.TServicio
            self.ventanaBCP()     

    def teclaPulsadaS(self, event):
        
        if self.pausado != True:
            if len(cBloqueados) > 0:
                self.pruebaLabel["text"] = "Proceso suspendido"

                aux = cBloqueados[0]
                aux.TTB = 0
                self.marcosDisponibles += aux.paginas
                cSuspendidos.append(aux)
                cBloqueados.pop(0)
                registros = self.tabla4.get_children()
                try:
                    self.tabla4.delete(registros[0])
                except:
                    pass

                while self.marcosDisponibles > 0 and len(c) > 0:
                    if self.marcosDisponibles - c[0].paginas >= 0:
                        c[0].TLlegada = self.contador
                        cListos.append(c[0])
                        self.marcosDisponibles -= c[0].paginas
                        c.pop(0)
                    else:
                        break

                self.limpiarTabla()
                self.insertarTabla()
                self.limpiarTablaPaginacion()
                self.insertarTablaPaginacion()
                self.archivoSuspendidos()
            else:
                self.pruebaLabel["text"] = "Se requiere proceso bloquedo"

    def teclaPulsadaR(self, event):
        
        if self.pausado != True:
            if len(cSuspendidos) > 0:
                
                aux = cSuspendidos[0]
                if self.marcosDisponibles > 0 and len(cSuspendidos) > 0:
                    if self.marcosDisponibles - aux.paginas >= 0:
                        cBloqueados.append(aux)
                        self.marcosDisponibles -= aux.paginas
                        cSuspendidos.pop(0)
                        self.pruebaLabel["text"] = "Proceso recuperado"
                        self.limpiarTablaPaginacion()
                        self.insertarTablaPaginacion()
                        self.limpiarTablaBloqueados()
                        self.tabla4.insert("", END, text = aux.id, values = (aux.TTB))
                        self.archivoSuspendidos()
                    else:
                        self.pruebaLabel["text"] = "No hay espacio para recuperar proceso"
                 
            else:
                self.pruebaLabel["text"] = "Se requiere proceso suspendido"
        
#############################################################################################################

###################### Metodos para insertar los datos en las tablas y el frame #############################

    def insertarTabla(self):

        for fila in cListos:

            self.tabla.insert("", END, text = fila.id, values = (fila.TME, fila.TT))

    def insertarTablaPaginacion(self):

        try:
            procesoActual = 0
            procesoActualBloqueado = 0
            fila = cListos[procesoActual]
            espacio = ""
            for i in range(45):
                if i > 41:
                    if i == 42 or i == 44:
                        self.tablaPaginacion1.insert("", END, text = i, values = ("SO", "SO", "SO"))

                    if i == 43:
                        self.tablaPaginacion2.insert("", END, text = i, values = ("SO", "SO", "SO"))
                else:

                    try:    
                        try:
                            fila = cListos[procesoActual]
                            if fila == cListos[0]:
                                estado = "En ejecucion"
                            else:
                                estado = "Listo"

                            if self.primero == True:
                                estado = "Listo"

                            espacio = "4/4"

                            if fila.paginas == 1:
                                if fila.tam % 4 == 0:
                                    espacio = "4/4"
                                else:
                                    espacio = str(fila.tam % 4) + "/4"

                            if i%2 == 0:
                                
                                self.tablaPaginacion1.insert("", END, text = i, values = (espacio, fila.id, estado))

                            else:
                                self.tablaPaginacion2.insert("", END, text = i, values = (espacio, fila.id, estado))
                            fila.paginas = fila.paginas - 1
                            if fila.paginas <= 0:
                                fila.paginas = fila.paginasEstables
                                procesoActual += 1
                                self.primero = False
                        except:
                            fila = cBloqueados[procesoActualBloqueado]
                            estado = "Bloqueado"

                            espacio = "4/4"

                            if fila.paginas == 1:
                                if fila.tam % 4 == 0:
                                    espacio = "4/4"
                                else:
                                    espacio = str(fila.tam % 4) + "/4"

                            if i%2 == 0:
                                
                                self.tablaPaginacion1.insert("", END, text = i, values = (espacio, fila.id, estado))

                            else:
                                self.tablaPaginacion2.insert("", END, text = i, values = (espacio, fila.id, estado))
                            fila.paginas = fila.paginas - 1
                            if fila.paginas <= 0:
                                fila.paginas = fila.paginasEstables
                                procesoActualBloqueado += 1
                    except:
                        if i%2 == 0:
                            
                            self.tablaPaginacion1.insert("", END, text = i, values = ("", "", ""))

                        else:
                            self.tablaPaginacion2.insert("", END, text = i, values = ("", "", ""))

        except:
            pass

        for i in cListos:
            i.paginas = i.paginasEstables

        for i in cBloqueados:
            i.paginas = i.paginasEstables
                    
    def insertarFrameProceso(self):

        self.inciarProcesamiento["state"] = DISABLED
        self.botonGuardar["state"] = DISABLED

        self.wind.bind('<I>', self.teclaPulsadaI)
        self.wind.bind('<E>', self.teclaPulsadaE)
        self.wind.bind('<P>', self.teclaPulsadaP)
        self.wind.bind('<C>', self.teclaPulsadaC)
        self.wind.bind('<N>', self.teclaPulsadaN)
        self.wind.bind('<B>', self.teclaPulsadaB)
        self.wind.bind('<A>', self.teclaPulsadaP)
        self.wind.bind('<S>', self.teclaPulsadaS)
        self.wind.bind('<R>', self.teclaPulsadaR)

        if self.pausado == False:

            if self.procesoActual < self.procesosAEjectar:

                if len(cListos) > 0:

                    fila = cListos[0]
                    fila.banderaRespuesta = True
                
                else:

                    fila = Proceso(0)
                    fila.op = ""
                    fila.operando1 = ""
                    fila.operando2 = ""
                    fila.TME = 0
                    fila.TR = 0
                    fila.paginas = 0
                    fila.tam = 0

                try:
                    registros1 = self.tabla.get_children()
                    if self.tabla.item(registros1[0])['text'] == fila.id:
                        registros = self.tabla.get_children()
                        try:
                            self.tabla.delete(registros[0])
                        except:
                            pass
                except:
                    pass

                for i in cListos:
                    
                    if i.banderaRespuesta == False:
                        i.TRespuesta += 1

                fila.TR = fila.TR - 1
                fila.TT = fila.TT + 1
                self.contador = self.contador + 1
                
                if fila.TME == fila.TT:
                    self.ejecutar = True

                if self.ejecutar==False:
                    if self.quantumContador == 0:

                        self.quantumContador = self.quantum

                        if fila.id != 0:
                            if len(cListos) > 0:
                                cListos.pop(0)

                            cListos.append(fila)
                            fila = cListos[0]

                        self.limpiarTabla()
                        self.insertarTabla()
                        self.limpiarTablaPaginacion()
                        self.insertarTablaPaginacion()
                        registros = self.tabla.get_children()
                        try:
                            self.tabla.delete(registros[0])
                        except:
                            pass
                
                if self.ejecutar:
                    
                    if fila.id != 0:

                        self.procesoActual = self.procesoActual + 1

                        if self.errorProceso == True:
                            fila.resultado = "ERROR"
                            
                        else:
                            fila.resultado = fila.calcularResulrado()

                        self.tabla3.insert("", END, text = fila.id, values = (str(fila.operando1) + fila.op + str(fila.operando2), fila.resultado))
                        fila.TFinalizacion = self.contador
                        fila.TServicio = fila.TT
                        fila.TRetorno = fila.TFinalizacion - fila.TLlegada
                        fila.TEspera = fila.TRetorno - fila.TServicio
                        cFinalizados.append(fila)
                        self.marcosDisponibles += fila.paginas
                        while self.marcosDisponibles > 0 and len(c) > 0:
                            if self.marcosDisponibles - c[0].paginas >= 0:
                                c[0].TLlegada = self.contador
                                cListos.append(c[0])
                                self.marcosDisponibles -= c[0].paginas
                                c.pop(0)
                            else:
                                break
                        if len(cListos) > 0:
                            cListos.pop(0)
                        self.limpiarTabla()
                        self.limpiarTablaPaginacion()
                        self.quantumContador = self.quantum
                        self.insertarTabla()
                        self.insertarTablaPaginacion()

                        self.child_id = self.tabla3.get_children()[-1]
                        self.tabla3.focus(self.child_id)
                        self.tabla3.selection_set(self.child_id)
                        self.tabla3.see(self.child_id)

                        registros = self.tabla.get_children()
                        try:
                            self.tabla.delete(registros[0])
                        except:
                            self.textProcesosNuevos.set("Procesos nuevos:   Id siguiente:   Tamaño: ")

                    self.ejecutar = False
                    self.errorProceso = False
                
                self.limpiarTablaBloqueados()
                for bloqueado in cBloqueados:
                    
                    if bloqueado.TTB >= 5:

                        bloqueado.TTB = 0
                        cListos.append(bloqueado)
                        self.tabla.insert("", END, text = bloqueado.id, values = (bloqueado.TME, bloqueado.TT))
                        if len(cBloqueados) > 0:
                            cBloqueados.pop(0)
                        self.tabla4.insert("", END, text = bloqueado.id, values = (bloqueado.TTB))
                        registros = self.tabla4.get_children()
                        self.tabla4.delete(registros[0])
                        if len(cListos) <= 1:
                            self.quantumContador = self.quantum
                        
                    else:
                        self.tabla4.insert("", END, text = bloqueado.id, values = (bloqueado.TTB))

                    self.limpiarTablaPaginacion()
                    self.insertarTablaPaginacion()

                self.quantumContador -= 1

                self.actualizarTexto(fila)
                
                self.textContador.set("Contador: " + str(self.contador))
                try:
                    self.textProcesosNuevos.set("Procesos nuevos: " + str(len(c)) + "  Id siguiente: " + str(c[0].id) + "  Tamaño: " + str(c[0].tam))
                except:
                     self.textProcesosNuevos.set("Procesos nuevos: " + str(len(c)) + "  Id siguiente:   Tamaño: ")
                try:
                    self.textProcesosSuspendidos.set("Id siguiente suspendido: " + str(cSuspendidos[0].id) + " Tamaño: " + str(cSuspendidos[0].tam))
                except:
                     self.textProcesosSuspendidos.set("Id siguiente suspendido:   Tamaño: ")
                
                for bloqueado in cBloqueados:
                    bloqueado.TTB += 1
                self.wind.after(1000, self.insertarFrameProceso)
                
            else:

                procVacio = Proceso("")
                procVacio.op = ""
                procVacio.operando1 = ""
                procVacio.operando2 = ""
                procVacio.TME = 0
                procVacio.TR = 0
                procVacio.tam = 0
                procVacio.paginas = 0
                self.actualizarTexto(procVacio)
                self.textQuantum.set("0")
                self.ventanaFinal()

        else:

            print("programa pausado")

    def insertarTablaFinal(self):

        for fila in c:
            
            fila.resultado = fila.calcularResulrado()
            self.tabla3.insert("", END, text = fila.id, values = (str(fila.operando1) + fila.op + str(fila.operando2), fila.resultado))
        
#############################################################################################################

###################################### Limpiar tablas #######################################################

    def limpiarTabla(self):

        registros = self.tabla.get_children()
        for elemento in registros:
            self.tabla.delete(elemento)

    def limpiarTablaPaginacion(self):

        registros = self.tablaPaginacion1.get_children()
        for elemento in registros:
            self.tablaPaginacion1.delete(elemento)
        registros = self.tablaPaginacion2.get_children()
        for elemento in registros:
            self.tablaPaginacion2.delete(elemento)

    def limpiarTablaBloqueados(self):

        registros = self.tabla4.get_children()
        for elemento in registros:
            self.tabla4.delete(elemento)

    def limpiarTablaProcesados(self):

        registros = self.tabla3.get_children()
        for elemento in registros:
            self.tabla3.delete(elemento)

#############################################################################################################

###################################### Validaciones #########################################################

    def validaciones(self):

        self.msgError = ""
        valido = True

        if len(self.numeroProcesos.get()) == 0:

            valido = False
            self.msgError = "numero de procesos vacios"
            return valido

        try:

            if int(self.numeroProcesos.get()) < 1:

                valido = False
                self.msgError = "numero de procesos invalido"
                return valido
        
        except:

            valido = False
            self.msgError = "entrada invalida, digite un numero"
            return valido

        if len(self.quantumEntry.get()) == 0:

            valido = False
            self.msgError = "quantum vacio"
            return valido

        try:

            if int(self.quantumEntry.get()) < 1:

                valido = False
                self.msgError = "quantum invalido"
                return valido
        
        except:

            valido = False
            self.msgError = "entrada invalida, digite un numero"
            return valido
        
        return valido

#############################################################################################################

################################## Crea los objetos proceso y los agrega ####################################

    def agregarProcesos(self):

        if self.validaciones():

            self.inciarProcesamiento["state"] = NORMAL
            self.botonGuardar["state"] = DISABLED

            self.quantum = int(self.quantumEntry.get())
            self.quantumContador = self.quantum

            for i in range (int(self.numeroProcesos.get())):

                proc = Proceso(i+1)
                c.append(proc)

                self.mensaje["text"] = "Procesos guardados: {}".format(int(self.numeroProcesos.get()))

            self.procesosAEjectar = int(self.numeroProcesos.get())
            self.limpiarTabla()
            
            while self.marcosDisponibles > 0 and len(c) > 0:
                a = c[0].paginas
                if self.marcosDisponibles - a >= 0:
                    c[0].TLlegada = 0
                    cListos.append(c[0])
                    self.marcosDisponibles -= a
                    c.pop(0)
                else:
                    break

            self.insertarTabla()
            self.insertarTablaPaginacion()
            cListos[0].TT = -1
            cListos[0].TR += 1

        else:

            self.mensaje["text"] = "Error al guardar los procesos, {}".format(self.msgError)

        self.numeroProcesos.delete(0, END)
        self.quantumEntry.delete(0, END)

#############################################################################################################

####################### Elimina de tabla sin procesar, actualiza frame procesando ###########################

    def procesamiento(self):

        registros = self.tabla.get_children()
        self.tabla.delete(registros[0])

        self.procesosNuevos = len(c)

        self.insertarFrameProceso()
        self.limpiarTablaPaginacion()
        self.insertarTablaPaginacion()

#############################################################################################################

################################# Actualiza el texto del frame procesando ###################################

    def actualizarTexto(self, proceso):

        self.textOp.set(str(proceso.operando1) + " " + proceso.op + " " + str(proceso.operando2))
        self.textId.set(proceso.id)
        self.textTME.set(proceso.TME)
        self.textTT.set(proceso.TT)
        self.textQuantum.set(self.quantumContador)
        self.textTam.set(proceso.tam)
        self.textNumPaginas.set(proceso.paginas)

        if proceso.TR > 0:
            self.textTR.set(proceso.TR)
        else:
            self.textTR.set(0)
            self.textTT.set(0)

#############################################################################################################

###################################### Tabla final ##########################################################

    def ventanaFinal(self):

        self.top = Toplevel()
        frameFinal = LabelFrame(self.top, text = "Procesos finalizados")
        frameFinal.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = W + E + N)
        
        # Tabla
        self.tablaFinal = ttk.Treeview(frameFinal, height = self.procesosAEjectar, columns = ("op", "res", "TME", "TT", "TR", "TLlegada", "TFinalizacion", "TRetorno", "TRespuesta", "TEspera", "TServicio"))
        self.tablaFinal.grid(row = 0, column = 1)
        self.tablaFinal.heading("#0", text = "Id", anchor = CENTER)
        self.tablaFinal.column("#0", minwidth = 0, width = 50, stretch=NO)
        self.tablaFinal.heading("op", text = "Operacion", anchor = CENTER)
        self.tablaFinal.column("op", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("res", text = "Resultado", anchor = CENTER)
        self.tablaFinal.column("res", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TME", text = "TME", anchor = CENTER)
        self.tablaFinal.column("TME", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TT", text = "TT", anchor = CENTER)
        self.tablaFinal.column("TT", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TR", text = "TR", anchor = CENTER)
        self.tablaFinal.column("TR", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TLlegada", text = "Llegada", anchor = CENTER)
        self.tablaFinal.column("TLlegada", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TFinalizacion", text = "Finalizacion", anchor = CENTER)
        self.tablaFinal.column("TFinalizacion", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TRetorno", text = "Retorno", anchor = CENTER)
        self.tablaFinal.column("TRetorno", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TRespuesta", text = "Respuesta", anchor = CENTER)
        self.tablaFinal.column("TRespuesta", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TEspera", text = "Espera", anchor = CENTER)
        self.tablaFinal.column("TEspera", minwidth = 0, width = 75, stretch=NO)
        self.tablaFinal.heading("TServicio", text = "Servicio", anchor = CENTER)
        self.tablaFinal.column("TServicio", minwidth = 0, width = 75, stretch=NO)

        for fila in cFinalizados:

            self.tablaFinal.insert("", END, text = fila.id, values = (str(fila.operando1) + fila.op + str(fila.operando2) + " =", fila.resultado, fila.TME, fila.TT, fila.TR, fila.TLlegada, fila.TFinalizacion, fila.TRetorno, fila.TRespuesta, fila.TEspera, fila.TServicio))

        self.top.mainloop()

#############################################################################################################

###################################### Tabla BCP ############################################################

    def ventanaBCP(self):

        self.top = Toplevel()
        frameBCP = LabelFrame(self.top, text = "BCP")
        frameBCP.grid(row = 0, column = 1, padx = 10, pady = 5, sticky = W + E + N)
        
        # Tabla
        self.tablaBCP = ttk.Treeview(frameBCP, height = self.procesosAEjectar, columns = ("estado", "op", "res", "TME", "TT", "TR", "TRB", "TLlegada", "TFinalizacion", "TRetorno", "TRespuesta", "TEspera", "TServicio"))
        self.tablaBCP.grid(row = 0, column = 1)
        self.tablaBCP.heading("#0", text = "Id", anchor = CENTER)
        self.tablaBCP.column("#0", minwidth = 0, width = 50, stretch=NO)
        self.tablaBCP.heading("estado", text = "Estado", anchor = CENTER)
        self.tablaBCP.column("estado", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("op", text = "Operacion", anchor = CENTER)
        self.tablaBCP.column("op", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("res", text = "Resultado", anchor = CENTER)
        self.tablaBCP.column("res", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TME", text = "TME", anchor = CENTER)
        self.tablaBCP.column("TME", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TT", text = "TT", anchor = CENTER)
        self.tablaBCP.column("TT", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TR", text = "TR", anchor = CENTER)
        self.tablaBCP.column("TR", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TRB", text = "TR Bloqueado", anchor = CENTER)
        self.tablaBCP.column("TRB", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TLlegada", text = "Llegada", anchor = CENTER)
        self.tablaBCP.column("TLlegada", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TFinalizacion", text = "Finalizacion", anchor = CENTER)
        self.tablaBCP.column("TFinalizacion", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TRetorno", text = "Retorno", anchor = CENTER)
        self.tablaBCP.column("TRetorno", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TRespuesta", text = "Respuesta", anchor = CENTER)
        self.tablaBCP.column("TRespuesta", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TEspera", text = "Espera", anchor = CENTER)
        self.tablaBCP.column("TEspera", minwidth = 0, width = 75, stretch=NO)
        self.tablaBCP.heading("TServicio", text = "Servicio", anchor = CENTER)
        self.tablaBCP.column("TServicio", minwidth = 0, width = 75, stretch=NO)

        for fila in cListos:

            self.tablaBCP.insert("", END, text = fila.id, values = ("Listo", str(fila.operando1) + fila.op + str(fila.operando2) + " =", "-", fila.TME, fila.TT, fila.TR, "-", fila.TLlegada, "-", "-", fila.TRespuesta, fila.TEspera, fila.TServicio))

        for fila in cBloqueados:

            self.tablaBCP.insert("", END, text = fila.id, values = ("Bloqueado", str(fila.operando1) + fila.op + str(fila.operando2) + " =", "-", fila.TME, fila.TT, fila.TR, 5 - fila.TTB, fila.TLlegada, "-", "-", fila.TRespuesta, fila.TEspera, fila.TServicio))

        for fila in c:

            self.tablaBCP.insert("", END, text = fila.id, values = ("Nuevo", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-", "-"))

        for fila in cFinalizados:

            self.tablaBCP.insert("", END, text = fila.id, values = ("Finalizado", str(fila.operando1) + fila.op + str(fila.operando2) + " =", fila.resultado, fila.TME, fila.TT, fila.TR, "-", fila.TLlegada, fila.TFinalizacion, fila.TRetorno, fila.TRespuesta, fila.TEspera, fila.TServicio))

        self.top.mainloop()

    def archivoSuspendidos(self):
        archivo = open("suspendidos.txt", "w")
        for i in cSuspendidos:
            linea = "Id: " + str(i.id) + " Tamaño: " + str(i.tam) + " Operacion: " + str(i.operando1) + str(i.op) + str(i.operando2) + " TME: " + str(i.TME) + " TT: " + str(i.TT) + "\n"
            archivo.write(linea)
        archivo.close()

if __name__ == '__main__':

    window = Tk()
    aplicacion = Ventana(window)
    window.mainloop()
