import tkinter as tk
from PIL import Image, ImageTk
import os
import random

def on_fullscreen(event=None):
    root.attributes("-fullscreen", True)
    root.bind("<Escape>", off_fullscreen)

def off_fullscreen(event=None):
    root.attributes("-fullscreen", False)
    root.bind("<F11>", on_fullscreen)

def read_number_from_file(filepath):
    """ Citește numărul din fișierul text. """
    with open(filepath, 'r') as file:
        number = file.read()
        return number  # Asigură-te că numărul este între 0 și 100

def update_progress_bar(number):
    """ Actualizează bara de progres în funcție de numărul citit. """
    canvas.delete("progress")
    bar_width = (number.count('1')*25 / 100) * root.winfo_screenwidth()
    canvas.create_rectangle(0, 0, bar_width, 40, fill="green", outline="green", tags="progress")

def write_number_to_file(filepath, vector):
    """ Scrie numărul în fișierul text. """
    with open(filepath, 'w') as file:
        file.write(vector)

def reset_number():
    """ Resetează numărul din fișier la 0 și actualizează bara de progres. """
    write_number_to_file("numar.txt", "0 0 0 0")
    update_progress_bar("0 0 0 0")
    show_main_buttons()

def close_application():
    root.destroy()

def show_quiz():
    """ Afișează un quiz cu întrebări. """
    global current_question_index, score, selected_questions

    all_questions = [
        {"question": "Derivata unei funcții într-un punct semnifică _______ cu care se modifică functia", "answers": ["rata", "inaltimea", "distanta fata de axa"], "correct": "rata"},
        {"question": "Functia care are derivata egala cu ea insasi este:", "answers": ["x^n", "ln x", "e^x"], "correct": "e^x"},
        {"question": "Derivata functiei sin x este:", "answers": ["sin x", "cos x", "tg x"], "correct": "cos x"},
        {"question": "Derivata functiei cos x este:", "answers": ["sin x", "-sin x", "-cos x"], "correct": "-sin x"},
        {"question": "Derivata functiei ln x este:", "answers": ["e^x", "1/x", "x ln x"], "correct": "1/x"},
        {"question": "Derivata functiei a^x este:", "answers": ["a^x * ln a", "a ln x", "ln x"], "correct": "a^x * ln a"},
        {"question": "Derivata functiei x^n este:", "answers": ["n * x ^ (n-1)", "x ^ (n-1)", "n * x"], "correct": "n * x ^ (n-1)"},
        {"question": "A doua derivată a poziției unui obiect în raport cu timpul este:", "answers": ["acceleratia", "viteza", "radicalul pozitiei"], "correct": "acceleratia"},
        {"question": "Care dintre urmatoarele variante arata derivata a doua", "answers": ["convexitatea", "cresterea", "schimbarea"], "correct": "convexitatea"},
        {"question": "Cand derivata a doua este negativa, functia este", "answers": ["convexa", "concava", "constanta"], "correct": "concava"},
        {"question": "Cand derivata a doua este pozitiva, functia este", "answers": ["convexa", "concava", "constanta"], "correct": "convexa"},
        {"question": "Cand derivata a doua este pozitiva, functia nula", "answers": ["convexa", "concava", "constanta"], "correct": "constanta"},
        {"question": "Graficul unei funcții f din A în B este mulțimea perechilor ordonate", "answers": ["(x,f(x))", "(f(x),x)", "(x,x(f))"], "correct": "(x,f(x))"},
        {"question": "Care este derivata functiei f(x)=3x^4", "answers": ["3x^3", "12x^3", "4x^3"], "correct": "12x^3"},
        {"question": "Care este derivata functiei f(x)=3sin x", "answers": ["3cos x", "-3sin x", "-3cos x"], "correct": "3cos x"}
    ]

    # Selectăm 7 întrebări random
    selected_questions = random.sample(all_questions, 7)
    current_question_index = 0
    score = 0

    def display_question(index):
        """ Afișează întrebarea curentă și răspunsurile asociate. """
        for widget in frame3.winfo_children():
            widget.destroy()

        if index < len(selected_questions):
            question = selected_questions[index]["question"]
            answers = selected_questions[index]["answers"]

            # Font pentru întrebare
            question_label = tk.Label(frame3, text=question, bg="white", font=("Arial", 30, "bold"))
            question_label.pack(pady=20, padx=20, anchor="w")

            # Maximal length for answers
            max_length = max(len(answer) for answer in answers)
            answer_width = max_length * 2  # Adjust multiplier to fit your design

            for answer in answers:
                answer_label = tk.Label(frame3, text=answer, font=("Arial", 30), width=answer_width, anchor="w", bg="white", padx=10, pady=5, borderwidth=1, relief="solid")
                answer_label.pack(fill="x", pady=5, padx=20)

                # Make clicking on the answer a button
                answer_label.bind("<Button-1>", lambda e, ans=answer: check_answer(ans))

        else:
            show_result()

    def check_answer(selected_answer):
        """ Verifică dacă răspunsul selectat este corect. """
        global score, current_question_index

        correct_answer = selected_questions[current_question_index]["correct"]

        if selected_answer == correct_answer:
            score += 1

        current_question_index += 1
        display_question(current_question_index)

    def show_result():
        """ Afișează rezultatul final. """
        result_text = f"Ai răspuns corect la {score} din {len(selected_questions)} întrebări!"
        finish_label = tk.Label(frame3, text=result_text, bg="white", font=("Arial", 30, "bold"))
        finish_label.pack(pady=20)
        back_button = tk.Button(frame3, image=back_photo, bd=0, bg="white", command=show_main_buttons)
        back_button.pack(pady=20)

    display_question(current_question_index)

