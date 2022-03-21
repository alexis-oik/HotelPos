from tkinter import *
from tkinter import ttk


class Orders_gui:

    def __init__(self, database):
        self.data = database
        self.window = Tk()
        self.window.title("View Orders")
        self.window.config(padx=20, pady=20)

        self.order_item_index = 0

        # ------------------------------------ CANVAS ----------------------------------------------------------
        self.canvas = Canvas(self.window)
        self.canvas.pack()

        # ------------------------------------ CANVAS COMPONENTS-------------------------------------------------
        self.orders = ttk.Treeview(self.canvas, selectmode='browse')
        self.orders['columns'] = ('Date', 'Time', 'Table', 'Customer', 'Invoice', 'Total Price')

        self.orders.column('#0', width=0, stretch=NO)
        self.orders.column('Date', anchor=CENTER, width=100)
        self.orders.column('Time', anchor=CENTER, width=100)
        self.orders.column('Table', anchor=CENTER, width=80)
        self.orders.column('Customer', anchor=CENTER, width=160)
        self.orders.column('Invoice', anchor=CENTER, width=80)
        self.orders.column('Total Price', anchor=CENTER, width=100)

        vsb = ttk.Scrollbar(self.canvas, orient="vertical", command=self.orders.yview)
        vsb.pack(side='right', fill='y')

        self.orders.heading('#0', text='', anchor=CENTER)
        self.orders.heading('Date', text='Date', anchor=CENTER)
        self.orders.heading('Time', text='Time', anchor=CENTER)
        self.orders.heading('Table', text='Table', anchor=CENTER)
        self.orders.heading('Customer', text='Customer', anchor=CENTER)
        self.orders.heading('Invoice', text='Invoice', anchor=CENTER)
        self.orders.heading('Total Price', text='Total Price', anchor=CENTER)
        self.orders.pack()

        open_button = Button(self.window, highlightthickness=0, text="Open", command=self.display_selected_order_items)
        open_button.pack(pady=(10, 0))
        back_button = Button(self.window, highlightthickness=0, text="Back", command=self.back_button_display)
        back_button.pack(pady=(10, 0))

        self.display_order()

        self.window.mainloop()

    def display_order(self):
        invoices = self.data.get_all_orders()
        for invoice in invoices:
            self.orders.insert(parent='', index=self.order_item_index, iid=str(self.order_item_index), text='',
                               values=(invoice[0], invoice[1], invoice[2], invoice[3], invoice[4], invoice[5]))
            self.order_item_index += 1

    def display_selected_order_items(self):
        item = self.orders.selection()[0]
        values = self.orders.item(item, 'values')
        order_items = self.data.get_selected_order_items(values[4])
        self.orders.delete(*self.orders.get_children())
        self.order_item_index = 0
        self.orders.insert(parent='', index=self.order_item_index, iid=str(self.order_item_index), text='',
                           values=(values[0], values[1], values[2], values[3], values[4], values[5]))
        for order_item in order_items:
            self.order_item_index += 1
            self.orders.insert(parent='', index=self.order_item_index, iid=str(self.order_item_index), text='',
                               values=('', '', '', f'{order_item[1]} x {order_item[0]}', '', order_item[2]))

    def back_button_display(self):
        self.orders.delete(*self.orders.get_children())
        self.display_order()
