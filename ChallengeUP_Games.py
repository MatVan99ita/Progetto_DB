
import tkinter as tk
import tkinter.font as tkfont
from tkinter import *
from tkinter import ttk

window_main = tk.Tk()
window_main.title("ChallengeUP Games")
admin_log=False
screen_width = window_main.winfo_screenwidth()
screen_height = window_main.winfo_screenheight()

password_entry=tk.StringVar()
name_entry=tk.StringVar()


def Admin_login(log):
    if(log):
        print("si")#andranno mostrati i textbox per le credenziali e nascosto il tasto
        first_frame.pack_forget()
        admin_login_frame.pack(side=tk.TOP)
    else:
        #accesso utente senza log in e senza funzionalità aggiuntive
        program_start("user")
    

def calcolo_dimensioni_finestra(frame, larg=0):
    if(frame=="inizio"):
        nuova_altezza=(10*screen_height)/100
        nuova_larghezza=(20*screen_width)/100
    elif("GUI principale"):#finestra principale
        nuova_altezza=(75*screen_height)/100
        nuova_larghezza=(50*screen_width)/100
    elif("frame tabella"):#frame tabella
        nuova_altezza=(75*screen_height)/100
        nuova_larghezza=((50*screen_width)/2)/100
    elif("tabella"):
        nuova_larghezza=(50*screen_width)/larg)/100
    geometria="%dx%d" % (nuova_larghezza, nuova_altezza)

    return geometria



nomeFrame=Frame()

def program_start(tipologia_utente):
    dimensioni_frame_tabella=calcolo_dimensioni_finestra("GUI principale")
    dimensioni_frame_tabella=dimensioni_frame_tabella.split("x")
    print(dimensioni_frame_tabella)
    if(tipologia_utente=="user"):
        nomeFrame=top_frame
        top_welcome_frame.pack_forget()
        window_main.geometry(calcolo_dimensioni_finestra("GUI principale"))
        top_frame.pack(side=tk.TOP)
        
        db_frame_user = tk.Frame(nomeFrame, highlightbackground="green", highlightcolor="green", highlightthickness=1, background='grey', width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])
        db_frame_user.pack(side=tk.RIGHT)

    elif(tipologia_utente=="admin"):
        print("acceso admin")
        nomeFrame=admin_frame
        top_welcome_frame.pack_forget()
    
        window_main.geometry(calcolo_dimensioni_finestra("GUI principale"))
        
        #if(nome=='mat' and passw=='123'):
        admin_frame.pack(side=tk.TOP)
        db_frame_user = tk.Frame(nomeFrame, highlightbackground="green", highlightcolor="green", highlightthickness=1, background='grey', width=dimensioni_frame_tabella[0], height=dimensioni_frame_tabella[1])
        db_frame_user.pack(side=tk.RIGHT)
        #else:
        #    print("errore user e/o password")
        #controllo sulle credenziali


def genera_tabella_query(ris):
    total_rows=len(ris)
    total_columns=len(ris[0])
    dimensione_colonna=int(total_columns*3)
    for i in range(total_rows):
            for j in range(total_columns):

                e = Entry(db_frame_user, width=dimensione_colonna,font=('Arial',16,'bold'))
                e.grid(row=i, column=j)
                e.insert(END, ris[i][j])

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

lbl_admin_name = tk.Label(admin_login_frame, text = "Name:").grid(row=0, column=0)
ent_admin_name = tk.Entry(admin_login_frame, textvariable=name_entry).grid(row=0, column=1)

lbl_password = tk.Label(admin_login_frame, text = "Password:").grid(row=1, column=0)
ent_password = tk.Entry(admin_login_frame, textvariable=password_entry).grid(row=1, column=1)

btn_Log = tk.Button(admin_login_frame, text="Log-in", command=lambda : program_start("admin")).grid(row=2, column=0)

admin_login_frame.pack(side=tk.TOP)
admin_login_frame.pack_forget()
#####################################
top_welcome_frame.pack(side=tk.TOP)



##################################### FINESTRA PRINCIPALE ####################################################


top_frame = tk.Frame(window_main)
#####################################
top_left_frame = tk.Frame(top_frame, highlightbackground="green", highlightcolor="green", highlightthickness=1)

v=[[1,1,1,1],[2,2,2,2],[3,3,3,3],[4,4,4,4],[5,5,5,5],[6,6,6,6]]
print(v)

btn_U1=tk.Button(top_left_frame, text="Lista delle partite effettuate in un torneo svolto in una data specificata", highlightbackground="green", highlightcolor="green", highlightthickness=1, command=lambda: genera_tabella_query(v)).grid(row=0, column=0)
btn_U2=tk.Button(top_left_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=1, column=0)
btn_U3=tk.Button(top_left_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=2, column=0)
btn_U4=tk.Button(top_left_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=3, column=0)

top_left_frame.pack(side=tk.LEFT)


################### DATABASE FRAME USER ##################
db_frame_user = tk.Frame(window_main, highlightbackground="green", highlightcolor="green", highlightthickness=1)

#tabella
lbl_prova=tk.Label(text="colonne db")

db_frame_user.pack(side=tk.RIGHT)

#####################################


top_frame.pack_forget()
#####################################




############################# SEZIONE ADMIN #############################################

admin_frame = tk.Frame(window_main)


lbl_line = tk.Label(admin_frame, text="***********************************************************").pack()
lbl_line = tk.Label(admin_frame, text="**** SESSIONE ADMIN ****", font = "Helvetica 13 bold", foreground="blue").pack()
lbl_line = tk.Label(admin_frame, text="***********************************************************").pack()


#####################################
final_frame = tk.Frame(admin_frame)
btn_U1_admin=tk.Button(final_frame, text="Lista delle partite effettuate in un torneo svolto in una data specificata", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=0, column=0)
btn_U2_admin=tk.Button(final_frame, text="Top 10 giocatori con il punteggio più alto", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=1, column=0)
btn_U3_admin=tk.Button(final_frame, text="Lista delle carte bandite dall'attuale formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=2, column=0)
btn_U4_admin=tk.Button(final_frame, text="Lista delle carte di un mazzo specificato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=3, column=0)

btn_A1=tk.Button(final_frame, text="Inserimento nuova fiera", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=5, column=0)
btn_A2=tk.Button(final_frame, text="Inserimento nuovo torneo", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=6, column=0)
btn_A3=tk.Button(final_frame, text="Inserimento dipendente", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=7, column=0)
btn_A4=tk.Button(final_frame, text="Inserimento nuovo formato", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=8, column=0)
btn_A5=tk.Button(final_frame, text="Gioco da tavolo con più partite non ufficiali", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=9, column=0)
btn_A6=tk.Button(final_frame, text="Il gioco più venduto per ogni stand", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=10, column=0)
btn_A7=tk.Button(final_frame, text="Registrazione vendita per stand", highlightbackground="green", highlightcolor="green", highlightthickness=1).grid(row=11, column=0)


final_frame.pack(side=tk.LEFT)



#####################################

admin_frame.pack_forget()





################### DATABASE FRAME ##################



window_main.mainloop()


######################################################################################################