def show_sub_buttons(button_id):
    """ Afișează textul specific pentru butonul apăsat și butonul de 'Back'. """
    if button_id == 4:
        show_quiz()
    else:
        # Curăță frame3 de toate widget-urile
        for widget in frame3.winfo_children():
            widget.destroy()

        imgD = Image.open(f"M{button_id}.png")
        imgD = imgD.resize((900, 500))  # Redimensionăm imaginea la dimensiunea dorită
        photoD = ImageTk.PhotoImage(imgD)

        # Creăm un Label și setăm imaginea
        labelD = tk.Label(frame3, image=photoD, bd=0, bg="white", relief="flat")
        labelD.image = photoD  # Păstrăm o referință la obiectul imagine pentru a preveni garbage collection
        labelD.pack(expand=True, fill="both")

        # Crează butonul de 'Back' pentru a reveni la cele patru butoane
  # Specifică calea către imaginea TRASH.png
        

        back_button = tk.Button(frame3, image=back_photo, bd=0, bg="white",command=show_main_buttons)
        back_button.pack(pady=20)

    num = read_number_from_file("numar.txt")
    c_list = list(num)
    c_list[2*(button_id-1)]="1"
    num = ''.join(c_list)

    write_number_to_file("numar.txt",num)
    update_progress_bar(num)
    print(num)

def show_main_buttons():
    """ Afișează cele patru butoane principale. """
    # Curăță frame3 de toate widget-urile
    for widget in frame3.winfo_children():
        widget.destroy()

    photos = [photo1, photo2, photo3, photo4]
    photosc = [photo1c, photo2c, photo3c, photo4c]

    c_list = list(read_number_from_file("numar.txt").replace(" ",""))
    for i in range(4):
        if c_list[i] == "1":
            photos[i]=photosc[i]

    # Crează cele patru butoane principale


    button1 = tk.Button(frame3, image=photos[0], bd=0, bg="white", command=lambda: show_sub_buttons(1))
    button2 = tk.Button(frame3, image=photos[1], bd=0, bg="white", command=lambda: show_sub_buttons(2))
    button3 = tk.Button(frame3, image=photos[2], bd=0, bg="white", command=lambda: show_sub_buttons(3))
    button4 = tk.Button(frame3, image=photos[3], bd=0, bg="white", command=lambda: show_sub_buttons(4))
    
    # Plasează butoanele în frame3
    button1.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    button2.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    button3.pack(side="left", fill="both", expand=True, padx=20, pady=20)
    button4.pack(side="left", fill="both", expand=True, padx=20, pady=20)



