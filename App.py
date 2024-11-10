import customtkinter
import main

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana
        self.title("Validador Regex")
        self.geometry("400x300")

        # Crear labels para indicar al usuario qué ingresar
        self.label_nombre = customtkinter.CTkLabel(master=self,
                                                 text="Ingresa la expresion Regular:")

        self.label_nombre.pack(pady=10)
        self.label_apellido = customtkinter.CTkLabel(master=self,
                                                   text="Ingresa la cadena a evaluar:")
        # Crear campos de entrada para el usuario
        self.entry_nombre = customtkinter.CTkEntry(master=self)
        self.entry_nombre.pack(pady=12)

        self.label_apellido.pack(pady=10)


        self.entry_apellido = customtkinter.CTkEntry(master=self)
        self.entry_apellido.pack(pady=12)

        # Crear botones
        self.button_enviar = customtkinter.CTkButton(master=self,
                                                   text="Enviar",
                                                   command=self.button_enviar_click)
        self.button_enviar.pack(pady=12)
        self.button_salir = customtkinter.CTkButton(master=self,
                                                  text="Salir",
                                                  command=self.destroy)
        self.button_salir.pack(pady=12)



    def button_enviar_click(self):
        # Obtener el texto ingresado por el usuario
        regex = self.entry_nombre.get()
        cadena = self.entry_apellido.get()

        result = motor.verificar_str(regex, cadena)
        print(f"\nResultado del match: {result}\n")

        # Crear una nueva ventana para mostrar los datos
        self.ventana_datos = customtkinter.CTkToplevel(self)
        self.ventana_datos.tkraise()
        self.ventana_datos.title("Datos Ingresados")
        self.ventana_datos.geometry("300x200")

        if result is None:
            label_datos = customtkinter.CTkLabel(self.ventana_datos, text="Error, la expresion regular es incorrecta")
        else:
            # Crear un label para mostrar los datos
            label_datos = customtkinter.CTkLabel(self.ventana_datos,
                                                 text=f"\nNotacion Postfix: {motor.postfix}\n"
                                                      f"\nCadena: {cadena}\n"
                                                      f"\nResultado del match: {result}\n")
        label_datos.pack(pady=20)

        # Crear un botón para volver a la ventana principal
        button_volver = customtkinter.CTkButton(self.ventana_datos,
                                                text="Volver",
                                                command=self.volver_a_principal)
        button_volver.pack(pady=12)
        # Ocultar la ventana principal temporalmente
        self.withdraw()

    def volver_a_principal(self):
        # Mostrar la ventana principal
        self.deiconify()
        # Cerrar la ventana secundaria
        self.ventana_datos.destroy()


if __name__ == "__main__":
    motor = main.MotorRegex()


    app = App()
    app.mainloop()