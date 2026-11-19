# interfaz.py
# Interfaz gráfica en Tkinter para el Sistema Integral de Gestión Software FJ

import tkinter as tk
from tkinter import ttk, messagebox
from gestor import SistemaSoftwareFJ
from modelos import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import ErrorSoftwareFJ


class InterfazSoftwareFJ:
    """Interfaz gráfica de escritorio conectada al controlador SistemaSoftwareFJ."""

    def __init__(self, root):
        self.root = root
        self.root.title("Software FJ - Sistema Integral de Gestión (Fase 4 UNAD)")
        self.root.geometry("950x620")
        self.root.configure(bg="#f4f6f9")

# Instancia del sistema principal (maneja listas en memoria y archivo .log)
        self.sistema = SistemaSoftwareFJ()

# Cargar datos iniciales de prueba para visualizar funcionamiento inmediato
        self._cargar_datos_demo()

        self._construir_encabezado()
        self._construir_tarjetas_resumen()
        self._construir_pestanas()
        self._construir_barra_estado()
        self.actualizar_todo()

    def _cargar_datos_demo(self):
        """Carga registros iniciales válidos en memoria."""
        self.sistema.registrar_cliente("C001", "Maicol Martínez", "mamartinezv2@unadvirtual.edu.co", "3105551234")
        self.sistema.registrar_servicio(ReservaSala("S001", "Sala Innovación Norte", 80000, 15))
        self.sistema.registrar_servicio(AlquilerEquipo("E001", "Workstation Dell Precision", 35000, "Computador"))
        self.sistema.registrar_servicio(AsesoriaEspecializada("A001", "Arquitectura Cloud", 120000, "Software"))

    def _construir_encabezado(self):
        header = tk.Frame(self.root, bg="#1e293b", height=55)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="Software FJ  |  Gestión de Clientes, Servicios y Reservas",
            bg="#1e293b",
            fg="white",
            font=("Segoe UI", 13, "bold"),
            padx=20
        ).pack(side="left", pady=12)

        tk.Button(
            header,
            text="▶ Ejecutar Simulación (12 Pruebas)",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 9, "bold"),
            relief="flat",
            padx=12,
            pady=5,
            cursor="hand2",
            command=self.ejecutar_pruebas_automaticas
        ).pack(side="right", padx=20, pady=10)

    def _construir_tarjetas_resumen(self):
        frame_cards = tk.Frame(self.root, bg="#f4f6f9", pady=12, padx=20)
        frame_cards.pack(fill="x")

        self.lbl_total_clientes = self._crear_tarjeta(frame_cards, "CLIENTES", "0", 0)
        self.lbl_total_servicios = self._crear_tarjeta(frame_cards, "SERVICIOS", "0", 1)
        self.lbl_total_reservas = self._crear_tarjeta(frame_cards, "RESERVAS", "0", 2)
        self.lbl_ultimo_costo = self._crear_tarjeta(frame_cards, "ÚLTIMO CÁLCULO", "$0", 3)

        for i in range(4):
            frame_cards.columnconfigure(i, weight=1)

    def _crear_tarjeta(self, padre, titulo, valor_inicial, columna):
        card = tk.Frame(padre, bg="white", bd=1, relief="solid", padx=15, pady=10)
        card.grid(row=0, column=columna, padx=6, sticky="ew")

        tk.Label(card, text=titulo, bg="white", fg="#64748b", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        lbl_valor = tk.Label(card, text=valor_inicial, bg="white", fg="#0f172a", font=("Segoe UI", 16, "bold"))
        lbl_valor.pack(anchor="w", pady=(2, 0))
        return lbl_valor

    def _construir_pestanas(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill="both", expand=True, padx=20, pady=(0, 10))

        self.tab_clientes = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.tab_servicios = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.tab_reservas = tk.Frame(self.notebook, bg="white", padx=15, pady=15)
        self.tab_logs = tk.Frame(self.notebook, bg="white", padx=15, pady=15)

        self.notebook.add(self.tab_clientes, text="  Clientes  ")
        self.notebook.add(self.tab_servicios, text="  Servicios  ")
        self.notebook.add(self.tab_reservas, text="  Reservas  ")
        self.notebook.add(self.tab_logs, text="  Registro de Logs (.log)  ")

        self._armar_tab_clientes()
        self._armar_tab_servicios()
        self._armar_tab_reservas()
        self._armar_tab_logs()

# PESTAÑA CLIENTES 
    def _armar_tab_clientes(self):
        izq = tk.Frame(self.tab_clientes, bg="white", width=290)
        izq.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(izq, text="Nuevo Cliente", bg="white", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        self.ent_cli_id = self._campo(izq, "ID / Documento:")
        self.ent_cli_nombre = self._campo(izq, "Nombre completo:")
        self.ent_cli_correo = self._campo(izq, "Email:")
        self.ent_cli_tel = self._campo(izq, "Teléfono:")

        tk.Button(
            izq, text="Registrar cliente", bg="#1e293b", fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", pady=7, cursor="hand2",
            command=self.accion_registrar_cliente
        ).pack(fill="x", pady=(12, 5))

        tk.Button(
            izq, text="Limpiar", bg="#e2e8f0", fg="#1e293b",
            font=("Segoe UI", 9), relief="flat", pady=5, cursor="hand2",
            command=lambda: [e.delete(0, tk.END) for e in (self.ent_cli_id, self.ent_cli_nombre, self.ent_cli_correo, self.ent_cli_tel)]
        ).pack(fill="x")

# Tabla derecha
        der = tk.Frame(self.tab_clientes, bg="white")
        der.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Nombre", "Email", "Teléfono")
        self.tree_clientes = ttk.Treeview(der, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_clientes.heading(c, text=c)
            self.tree_clientes.column(c, width=130)
        self.tree_clientes.pack(fill="both", expand=True)

    # PESTAÑA SERVICIOS
    def _armar_tab_servicios(self):
        izq = tk.Frame(self.tab_servicios, bg="white", width=290)
        izq.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(izq, text="Nuevo Servicio", bg="white", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        tk.Label(izq, text="Tipo de servicio:", bg="white", font=("Segoe UI", 9)).pack(anchor="w")
        self.cmb_srv_tipo = ttk.Combobox(izq, values=["Sala", "Equipo", "Asesoría"], state="readonly")
        self.cmb_srv_tipo.current(0)
        self.cmb_srv_tipo.pack(fill="x", pady=(2, 8))

        self.ent_srv_id = self._campo(izq, "ID Servicio (ej. S002):")
        self.ent_srv_nombre = self._campo(izq, "Nombre del servicio:")
        self.ent_srv_tarifa = self._campo(izq, "Tarifa por hora ($):")
        self.ent_srv_extra = self._campo(izq, "Capacidad / Tipo / Área:")

        tk.Button(
            izq, text="Registrar servicio", bg="#1e293b", fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", pady=7, cursor="hand2",
            command=self.accion_registrar_servicio
        ).pack(fill="x", pady=(12, 5))

        der = tk.Frame(self.tab_servicios, bg="white")
        der.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Servicio", "Tarifa/h", "Estado", "Detalle")
        self.tree_servicios = ttk.Treeview(der, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_servicios.heading(c, text=c)
            self.tree_servicios.column(c, width=110)
        self.tree_servicios.pack(fill="both", expand=True)

 # PESTAÑA RESERVAS
    def _armar_tab_reservas(self):
        izq = tk.Frame(self.tab_reservas, bg="white", width=290)
        izq.pack(side="left", fill="y", padx=(0, 15))

        tk.Label(izq, text="Gestionar Reserva", bg="white", font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(0, 10))

        self.ent_res_id = self._campo(izq, "ID Reserva (ej. R001):")
        self.ent_res_cli = self._campo(izq, "ID Cliente (ej. C001):")
        self.ent_res_srv = self._campo(izq, "ID Servicio (ej. S001):")
        self.ent_res_horas = self._campo(izq, "Duración (horas):")
        self.ent_res_desc = self._campo(izq, "Descuento (0.0 a 1.0):", "0.0")

        tk.Button(
            izq, text="Confirmar Reserva", bg="#16a34a", fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", pady=7, cursor="hand2",
            command=self.accion_crear_reserva
        ).pack(fill="x", pady=(10, 5))

        tk.Button(
            izq, text="Cancelar Reserva Seleccionada", bg="#dc2626", fg="white",
            font=("Segoe UI", 9, "bold"), relief="flat", pady=6, cursor="hand2",
            command=self.accion_cancelar_reserva
        ).pack(fill="x")

        der = tk.Frame(self.tab_reservas, bg="white")
        der.pack(side="right", fill="both", expand=True)

        cols = ("ID", "Estado", "Cliente", "Servicio", "Horas", "Total")
        self.tree_reservas = ttk.Treeview(der, columns=cols, show="headings", height=12)
        for c in cols:
            self.tree_reservas.heading(c, text=c)
            self.tree_reservas.column(c, width=95)
        self.tree_reservas.pack(fill="both", expand=True)

# PESTAÑA LOGS
    def _armar_tab_logs(self):
        top = tk.Frame(self.tab_logs, bg="white")
        top.pack(fill="x", pady=(0, 8))

        tk.Label(top, text="Historial en tiempo real (eventos_sistema.log)", bg="white", font=("Segoe UI", 10, "bold")).pack(side="left")
        tk.Button(
            top, text="Refrescar Log", bg="#1e293b", fg="white",
            font=("Segoe UI", 8, "bold"), relief="flat", padx=10, pady=4,
            command=self.cargar_archivo_log
        ).pack(side="right")

        self.txt_logs = tk.Text(self.tab_logs, bg="#0f172a", fg="#e2e8f0", font=("Consolas", 9), wrap="none")
        self.txt_logs.pack(fill="both", expand=True)

    def _campo(self, padre, etiqueta, valor_defecto=""):
        tk.Label(padre, text=etiqueta, bg="white", font=("Segoe UI", 9)).pack(anchor="w")
        entry = tk.Entry(padre, font=("Segoe UI", 9), relief="solid", bd=1)
        if valor_defecto:
            entry.insert(0, valor_defecto)
        entry.pack(fill="x", pady=(2, 7), ipady=3)
        return entry

    def _construir_barra_estado(self):
        self.lbl_estado = tk.Label(
            self.root, text="Sistema Software FJ iniciado correctamente.",
            bg="#e2e8f0", fg="#166534", font=("Segoe UI", 9, "bold"), anchor="w", padx=15, pady=5
        )
        self.lbl_estado.pack(fill="x", side="bottom")

    def notificar(self, mensaje, es_error=False):
        color = "#b91c1c" if es_error else "#166534"
        self.lbl_estado.config(text=mensaje, fg=color)
        if es_error:
            messagebox.showwarning("Excepción Controlada - Software FJ", mensaje)

# ACCIONES DE BOTONES
    def accion_registrar_cliente(self):
        id_c = self.ent_cli_id.get()
        nom = self.ent_cli_nombre.get()
        cor = self.ent_cli_correo.get()
        tel = self.ent_cli_tel.get()

        cliente = self.sistema.registrar_cliente(id_c, nom, cor, tel)
        if cliente:
            self.notificar(f"Cliente registrado: {cliente.obtener_resumen()}")
        else:
            self.notificar(f"Error controlado al registrar cliente '{id_c}'. Revise la pestaña de Logs.", es_error=True)
        self.actualizar_todo()

    def accion_registrar_servicio(self):
        tipo = self.cmb_srv_tipo.get()
        id_s = self.ent_srv_id.get()
        nom = self.ent_srv_nombre.get()
        extra = self.ent_srv_extra.get()

        try:
            tarifa = float(self.ent_srv_tarifa.get())
            if tipo == "Sala":
                srv = ReservaSala(id_s, nom, tarifa, int(extra))
            elif tipo == "Equipo":
                srv = AlquilerEquipo(id_s, nom, tarifa, extra)
            else:
                srv = AsesoriaEspecializada(id_s, nom, tarifa, extra)

            res = self.sistema.registrar_servicio(srv)
            if res:
                self.notificar(f"Servicio registrado: {srv.obtener_resumen()}")
            else:
                self.notificar(f"No se pudo registrar el servicio '{id_s}'.", es_error=True)
        except ValueError as e:
            self.sistema.log.error(f"Error de conversión numérica en servicio '{id_s}': {e}")
            self.notificar("La tarifa y la capacidad (en Salas) deben ser valores numéricos válidos.", es_error=True)
        except ErrorSoftwareFJ as e:
            self.sistema.log.error(f"Error al instanciar servicio '{id_s}': {e}")
            self.notificar(str(e), es_error=True)

        self.actualizar_todo()

    def accion_crear_reserva(self):
        id_r = self.ent_res_id.get()
        id_c = self.ent_res_cli.get()
        id_s = self.ent_res_srv.get()

        try:
            horas = float(self.ent_res_horas.get())
            desc = float(self.ent_res_desc.get())
            reserva = self.sistema.crear_y_confirmar_reserva(id_r, id_c, id_s, horas, descuento=desc)
            if reserva:
                self.lbl_ultimo_costo.config(text=f"${reserva.costo_total:,.0f}")
                self.notificar(f"Reserva confirmada: {reserva.obtener_detalle()}")
            else:
                self.notificar(f"Reserva '{id_r}' rechazada por validación o disponibilidad. Revise Logs.", es_error=True)
        except ValueError as e:
            self.sistema.log.error(f"Datos no numéricos en reserva '{id_r}': {e}")
            self.notificar("Las horas y el descuento deben ser números válidos.", es_error=True)

        self.actualizar_todo()

    def accion_cancelar_reserva(self):
        seleccion = self.tree_reservas.selection()
        if not seleccion:
            self.notificar("Seleccione una reserva de la tabla para cancelar.", es_error=True)
            return
        id_r = self.tree_reservas.item(seleccion[0])["values"][0]
        self.sistema.cancelar_reserva(str(id_r))
        self.notificar(f"Proceso de cancelación ejecutado para reserva '{id_r}'.")
        self.actualizar_todo()

    def ejecutar_pruebas_automaticas(self):
        """Ejecuta casos válidos e inválidos para demostrar resiliencia y llenar el log."""
        self.sistema.registrar_cliente("C002", "Laura Gómez", "laura@empresa.com", "3209876543")
        self.sistema.registrar_cliente("C003", "Error Prueba", "sin_arroba.com", "12")
        r1 = self.sistema.crear_y_confirmar_reserva("R001", "C001", "S001", 3)
        if r1:
            self.lbl_ultimo_costo.config(text=f"${r1.costo_total:,.0f}")
# Intentar reservar servicio ocupado y horas inválidas (encadenamiento de excepciones)
        self.sistema.crear_y_confirmar_reserva("R002", "C002", "S001", 2)
        self.sistema.crear_y_confirmar_reserva("R003", "C002", "E001", 1)
        self.actualizar_todo()
        messagebox.showinfo(
            "Simulación Completada",
            "Se ejecutaron operaciones válidas y fallidas sin detener la aplicación.\nRevise la pestaña 'Registro de Logs (.log)'."
        )

# ACTUALIZACIÓN VISUAL
    def actualizar_todo(self):
        self.lbl_total_clientes.config(text=str(len(self.sistema.clientes)))
        self.lbl_total_servicios.config(text=str(len(self.sistema.servicios)))
        self.lbl_total_reservas.config(text=str(len(self.sistema.reservas)))

 # Tabla clientes
        for item in self.tree_clientes.get_children():
            self.tree_clientes.delete(item)
        for c in self.sistema.clientes:
            self.tree_clientes.insert("", "end", values=(c.id_entidad, c.nombre, c.correo, c.telefono))

 # Tabla servicios
        for item in self.tree_servicios.get_children():
            self.tree_servicios.delete(item)
        for s in self.sistema.servicios:
            est = "Disponible" if s.disponible else "Ocupado"
            self.tree_servicios.insert("", "end", values=(s.id_entidad, s.nombre, f"${s._tarifa_hora:,.0f}", est, s.describir_servicio()))

# Tabla reservas
        for item in self.tree_reservas.get_children():
            self.tree_reservas.delete(item)
        for r in self.sistema.reservas:
            self.tree_reservas.insert("", "end", values=(r.id_reserva, r.estado, r.cliente.nombre, r.servicio.nombre, f"{r.horas}h", f"${r.costo_total:,.0f}"))

        self.cargar_archivo_log()

    def cargar_archivo_log(self):
        self.txt_logs.delete("1.0", tk.END)
        try:
            with open("eventos_sistema.log", "r", encoding="utf-8") as f:
                self.txt_logs.insert(tk.END, f.read())
                self.txt_logs.see(tk.END)
        except FileNotFoundError:
            self.txt_logs.insert(tk.END, "Aún no se ha generado el archivo eventos_sistema.log.")


if __name__ == "__main__":
    root = tk.Tk()
    app = InterfazSoftwareFJ(root)
    root.mainloop()