# Crearea fereastrei principale
root = tk.Tk()
root.title("Aplicație Full Screen")

# Setăm fereastra în modul full screen
root.attributes("-fullscreen", True)
root.bind("<F11>", on_fullscreen)
root.bind("<Escape>", off_fullscreen)

# Creăm frame-urile pentru cele 3 zone
frame1 = tk.Frame(root, bg="white")
frame2 = tk.Frame(root, bg="white")
frame3 = tk.Frame(root, bg="white")

# Folosim pack pentru a le poziționa vertical
frame1.pack(side="top", fill="both")
frame2.pack(side="top", fill="both")
frame3.pack(side="top", fill="both", expand=True)

# Configurăm weights pentru a asigura proporțiile dorite
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_rowconfigure(2, weight=3)

# Adăugăm conținut în frame-uri
# Frame 1: Placeholder pentru o poză fără umbră
image_path = "LOGO.jpeg"  # Specifică calea către imaginea ta

# Încărcăm imaginea
img = Image.open(image_path)
img = img.resize((400, 200))
photo = ImageTk.PhotoImage(img)

close_image_path = "EXIT.png"  # Specifică calea către imaginea TRASH.png
close_img = Image.open(close_image_path)
close_img = close_img.resize((100, 100))  # Redimensionează imaginea dacă este necesar
close_photo = ImageTk.PhotoImage(close_img)

back_img = Image.open("BACK.png")
back_img = back_img.resize((100, 70))  # Redimensionează imaginea dacă este necesar
back_photo = ImageTk.PhotoImage(back_img)

close_button = tk.Button(frame1, image=close_photo, bd=0, bg="white", command=close_application)
close_button.pack(side="right", fill="both", padx=20, pady=20)

# Creăm un Label și setăm imaginea
label1 = tk.Label(frame1, image=photo, bd=0, relief="flat")
label1.image = photo  # Păstrăm o referință la obiectul imagine pentru a preveni garbage collection
label1.pack(side="right",expand=True)

reset_image_path = "TRASH.png"  # Specifică calea către imaginea TRASH.png
reset_img = Image.open(reset_image_path)
reset_img = reset_img.resize((100, 100))  # Redimensionează imaginea dacă este necesar
reset_photo = ImageTk.PhotoImage(reset_img)

img1 = Image.open("DERIV1.png")
img1 = img1.resize((330, 600))
photo1 = ImageTk.PhotoImage(img1)

img1c = Image.open("DERIV1C.png")
img1c = img1c.resize((330, 600))
photo1c = ImageTk.PhotoImage(img1c)

img2 = Image.open("DERIV2.png")
img2 = img2.resize((330, 600))
photo2 = ImageTk.PhotoImage(img2)

img2c = Image.open("DERIV2C.png")
img2c = img2c.resize((330, 600))
photo2c = ImageTk.PhotoImage(img2c)

img3 = Image.open("GRAPH.png")
img3 = img3.resize((330, 600))
photo3 = ImageTk.PhotoImage(img3)

img3c = Image.open("GRAPHC.png")
img3c = img3c.resize((330, 600))
photo3c = ImageTk.PhotoImage(img3c)

img4 = Image.open("QUESTION.png")
img4 = img4.resize((330, 600))
photo4 = ImageTk.PhotoImage(img4)

img4c = Image.open("QUESTIONC.png")
img4c = img4c.resize((330, 600))
photo4c = ImageTk.PhotoImage(img4c)

reset_button = tk.Button(frame1, image=reset_photo, bd=0, bg="white", command=reset_number)
reset_button.image = reset_photo  # Păstrăm o referință la obiectul imagine pentru a preveni garbage collection
reset_button.pack(side="right", fill="both", padx=20, pady=20)

# Frame 2: Bara de progres
canvas = tk.Canvas(frame2, bg="white", bd=0, relief="flat", height=40)
canvas.pack(fill="both", expand=True)

# Citiți numărul din fișier și actualizează bara de progres
number = read_number_from_file("numar.txt")  # Înlocuiește cu calea corectă dacă fișierul nu este în același director
update_progress_bar(number)

# Frame 3: Cele patru butoane principale
show_main_buttons()

root.mainloop()
