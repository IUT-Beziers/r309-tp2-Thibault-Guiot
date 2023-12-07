import tkinter as tk
from PIL import Image, ImageTk

class PacketTracerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulateur Packet Tracer")

        # Création du cadre jaune autour du canevas
        self.canvas_frame = tk.Frame(root, bg="yellow")
        self.canvas_frame.grid(row=0, column=0, sticky="nsew")  # Expansion pour remplir l'espace

        # Création du canevas dans le cadre
        self.create_canvas()

        # Création du menu d'outils
        self.create_tools_menu()

        # Titre "Interface de Configuration" dans le menu de configuration
        self.create_config_title()

        # Expansion du cadre jaune pour qu'il prenne tout l'écran
        root.grid_rowconfigure(0, weight=1)
        root.columnconfigure(0, weight=1)

        self.counter = {
            "Router": 0,
            "Switch": 0,
            "Client": 0
        }

        # Dictionnaire pour lier les images et les textes correspondants
        self.image_text = {}

    def create_canvas(self):
        # Création du canevas dans le cadre jaune
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(expand=True, fill="both")  # Expansion pour remplir le canevas
        self.canvas_frame.grid_rowconfigure(0, weight=1)
        self.canvas_frame.grid_columnconfigure(0, weight=1)

        # Ajout de gestionnaires d'événements pour le glisser-déposer
        self.canvas.bind("<ButtonPress-1>", self.on_drag_start)
        self.canvas.bind("<B1-Motion>", self.on_drag_motion)

        # Dictionnaire pour stocker les informations de glisser-déposer pour chaque objet
        self.drag_data = {}

    def create_tools_menu(self):
        # Création du cadre pour le menu d'outils
        self.tools_frame = tk.Frame(self.root, bg="#13CACA")
        self.tools_frame.grid(row=1, column=0, sticky="ew")  # Positionnement et expansion du cadre

        # Création de l'étiquette du menu "Outils"
        self.create_menu_label("Outils")

        image_size = (60, 60)
        router_img = self.create_resized_image("Image/Router.png", image_size)
        switch_img = self.create_resized_image("Image/Switch.png", image_size)
        computer_img = self.create_resized_image("Image/Client.png", image_size)

        # Création des étiquettes pour les outils avec les images redimensionnées
        self.create_tool_label(router_img, "Router")
        self.create_tool_label(switch_img, "Switch")
        self.create_tool_label(computer_img, "Client")

    def create_menu_label(self, text):
        # Création d'une étiquette avec le texte du menu
        menu_label = tk.Label(self.tools_frame, text=text, bg="#13CACA", font=("Helvetica", 12, "bold"))
        menu_label.pack(fill="x")  # Expansion horizontale de l'étiquette

    def create_tool_label(self, img, tool_type):
        # Création d'une étiquette pour un outil avec une image
        tool_label = tk.Label(self.tools_frame, image=img)
        tool_label.image = img
        tool_label.pack(side=tk.LEFT, padx=20)  # Positionnement à gauche avec une marge
        tool_label.bind("<ButtonPress-1>", lambda event, img=img, tool_type=tool_type: self.add_to_config(event, img, tool_type))

    def create_resized_image(self, image_path, size):
        # Chargement et redimensionnement d'une image
        original_image = Image.open(image_path)
        resized_image = original_image.resize(size, Image.BILINEAR)
        return ImageTk.PhotoImage(resized_image)

    def add_to_config(self, event, img, tool_type):
        # Ajout d'une copie de l'image au menu de configuration
        x, y = self.canvas.winfo_reqwidth() / 2, 200  # Coordonnées au centre du menu
        self.counter[tool_type] += 1
        image_name = f"{tool_type} {self.counter[tool_type]}"  # Nom unique pour chaque élément

        config_image = self.canvas.create_image(x, y, image=img, tags="config_image")
        text_label = self.canvas.create_text(x, y + 40, text=image_name, font=("Helvetica", 10), fill="black", tags="config_text")

        # Sauvegarde des informations pour le glisser-déposer
        self.drag_data[config_image] = {'x': x, 'y': y, 'img': img, 'name': image_name}

        # Associer l'image et le texte correspondant dans le dictionnaire
        self.image_text[config_image] = text_label

    def create_config_title(self):
        # Création d'un cadre pour le titre dans le menu de configuration
        title_frame = tk.Frame(self.canvas_frame, bg="#13CACA")
        title_frame.place(relx=0.5, rely=0.03, anchor="n")  # Placement au centre du canevas

        # Création de l'étiquette du titre avec une police légèrement plus grande
        title_label = tk.Label(title_frame, text="Interface de Configuration", font=("Helvetica", 14, "bold"))
        title_label.pack()  # Expansion automatique de l'étiquette

    def on_drag_start(self, event):
        # Trouver l'objet sous le pointeur de la souris
        x, y = event.x, event.y
        item = self.canvas.find_closest(x, y)[0]

        # Sauvegarder les informations pour le glisser-déposer
        self.drag_data['item'] = item
        self.drag_data['x'] = x
        self.drag_data['y'] = y

    def on_drag_motion(self, event):
        # Calculer le déplacement
        x, y = event.x, event.y
        dx = x - self.drag_data['x']
        dy = y - self.drag_data['y']

        # Déplacer l'objet et le texte associé
        self.canvas.move(self.drag_data['item'], dx, dy)
        text_item = self.image_text.get(self.drag_data['item'])
        if text_item:
            self.canvas.move(text_item, dx, dy)

        # Mettre à jour les coordonnées de départ pour le prochain mouvement
        self.drag_data['x'] = x
        self.drag_data['y'] = y

if __name__ == "__main__":
    root = tk.Tk()
    app = PacketTracerApp(root)
    root.mainloop()
