# Program spustí hru Keyboard King, která se zaměřuje na hráčovy reflexy
# autor: Lukáš Lacina 4.B <lacinal@jirovcovka.net>

import tkinter
import random
from tkinter import messagebox
from PIL import Image, ImageTk

class KeyboardKing(tkinter.Tk):
    def __init__(self, main_title, width, height):
        super().__init__()

        # Nastavení atributů
        self.width = width
        self.height = height
        self.score = 0
        self.best_score = 0
        self.rounds_left = 10
        self.game_speed = 50
        self.circle = None
        self.y_position = 0
        self.game_active = False
        self.end_game_text = None

        # Nastavení okna
        self.title(main_title)
        self.geometry(f"{width}x{height}")

        # GUI
        # Vytvoření horního panelu s pozadím
        self.top_frame = tkinter.Frame(self, background="#4CAF50")  # Změna barvy pozadí na zelenou
        self.top_frame.pack(fill=tkinter.X)

        # Vytvoření labelu pro spuštění hry
        self.start_label = tkinter.Label(self.top_frame, text="Spustit hru", font=("Clarendon", 30, "bold"), cursor="hand2", background="#4CAF50")
        self.start_label.pack(pady=10)
        self.start_label.bind("<Button-1>", self.start_game)  # Spuštění hry po kliknutí na label

        # Nastavení menu baru
        self.menu_bar = tkinter.Menu(self)
        self.config(menu=self.menu_bar)

        # Vytvoření složky "Nápověda" a "O hře"
        help_menu = tkinter.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label="Nápověda", command=self.show_help)
        help_menu.add_command(label="O hře", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

        # Nastavení klávesových událostí
        self.keys = ["S", "D", "F", "J", "K", "L"]
        self.bind("<KeyPress>", self.key_pressed)

        # Rozložení plátna
        self.score_label = tkinter.Label(self, text=f"{self.rounds_left}:{self.score}", font=("Clarendon", 30, "bold"))
        self.canvas = tkinter.Canvas(self, width=width, height=height - 200, background="#F2F2F2")  # Nová výška plátna
        self.rectangles = self.create_rectangles()

        self.score_label.pack()
        self.canvas.pack()

        # Label pro zobrazení nejlepšího skóre
        self.best_score_label = tkinter.Label(self, text=f"Nejlepší skóre: {self.best_score}", font=("Clarendon", 20, "bold"))
        self.best_score_label.pack(side=tkinter.LEFT, padx=20, pady=10)

    def create_rectangles(self):
        rectangles = []
        for i in range(len(self.keys)):
            rectangle = self.canvas.create_rectangle(50 + i * 150, 650, 120 + i * 150, 680, outline="black", fill="gray")
            rectangles.append(rectangle)        
        return rectangles
    
    def start_game(self, event=None):
        # Spustí hru pokud již není puštěná
        if not self.game_active:
            self.game_active = True  # Nastavení stavu hry na aktivní

            # Resetování hry
            self.score = 0
            self.rounds_left = 10
            self.game_speed = 50
            self.update_score()
            self.hide_end_game_text()
            self.next_round()
        
    def update_score(self):
        # Aktualizuje scóre
        self.score_label.config(text=f"{self.score}:{self.rounds_left}")
        # Aktualizace nejlepšího skóre, pokud je aktuální skóre vyšší
        if self.score > self.best_score:
            self.best_score = self.score
            self.best_score_label.config(text=f"Nejlepší skóre: {self.best_score}")

    def next_round(self):
        # Spustí sled údálostí na začátku každého kola

        # Odstraní padající kruh
        if self.circle:
            self.canvas.delete(self.circle)

        # Kontrola, zda hra neskončila
        if self.rounds_left < 1:
            self.end_game()
            return

        # Snížení zbývajícího počtu kol
        self.rounds_left -= 1

        # Náhodné zvolení místa, kde se objeví kruh
        self.random_key()
        self.y_position = 0

        # Vytvoření kruhu
        self.create_falling_circle()

        # Zrychlení hry
        self.game_speed = max(10, self.game_speed - 50)  # Každé kolo zrychlí hru snížením rychlosti o 50 ms, minimální rychlost je 10 ms

        # Zahájení pohybu kruhu
        self.move_circle()

        # Aktualizace scóre
        self.update_score()

    def random_key(self):
        # Výběr náhodného tlačítka na zmáčknutí
        self.current_key = random.choice(self.keys)
        self.highlight_key(self.current_key)

    def highlight_key(self, key):
        # Zvýraznění správného obdelníku pro stisk
        # Odstranění zvýraznění předchozího obdelníku
        for rectangle in self.rectangles:
            self.canvas.itemconfig(rectangle, fill="gray")
        # Zvýraznění nového obdelníku
        self.rec_index = self.keys.index(key)
        self.canvas.itemconfig(self.rectangles[self.rec_index], fill="red")

    def create_falling_circle(self):
        # Vytvoření kruhu na náhodně zvoleném místě
        index = self.keys.index(self.current_key)
        x_position = 100 + index * 150
        self.circle = self.canvas.create_oval(x_position - 15, self.y_position, x_position + 15, self.y_position + 30, fill="black")

    def key_pressed(self, event):
        # Funkce tlačítek S, D, F, J, K, L
        # Kontrola, zda byla stisknuta správná klávesa
        if event.keysym.upper() == self.current_key:
            self.score += 1
            self.update_score()
        else:
            # Změna barvy nesprávného obdélníku na černou po dobu 2 sekund
            self.canvas.itemconfig(self.rectangles[self.keys.index(self.current_key)], fill="black")
            self.after(2000, self.reset_rectangle_color, self.keys.index(self.current_key))

            # Omezení funkce kláves na 2 sekundy
            self.unbind("<KeyPress>")
            self.after(2000, self.rebind_key)
            return

        # Změna y-souřadnice pro změny polohy kolečka a následné odstranění kolečka
        if self.circle:
            position = self.canvas.coords(self.circle)
            self.y_position = position[1]
            self.canvas.delete(self.circle)
        
        #Změna tlačítka pro zmáčknutí a vytvoření kolečka
        self.random_key()
        self.create_falling_circle()

    def reset_rectangle_color(self, index):
        # Obnoví barvu obdélníku na červenou
        self.canvas.itemconfig(self.rectangles[index], fill="red")

    def rebind_key(self):
        # Znovu aktivuje používání kláves
        self.bind("<KeyPress>", self.key_pressed)

    def move_circle(self):
        # Pohyb kruhu směrem dolu
        if self.circle:
            self.canvas.move(self.circle, 0, 5)  # Posun dolu o 5 jednotek
            circle_pos = self.canvas.coords(self.circle)

            # Zkontrolujte, zda kruh dosáhl dna, pokud ano, soustí se nové kolo
            if circle_pos[3] < self.height - 100:
                self.after(self.game_speed, self.move_circle)
            else:
                self.next_round()

    def end_game(self):
        # Zobrazení textu "Konec hry!"
        if self.end_game_text is None:
            self.end_game_text = self.canvas.create_text(self.width // 2, self.height // 2, text="Konec hry!", font=("Clarendon", 30, "bold"))
        else:
            self.canvas.itemconfig(self.end_game_text, state="normal")  # Zobrazí text znovu
        self.unbind("<KeyPress>")
        self.game_active = False  # Nastavení stavu hry na neaktivní

    def hide_end_game_text(self):
        #Skryje text, který oznamuje konec hry
        if self.end_game_text is not None:
            self.canvas.itemconfig(self.end_game_text, state="hidden") 

    def show_help(self):
        # Zobrazení okna s nápovědou
        help_window = tkinter.Toplevel(self)
        help_window.title("Nápověda")
        help_window.geometry("600x300")

        help_text = "Tato hra testuje vaši rychlost a přesnost při stisknutí kláves.\n\n" \
                    "Cílem je stisknout správnou klávesu, kterou určuje červený obdelník.\n" \
                    "Hra se ovládá klávesami S, D, F, J, K, L. Každá klávesa symbolizuje jeden obdelník v dolní části programu.\n\n" \
                    "Za každý správný stisk získáte bod.\n\n" \
                    "Pokud zmáčknete špatné tlačítko, 2 sekundy nemůžete stisknout jiné.\n\n" \
                    "Hraje se celkem 10 kol a každé kolo se zrychluje."
        
        label = tkinter.Label(help_window, text=help_text, padx=20, pady=20)
        label.pack()

    def show_about(self):
        # Zobrazení okna "O hře"
        about_window = tkinter.Toplevel(self)
        about_window.title("O hře")
        about_window.geometry("400x400")

        about_text = "Verze: 1.0\n\nAutor: Lukáš Lacina"
        
        # Zobrazení textu
        label = tkinter.Label(about_window, text=about_text, padx=20, pady=20)
        label.pack()

        # Vytvoření obrázku
        image_path = r"c:\Users\uzivatel\Desktop\KeyboardKing\author.jpg"
        max_size = (200, 200)
        image = Image.open(image_path)
        image.thumbnail(max_size)
        photo = ImageTk.PhotoImage(image)

        # Zobrazení obrázku
        avatar_label = tkinter.Label(about_window, image=photo)
        avatar_label.image = photo 
        avatar_label.pack(pady=10)

    def run(self):
        """
        Spuštění hlavní smyčky.
        """
        self.mainloop()

# Spuštění hry
if __name__ == "__main__":
    app = KeyboardKing("Keyboard King", 900, 900)
    app.run()
