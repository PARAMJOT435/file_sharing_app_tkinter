from tkinter import *
import os
import socket
from tkinter import filedialog, messagebox

root = Tk()
root.title("Share It")
root.geometry("450x560+500+200")
root.configure(bg="#f4fdfe")
root.resizable(False, False)

filename = None

# Function to select a file
def select_file():
    global filename
    try:
        filename = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title='Select a file',
            filetypes=[('All Files', '*.*')]
        )
        if filename:
            messagebox.showinfo("File Selected", f"File '{os.path.basename(filename)}' selected.")
        else:
            messagebox.showwarning("No File", "No file was selected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while selecting a file: {e}")

# Function to send a file
def sender():
    try:
        if not filename:
            messagebox.showwarning("No File", "Please select a file first.")
            return

        s = socket.socket()
        host = socket.gethostname()
        port = 8080
        s.bind((host, port))
        s.listen(1)
        print(f"Host: {host}")
        print('Waiting for incoming connection...')

        conn, addr = s.accept()
        print(f"Connection established with {addr}")

        with open(filename, 'rb') as file:
            while True:
                file_data = file.read(1024)
                if not file_data:
                    break
                conn.send(file_data)

        print('Data has been transmitted successfully...')
        conn.close()
        messagebox.showinfo("Success", "File has been sent successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while sending the file: {e}")
    finally:
        s.close()

# Function to open the send window
def send():
    window = Toplevel(root)
    window.title("Send")
    window.geometry('450x560+500+200')
    window.configure(bg='#f4fdfe')
    window.resizable(False, False)

    image_icon1 = PhotoImage(file='send.png')
    window.iconphoto(False, image_icon1)

    sbackground = PhotoImage(file='sender.png')
    Label(window, image=sbackground).place(x=-2, y=0)

    mbackground = PhotoImage(file='id.png')
    Label(window, image=mbackground, bg='#f4fdfe').place(x=100, y=260)

    hostname = socket.gethostname()
    ip_address = socket.gethostbyname(hostname)
    Label(window, text=f'ID: {hostname}\nIP: {ip_address}', bg='#ffffff', fg='#000000').place(x=170, y=285)

    Button(window, text="+ Select File", width=10, height=1, font='arial 14 bold', bg='#ffffff', fg='#000000', command=select_file).place(x=160, y=150)
    Button(window, text="Send", width=8, height=1, font='arial 14 bold', bg='#000000', fg='#ffffff', command=sender).place(x=300, y=150)

    window.mainloop()

# Function to receive a file
def receiver():
    try:
        ID = senderId.get()
        filename1 = incoming_file.get()

        if not ID or not filename1:
            messagebox.showwarning("Input Missing", "Please provide both sender ID and file name.")
            return

        s = socket.socket()
        port = 8080
        s.connect((ID, port))
        print('Connected to the sender')

        with open(filename1, 'wb') as file:
            while True:
                file_data = s.recv(1024)
                if not file_data:
                    break
                file.write(file_data)

        print('File has been successfully received')
        messagebox.showinfo("Success", "File has been received successfully.")
    except ConnectionRefusedError:
        messagebox.showerror("Connection Error", "Unable to connect to the sender. Check the ID and network connection.")
    except FileNotFoundError:
        messagebox.showerror("File Error", "Invalid file path provided.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while receiving the file: {e}")
    finally:
        s.close()

# Function to open the receive window
def receive():
    main = Toplevel(root)
    main.title("Receive")
    main.geometry('450x560+500+200')
    main.configure(bg='#f4fdfe')
    main.resizable(False, False)

    image_icon1 = PhotoImage(file='recieve.png')
    main.iconphoto(False, image_icon1)

    hbackground = PhotoImage(file='receiver.png')
    Label(main, image=hbackground).place(x=-2, y=0)

    logo = PhotoImage(file='profile.png')
    Label(main, image=logo, bg='#f4fdfe').place(x=10, y=250)

    Label(main, text='Receive', font=('arial', 20), bg='#f4fdfe').place(x=100, y=270)
    Label(main, text='Input sender ID', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=340)

    global senderId, incoming_file
    senderId = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    senderId.place(x=20, y=370)
    senderId.focus()

    Label(main, text='Filename for incoming file', font=('arial', 10, 'bold'), bg='#f4fdfe').place(x=20, y=420)
    incoming_file = Entry(main, width=25, fg='black', border=2, bg='white', font=('arial', 15))
    incoming_file.place(x=20, y=450)

    imageicon = PhotoImage(file='arrow.png')
    rr = Button(main, text='Receive', compound=LEFT, image=imageicon, width=130, bg='#39c790', font='arial 14 bold', command=receiver)
    rr.place(x=20, y=500)

    main.mainloop()

# Main GUI setup
image_icon = PhotoImage(file="icon.png")
root.iconphoto(False, image_icon)

Label(root, text="File Transfer", font=('acumin variable concept', 20, 'bold'), bg='#f4fdfe').place(x=20, y=30)
Frame(root, width=400, height=2, bg='#f3f5f6').place(x=25, y=80)

send_image = PhotoImage(file='send.png')
Button(root, image=send_image, bg='#f4fdfe', bd=0, command=send).place(x=50, y=100)

recieve_image = PhotoImage(file='recieve.png')
Button(root, image=recieve_image, bg='#f4fdfe', bd=0, command=receive).place(x=300, y=100)

Label(root, text="Send", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=65, y=200)
Label(root, text="Receive", font=('Acumin Variable Concept', 17, 'bold'), bg="#f4fdfe").place(x=300, y=200)

background = PhotoImage(file="background.png")
Label(root, image=background).place(x=-2, y=323)

root.mainloop()
