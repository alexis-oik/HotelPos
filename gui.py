import tkinter.messagebox
from tkinter import *
from tkinter import ttk
from time import strftime
from datetime import date
from database import Database
from orders_gui import Orders_gui

DELETE_ICON = './icons/delete.PNG'
MINUS_ICON = './icons/minus.png'
CHECKOUT_ICON = './icons/cart.png'
CANCEL_ICON = './icons/cancel.png'
TABLE_ICON = './icons/table.png'
TABLE_TAKEN_ICON = './icons/table-taken.png'

MAIN_BUTTON_COLOUR = '#6FB2D2'
SUB_BUTTON_COLOUR = '#DFF6FF'


def responsive_spaces(frame, rows, columns):
    for i in range(rows):
        frame.grid_rowconfigure(i, weight=1)
    for i in range(columns):
        frame.grid_columnconfigure(i, weight=1)


class Gui:

    def __init__(self, database: Database):
        self.data = database
        self.root = Tk()
        self.root.title("HotelPos")
        self.root.config(padx=20, pady=20)
        responsive_spaces(self.root, 10, 6)

        # ------------------------------------ VARIABLES ---------------------------------------------------------
        self.buttons = []
        self.table_buttons = []
        self.register_item_index = 0

        # ------------------------------------ MENU BAR ---------------------------------------------------------
        self.menu_bar = Menu(self.root)
        self.file_menu = Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="View Orders", command=lambda data=self.data: Orders_gui(data))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.root.config(menu=self.menu_bar)

        # ------------------------------------ CUSTOMER DETAILS FRAME (0,0) --------------------------------------
        self.customer_frame = LabelFrame(self.root, text="Customer Details")
        self.customer_frame.grid(row=0, column=0, pady=15, sticky=NSEW)
        responsive_spaces(self.customer_frame, 4, 3)
        # ------------------------------------ CUSTOMER DETAILS COMPONENTS ---------------------------------------
        self.room_number_label = Label(self.customer_frame, text="Selected Room Number")
        self.room_number_label.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        self.room_number_input = Entry(self.customer_frame)
        self.room_number_input.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
        self.room_number_button = Button(self.customer_frame, text="Load", command=self.load_room)
        self.room_number_button.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)
        self.name_label = Label(self.customer_frame, text="Customer Name: ")
        self.name_label.grid(row=1, column=0, padx=10, sticky=NSEW)
        self.name_label_text = Label(self.customer_frame, text="")
        self.name_label_text.grid(row=1, column=1, padx=10, sticky=NSEW)
        self.room_label = Label(self.customer_frame, text="Room: ")
        self.room_label.grid(row=2, column=0, padx=10, sticky=NSEW)
        self.room_label_text = Label(self.customer_frame, text="")
        self.room_label_text.grid(row=2, column=1, padx=10, sticky=NSEW)
        self.number_guests_label = Label(self.customer_frame, text="Guests: ")
        self.number_guests_label.grid(row=3, column=0, padx=10, sticky=NSEW)
        self.number_guests_label_text = Label(self.customer_frame, text="")
        self.number_guests_label_text.grid(row=3, column=1, padx=10, sticky=NSEW)

        # ------------------------------------ TIME FRAME (0,1) --------------------------------------------------
        self.time_frame = LabelFrame(self.root, text="Time")
        self.time_frame.grid(row=0, column=1)
        self.time_label = Label(self.time_frame)
        self.date_label = Label(self.time_frame)
        responsive_spaces(self.time_frame, 2, 3)
        self.get_time()
        self.get_date()
        self.time_label.pack()
        self.date_label.pack()

        # ------------------------------------ REGISTER FRAME (1,0) -----------------------------------------------
        self.register_frame = LabelFrame(self.root, text='Register')
        self.register_frame.grid(row=1, column=0)
        # ------------------------------------ REGISTER COMPONENTS-------------------------------------------------
        self.register = ttk.Treeview(self.register_frame, selectmode='browse')
        self.register['columns'] = ('Description', 'Qty', 'Price', 'Total')

        self.register.column('#0', width=0, stretch=NO)
        self.register.column('Description', anchor=CENTER, width=160)
        self.register.column('Qty', anchor=CENTER, width=40)
        self.register.column('Price', anchor=CENTER, width=80)
        self.register.column('Total', anchor=CENTER, width=80)

        vsb = ttk.Scrollbar(self.register_frame, orient="vertical", command=self.register.yview)
        vsb.pack(side='right', fill='y')

        self.register.heading('#0', text='', anchor=CENTER)
        self.register.heading('Description', text='Description', anchor=CENTER)
        self.register.heading('Qty', text='Qty', anchor=CENTER)
        self.register.heading('Price', text='Price', anchor=CENTER)
        self.register.heading('Total', text='Total', anchor=CENTER)
        self.register.pack(side='left')

        minus_icon = PhotoImage(file=MINUS_ICON)
        plus_button = Button(self.register_frame, highlightthickness=0, image=minus_icon, command=self.reduce_qty_item)
        plus_button.pack(side=TOP)
        delete_icon = PhotoImage(file=DELETE_ICON)
        delete_button = Button(self.register_frame, highlightthickness=0, image=delete_icon,
                               command=self.delete_register_item)
        delete_button.pack(side=TOP)

        # ------------------------------------ MENU ITEMS FRAME (1,1)----------------------------------------------
        self.menu_frame = LabelFrame(self.root, text="Menu Items")
        self.menu_frame.grid(row=1, column=1, padx=10)
        responsive_spaces(self.menu_frame, 5, 5)
        # ------------------------------------ MENU ITEMS COMPONENTS-----------------------------------------------
        self.main_menu()

        # ------------------------------------ CHECKOUT FRAME (2,0)------------------------------------------------
        self.checkout_frame = LabelFrame(self.root)
        self.checkout_frame.grid(row=2, column=0, pady=5)
        responsive_spaces(self.checkout_frame, 5, 2)
        # ------------------------------------ CHECKOUT COMPONENTS-------------------------------------------------
        self.subtotal_label = Label(self.checkout_frame, text="Subtotal: ", font=2)
        self.subtotal_label.grid(row=1, column=0, pady=5, sticky=NSEW)
        self.subtotal_label_text = Label(self.checkout_frame, text="0.00", font=2)
        self.subtotal_label_text.grid(row=1, column=1, padx=(220, 2), pady=5)
        self.tax_label = Label(self.checkout_frame, text="Tax 24%: ", font=2)
        self.tax_label.grid(row=2, column=0, pady=5, sticky=NSEW)
        self.tax_label_text = Label(self.checkout_frame, text="0.00", font=2)
        self.tax_label_text.grid(row=2, column=1, padx=(220, 2), pady=5, sticky=NSEW)
        self.total_label = Label(self.checkout_frame, text="Total: ", font=('Arial', 15, 'bold'))
        self.total_label.grid(row=3, column=0, pady=5, sticky=NSEW)
        self.total_label_text = Label(self.checkout_frame, text="0.00", font=('Arial', 15, 'bold'))
        self.total_label_text.grid(row=3, column=1, padx=(220, 2), pady=5, sticky=NSEW)
        self.table_label = Label(self.checkout_frame, text="Table: ")
        self.table_label.grid(row=4, column=0, pady=5, sticky=NSEW)
        self.table_label_text = Label(self.checkout_frame, text="")
        self.table_label_text.grid(row=4, column=0, padx=(50, 0), pady=5, sticky=NSEW)
        cancel_icon = PhotoImage(file=CANCEL_ICON)
        self.cancel_button = Button(self.checkout_frame, image=cancel_icon, highlightthickness=0, border=0,
                                    command=self.cancel_order)
        self.cancel_button.grid(row=4, column=1, padx=(120, 2), pady=(15, 2), sticky=NSEW)
        checkout_icon = PhotoImage(file=CHECKOUT_ICON)
        self.checkout_button = Button(self.checkout_frame, image=checkout_icon, highlightthickness=0, border=0,
                                      state='disabled', command=self.send_order)
        self.checkout_button.grid(row=4, column=1, padx=(220, 0), pady=(15, 2), sticky=NSEW)

        # ------------------------------------ TABLE FRAME (2,1) ------------------------------------------------
        self.table_frame = LabelFrame(self.root, text='Tables')
        self.table_frame.grid(row=2, column=1, columnspan=10, rowspan=10)
        responsive_spaces(self.table_frame, 50, 50)
        # ------------------------------------ TABLE FRAME ------------------------------------------------------
        self.table_icon = PhotoImage(file=TABLE_ICON)
        self.table_taken_icon = PhotoImage(file=TABLE_TAKEN_ICON)
        self.create_tables()

        self.root.mainloop()

    # Deletes the submenu buttons to load new submenu
    def hide_buttons(self):
        for button in self.buttons:
            button.grid_forget()

    def enable_checkout_button(self):
        self.checkout_button.config(state='active')

    def table_taken(self, button):
        if button.cget('image') == "pyimage5":
            table_num = button.cget('text')
            self.table_label_text.config(text=table_num)
        else:
            answer = tkinter.messagebox.askyesno(title="Receipt",
                                                 message=f"Send receipt on table {button.cget('text')}?")
            if answer:
                button.config(image=self.table_icon)

    def send_order(self):
        if self.table_label_text.cget('text') != '' and self.name_label_text.cget('text') != '':
            answer = tkinter.messagebox.askyesno(title="Confirmation", message=f"Are you sure you want to send the "
                                                                               f"order?")
            if answer:
                i = int(self.table_label_text.cget('text')) - 1
                button = self.table_buttons[i]
                button.config(image=self.table_taken_icon)
                self.place_order()
                self.cancel_order()
        else:
            tkinter.messagebox.showwarning(title="Error", message=f"Please select room and table")

    def cancel_order(self):
        self.register.delete(*self.register.get_children())
        self.hide_buttons()
        self.subtotal_label_text.config(text="0.00")
        self.tax_label_text.config(text="0.00")
        self.total_label_text.config(text="0.00")
        self.room_number_input.config(state='normal')
        self.room_number_button.config(state='active')
        self.room_label_text.config(text='')
        self.name_label_text.config(text='')
        self.number_guests_label_text.config(text='')
        self.table_label_text.config(text='')
        self.checkout_button.config(state='disabled')
        self.buttons.clear()

    def calculate_total(self):
        subtotal = sum(float(self.register.set(item, 'Total')) for item in self.register.get_children())
        self.subtotal_label_text.config(text=subtotal)
        tax = (subtotal * 0.24)
        self.tax_label_text.config(text="{:.2f}".format(tax))
        total = subtotal + tax
        self.total_label_text.config(text="{:.2f}".format(total))

    def delete_register_item(self):
        selected_item = self.register.selection()[0]
        self.register.delete(selected_item)
        self.calculate_total()

    def reduce_qty_item(self):
        item = self.register.selection()[0]
        values = self.register.item(item, 'values')
        name = values[0]
        qty = int(values[1]) - 1
        if qty != 0:
            price = values[2]
            total = float(values[3]) - float(price)
            self.register.item(item, text='', values=(name, qty, price, total))
        else:
            self.delete_register_item()
        self.calculate_total()

    def get_time(self):
        string = strftime('%H:%M:%S %p')
        self.time_label.config(text=string, font=('Arial', 30, 'bold'))
        self.time_label.after(1000, self.get_time)
        return string

    def get_date(self):
        today = date.today().strftime("%d/%m/%Y")
        self.date_label.config(text=today, font=('Arial', 30, 'bold'))
        return today

    # Create main menu buttons
    def main_menu(self):
        beer = Button(self.menu_frame, highlightthickness=0, border=0, text="Beer", width=15, height=5,
                      bg=MAIN_BUTTON_COLOUR, command=lambda item="beers": self.sub_menu(item))
        beer.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
        soft_drinks = Button(self.menu_frame, highlightthickness=0, border=0, text="Soft Drinks", width=15, height=5,
                             bg=MAIN_BUTTON_COLOUR, command=lambda item="soft drinks": self.sub_menu(item))
        soft_drinks.grid(row=0, column=1, padx=10, pady=10, sticky=NSEW)
        wine = Button(self.menu_frame, highlightthickness=0, border=0, text="Wine", width=15, height=5,
                      bg=MAIN_BUTTON_COLOUR, command=lambda item="wine": self.sub_menu(item))
        wine.grid(row=0, column=2, padx=10, pady=10, sticky=NSEW)
        water = Button(self.menu_frame, highlightthickness=0, border=0, text="Water", width=15, height=5,
                       bg=MAIN_BUTTON_COLOUR, command=lambda item="water": self.sub_menu(item))
        water.grid(row=0, column=3, padx=10, pady=10, sticky=NSEW)

    # Load submenu of each item in the main menu
    def sub_menu(self, item):
        row = 2
        column = -1
        self.hide_buttons()
        self.room_number_input.config(state='disabled')
        self.room_number_button.config(state='disabled')
        for i in range(0, len(self.data.products[item])):
            it = self.data.products[item][i]
            button = Button(self.menu_frame, highlightthickness=0, border=0, text=it['title'], width=20, height=5,
                            bg=SUB_BUTTON_COLOUR, command=lambda itm=it: self.add_to_register(itm))
            self.buttons.append(button)
            if i % 4 != 0:
                column += 1
                button.grid(row=row, column=column, padx=10, pady=10, sticky=NSEW)
            else:
                row += 1
                column = 0
                button.grid(row=row, column=column, padx=10, pady=10, sticky=NSEW)

    def create_tables(self):
        table_num = 1
        for i in range(4):
            for j in range(5):
                b = Button(self.table_frame, text=table_num, image=self.table_icon, compound='bottom', font=5)
                b.config(command=lambda button=b: self.table_taken(button))
                b.grid(row=i, column=j, padx=10, pady=10, sticky=NSEW)
                self.table_buttons.append(b)
                table_num += 1

    # Add items in register to make an order
    def add_to_register(self, item):
        child = self.search_register(item['title'])
        if child == 0:
            self.register.insert(parent='', index=self.register_item_index, iid=str(self.register_item_index), text='',
                                 values=(item['title'], '1', item['price'], item['price']))
            self.register_item_index += 1
        else:
            values = self.register.item(child, 'values')
            qty = int(values[1]) + 1
            total = float(values[3]) + float(item['price'])
            self.register.item(child, text='', values=(item["title"], qty, item["price"], total))
        self.calculate_total()
        self.enable_checkout_button()

    # Search the register for the same entry if we have duplicates we increase qty in add_to register function
    def search_register(self, title):
        children = self.register.get_children('')
        for child in children:
            values = self.register.item(child, 'values')
            if title == values[0]:
                return child
        return 0

    # Search for the room number if not exists sends message
    def load_room(self):
        room_number = self.room_number_input.get()
        for customer in self.data.customers:
            if customer['room'] == room_number:
                self.room_label_text.config(text=customer['room'])
                self.name_label_text.config(text=customer['name'])
                self.number_guests_label_text.config(text=customer['guests'])
                self.room_number_input.delete(0, END)
                return
        tkinter.messagebox.showwarning(title="Error", message=f"Room {room_number} does not exists!")

    def place_order(self):
        customer_name = self.name_label_text.cget('text')
        customer_id = self.data.find_customer_id(customer_name)
        time = self.get_time()
        day = self.get_date()
        table = self.table_label_text.cget('text')
        total_price = self.total_label_text.cget('text')
        self.data.send_invoice((customer_id, day, time, table, total_price))
        invoice_id = self.data.get_last_invoice_id()
        children = self.register.get_children('')
        for child in children:
            values = self.register.item(child, 'values')
            product_name = values[0]
            product_id = self.data.find_product_id(product_name)
            quantity = values[1]
            price = values[3]
            self.data.send_order((customer_id, product_id, invoice_id, day, quantity, price))
