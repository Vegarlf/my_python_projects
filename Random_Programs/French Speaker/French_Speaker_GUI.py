import tkinter as tk; from tkinter import font; from gtts import gTTS; import io, sys, os, pygame
pygame.mixer.init()

def resourcepath(relativepath):
     try:
          basepath = sys._MEIPASS
     except Exception:
          basepath = os.path.abspath(".")
     return os.path.join(basepath,relativepath)

def resizebox(event):
     widget = event.widget
     numlines = widget.count("1.0", "end", "displaylines")
     if numlines is None:
          numlines = [1]
     currentheight = int(numlines[0])
     newheight = min(max(currentheight, 1), 5)
     widget.config(height = newheight)

def speaker(event=None):
        if event:
             if event.state & 0x0001:
                  return None
             speakbutton.config(relief=tk.SUNKEN)
             speakbutton.update_idletasks()
             root.after(100, lambda: speakbutton.config(relief=tk.RAISED))
    
        tospeak = speakinput.get("1.0","end-1c").strip().lower()
        if not tospeak:
             return
        try:
            speakbutton.config(text="Speaking...", font=italicfont)
            speakbutton.update_idletasks()
            fp = io.BytesIO()
            tts = gTTS(text=tospeak, lang="fr")  
            tts.write_to_fp(fp)
            fp.seek(0)
            pygame.mixer.music.load(fp)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                 root.update()           
        except Exception as e:
            errorpanel.config(text= f"Error: {e}")
        try:
            speakbutton.config(text="Speak", font = boldfont)
        except:
             pass


root = tk.Tk()
root.title("French Speaker")
root.geometry("500x300")
try:
    root.iconbitmap("app_icon.ico") 
except:
    pass
root.configure(bg="#053596")
try:
    root.iconbitmap(resourcepath("FrenchSpeakerIcon.ico"))
except:
     pass

titlefont = font.Font(family="Times New Roman", size=24, weight="bold", underline=True,)
boldfont = font.Font(family="Times New Roman", size=16, weight= 'bold', slant= 'italic')
italicfont = font.Font(family='Times New Roman', size=16, weight = 'bold', slant= 'italic')

label = tk.Label(root, text="French Speaker", font=titlefont, fg="#15AB13", bg="#053596")
speakinput = tk.Text(root, width=30, height=1, font=("Times New Roman", 16), wrap=tk.WORD)
speakbutton = tk.Button(
    root,
    text="Speak",
    bg="red",
    fg="white",
    command=speaker,
    font = boldfont,
    width=10,
)
errorpanel = tk.Label(root, text="")
label.grid(row=0, column=1, pady=20)
speakinput.grid(row=1, column=1, pady=20)
speakbutton.grid(row=2, column=1, pady=20)
errorpanel.grid(row=3,column=1,pady=10,padx=10)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(2, weight=1)
speakinput.bind("<KeyRelease>", resizebox)
speakinput.bind('<Return>', speaker)
errorpanel.configure(text="", fg= "black", bg="#053596")
root.mainloop()
