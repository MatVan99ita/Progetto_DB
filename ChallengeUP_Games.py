
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import PhotoImage
from tkinter import messagebox


window_main = tk.Tk()
window_main.title("ChallengeUP Games")
admin_log=False

def Admin_login(log):
    if(log):
        print("si")#andranno mostrati i textbox per le credenziali e nascosto il tasto
        first_frame.pack_forget()
        admin_login_frame.pack(side=tk.TOP)
    else:
        #accesso utente senza log in e senza funzionalità aggiuntive
        program_start("user")
    

def calcolo_dimensioni_finestra(frame):
    screen_width = window_main.winfo_screenwidth()
    screen_height = window_main.winfo_screenheight()

    if(frame=="inizio"):
        nuova_altezza=(10*screen_height)/100
        nuova_larghezza=(20*screen_width)/100
    else:#finestra principale
        nuova_altezza=(75*screen_height)/100
        nuova_larghezza=(50*screen_width)/100
    geometria="%dx%d" % (nuova_larghezza, nuova_altezza)

    return geometria


def program_start(tipologia_utente):
        
    if(tipologia_utente=="user"):
        window_main.geometry(calcolo_dimensioni_finestra("GUI principale"))
        print("accesso utente")
        top_welcome_frame.pack_forget()
        top_frame.pack()
        middle_frame.pack()
    else:
        print("acceso admin")
        #controllo sulle credenziali



window_main.geometry(calcolo_dimensioni_finestra("inizio"))


##################################### FINESTRA LOG IN ####################################################

top_welcome_frame = tk.Frame(window_main)

#####################################
first_frame = tk.Frame(top_welcome_frame)

lbl_choice1 = tk.Label(first_frame, text = "Log in method:")
lbl_choice1.pack(side=tk.LEFT)
btn_Admin = tk.Button(first_frame, text="Admin", command=lambda : Admin_login(True))
btn_Admin.pack(side=tk.RIGHT)
btn_User = tk.Button(first_frame, text="User", command=lambda : Admin_login(False))
btn_User.pack(side=tk.RIGHT)

first_frame.pack(side=tk.TOP)
#####################################

#####################################
admin_login_frame = tk.Frame(top_welcome_frame)

lbl_name = tk.Label(admin_login_frame, text = "Name:").grid(row=0, column=0)
ent_name = tk.Entry(admin_login_frame).grid(row=0, column=1)
lbl_password = tk.Label(admin_login_frame, text = "Password:").grid(row=1, column=0)
ent_password = tk.Entry(admin_login_frame).grid(row=1, column=1)
btn_Log = tk.Button(admin_login_frame, text="Log-in", command=lambda : program_start("admin")).grid(row=2, column=0)

admin_login_frame.pack(side=tk.TOP)
admin_login_frame.pack_forget()
#####################################


top_welcome_frame.pack(side=tk.TOP)
##################################### FINESTRA PRINCIPALE ####################################################

top_frame = tk.Frame(window_main)
#####################################
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)

lbl_your_name = tk.Label(top_left_frame, text="Your name: ", font = "Helvetica 13 bold")
lbl_opponent_name = tk.Label(top_left_frame, text="Opponent: ")
lbl_your_name.grid(row=0, column=0, padx=5, pady=8)
lbl_opponent_name.grid(row=1, column=0, padx=5, pady=8)

top_left_frame.pack(side=tk.LEFT, padx=(10, 10))
#####################################

#####################################
top_right_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)

lbl_game_round = tk.Label(top_right_frame, text="Game round (x) starts in", foreground="blue", font = "Helvetica 14 bold")
lbl_timer = tk.Label(top_right_frame, text=" ", font = "Helvetica 24 bold", foreground="blue")
lbl_game_round.grid(row=0, column=0, padx=5, pady=5)
lbl_timer.grid(row=1, column=0, padx=5, pady=5)

top_right_frame.pack(side=tk.RIGHT, padx=(10, 10))

#####################################
top_frame.pack_forget()


##########################################################################

middle_frame = tk.Frame(window_main)

lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()
lbl_line = tk.Label(middle_frame, text="**** GAME LOG ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(middle_frame, text="***********************************************************").pack()

#####################################
round_frame = tk.Frame(middle_frame)

lbl_round = tk.Label(round_frame, text="Round")
lbl_round.pack()
lbl_your_choice = tk.Label(round_frame, text="Your choice: " + "None", font = "Helvetica 13 bold")
lbl_your_choice.pack()
lbl_opponent_choice = tk.Label(round_frame, text="Opponent choice: " + "None")
lbl_opponent_choice.pack()
lbl_result = tk.Label(round_frame, text=" ", foreground="blue", font = "Helvetica 14 bold")
lbl_result.pack()

round_frame.pack(side=tk.TOP)
#####################################

#####################################
final_frame = tk.Frame(middle_frame)

lbl_line = tk.Label(final_frame, text="***********************************************************").pack()
lbl_final_result = tk.Label(final_frame, text=" ", font = "Helvetica 13 bold", foreground="blue")
lbl_final_result.pack()
lbl_line = tk.Label(final_frame, text="***********************************************************").pack()

final_frame.pack(side=tk.TOP)
#####################################

middle_frame.pack_forget()


window_main.mainloop()