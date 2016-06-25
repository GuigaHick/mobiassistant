#section to import libraryes

import tkinter as tk
import tkinter.font as tkFont
import tkinter.ttk as ttk
import sqlite3
import tkinter.messagebox


class MultiColumnListbox(object):

    def __init__(self):
        #criar banco
        self.conectar = sqlite3.connect("database_mobiassistant.db")
        self.cur = self.conectar.cursor()
        self.cur.execute("SELECT * FROM onibus")
        self.lista = self.cur.fetchall()
        for i in self.lista:
            it = (i[0] ,i[1],i[2])
            car_list.append(it)
        self.tree = None
        self._setup_widgets()
        self._build_tree()

    def _setup_widgets(self):

        topFrame = ttk.Frame()
        topFrame.pack(pady=10,padx=10)
        btn = ttk.Button(topFrame,text="Parada",command=self.searchbystop)
        btn.pack(pady=10,padx = 10)
        self.parada = tk.StringVar()
        self.rua = tk.StringVar()
        self.txtparada = ttk.Entry(topFrame,textvariable = self.parada,width=35)
        self.txtparada.pack()
        btnrua = ttk.Button(topFrame,text="Rua",command=self.searchbystreet)
        btnrua.pack(pady=10,padx = 10)
        self.txtrua = ttk.Entry(topFrame,textvariable = self.rua,width=35)
        self.txtrua.pack()
        btnrua = ttk.Button(topFrame,text="Exibir Todos",command=self.show_all)
        btnrua.pack(pady=10,padx = 10)

        s = """Linhas de ônibus da Parada 87
        """
        msg = ttk.Label(wraplength="4i", justify="left", anchor="n",
            padding=(10, 2, 10, 6), text=s)
        msg.pack(fill='x')
        container = ttk.Frame()
        container.pack(fill='both', expand=True)

        # create a treeview with dual scrollbars
        self.tree = ttk.Treeview(columns=car_header, show="headings")
        vsb = ttk.Scrollbar(orient="vertical",
            command=self.tree.yview)
        hsb = ttk.Scrollbar(orient="horizontal",
            command=self.tree.xview)
        self.tree.configure(yscrollcommand=vsb.set,
            xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=container)
        vsb.grid(column=1, row=0, sticky='ns', in_=container)
        hsb.grid(column=0, row=1, sticky='ew', in_=container)
        container.grid_columnconfigure(0, weight=1)
        container.grid_rowconfigure(0, weight=1)
        self.tree.bind("<Double-1>", self.select)

    def _build_tree(self):
        for col in car_header:
            self.tree.heading(col, text=col.title(),
                command=lambda c=col: sortby(self.tree, c, 0))
            # adjust the column's width to the header string
            self.tree.column(col,
                width=tkFont.Font().measure(col.title()))

        for item in car_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)

#this function gonna communicate this application and bus module through nrf wireless 
    def select(self,event):
        item = self.tree.selection()[0]
        codigo,nome,empresa = self.tree.item(item,"values") 
        tkinter.messagebox.showinfo("info","Você selecionou o ônibus : " + str(codigo) + str(nome) + str(empresa))
        #enviar para nrf o código da linha

    def searchbystop(self):
        stop_number = self.txtparada.get()
        self.cur.execute("select o.numero_onibus,o.nome,o.empresa from onibus o ,passar p where p.numer_parada = " + stop_number + " and p.numero_onibus = o.numero_onibus")
        lista = self.cur.fetchall()

        buscount = len(lista)
        
        if buscount > 0:
            ct = len(car_list)
            print(str(ct))
            while ct > 0:
                car_list.remove(car_list[ct-1])
                ct = ct -1

            #populate the data into bus list
            for ib in lista:
                it = (ib[0] ,ib[1], ib[2])
                car_list.append(it)
            
            #call the function to reload the bus list data
            self.reload_results()
            tkinter.messagebox.showinfo("info","As linhas que passam na parada estão listadas abaixo" + str(buscount))
        else:
            tkinter.messagebox.showinfo("info","Não há ônibus para a parada Requerida" + str(buscount))

        self.parada.set("") #erase the input text

    def searchbystreet(self):
        street = self.txtrua.get()
        self.cur.execute("SELECT  O.numero_onibus , O.nome,O.empresa FROM onibus O, parada P, passar Q WHERE Q.numero_onibus = O.numero_onibus AND P.numero_parada= Q.numer_parada AND P.rua LIKE '%"+street+"'")
        lista = self.cur.fetchall()
        buscount = len(lista)

        if buscount > 0:
        #erasing current data, to show specif data to user
            ct = len(car_list)
            print(str(ct))
            while ct > 0:
                car_list.remove(car_list[ct-1])
                ct = ct-1
        #reload the bus list withe the specifcs bus
            for i in lista:
                it = (i[0] ,i[1],i[2])
                car_list.append(it)
            self.reload_results()
            tkinter.messagebox.showinfo("info","As linhas que passam na parada estão listadas abaixo" +str(buscount))
        else:
            tkinter.messagebox.showinfo("info","Não há ônibus para a parada Requerida" + str(buscount))

        self.rua.set("") #erase the input text

    def show_all (self):
        ct = len(car_list)
        print(str(ct))
        while ct > 0:
            car_list.remove(car_list[ct-1])
            ct = ct-1

        i = 0
        while i < len(self.lista):
            item = self.lista[i]
            it = (item[0] ,item[1],item[2])
            car_list.append(it)
            print("atualizou")
            i = i + 1
        self.reload_results()

    def reload_results(self):
        #erasing all data
        for row in self.tree.get_children():
            self.tree.delete(row)
            print("deletou a linha")
        print("Dados Deletados")
 
        for item in car_list:
            self.tree.insert('', 'end', values=item)
            # adjust column's width if necessary to fit each value
            for ix, val in enumerate(item):
                col_w = tkFont.Font().measure(val)
                if self.tree.column(car_header[ix],width=None)<col_w:
                    self.tree.column(car_header[ix], width=col_w)
            print("Adicionou na árvore")

def sortby(tree, col, descending):
    """sort tree contents when a column header is clicked on"""
    # grab values to sort
    data = [(tree.set(child, col), child) \
        for child in tree.get_children('')]
    # if the data to be sorted is numeric change to float
    #data =  change_numeric(data)
    # now sort the data in place
    data.sort(reverse=descending)
    for ix, item in enumerate(data):
        tree.move(item[1], '', ix)
    # switch the heading so it will sort in the opposite direction
    tree.heading(col, command=lambda col=col: sortby(tree, col, \
        int(not descending)))


# the test data ...

car_header = ['Cod', 'Nome','Empresa']

car_list = []

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Mobi Assistant")
    root.geometry("2048x1536");
    listbox = MultiColumnListbox()
    root.mainloop()
