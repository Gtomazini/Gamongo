import  tkinter as tk
from tkinter import ttk


def main():
    app = Application()
    app.mainloop()

class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        self.title("Gamongo")

        # Grid configuration
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=3)
        self.rowconfigure(0, weight=0)  # Toolbar - altura fixa
        self.rowconfigure(1, weight=1)  # Sidebar esquerda
        self.rowconfigure(2, weight=2)

        toolbar = ToolBar(self)
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)

        # SIDEBAR ESQUERDA - Lista de databases (ocupa toda a lateral)
        list_connections = ListConnections(self)
        list_connections.grid(row=1, column=0, rowspan=2, sticky="nsew", padx=(5, 2), pady=(0, 5))

        # ÁREA QUERY - Top right (menor)
        terminal_query = TerminalQuery(self)
        terminal_query.grid(row=1, column=1, sticky="nsew", padx=(2, 5), pady=(0, 2))

        # ÁREA RESULTADOS - Bottom right (maior)
        tree_result = TreeResult(self)
        tree_result.grid(row=2, column=1, sticky="nsew", padx=(2, 5), pady=(2, 5))


class ToolBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, relief="solid", borderwidth=1, height=40)
        self.pack_propagate(False)
        self.parent = parent
        self.connect_btn = ttk.Button(self, text="Connect", command=self.connect_to_mongo)
        self.connect_btn.grid(row=0, column=0, padx=(5, 2), pady=5)

        self.query_btn = ttk.Button(self, text="Query", command=self.query_orders_mongo)
        self.query_btn.grid(row=0, column=1, padx=(2, 5), pady=5)

    def connect_to_mongo(self):
        connection_mongo = ConnectionDialog(self.parent)
        connection_mongo.create_widgets()

    def query_orders_mongo(self):
        print("Query realizada com sucesso!")


class ListConnections(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Listbox das conexões
        self.text_list = tk.Listbox(self, relief="flat", borderwidth=0)
        self.text_list.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)

        # Adicionar algumas conexões de exemplo
        self.text_list.insert(0, "meubanco-teste-mongo")
        self.text_list.insert(1, "meubanco2-teste-mongo")

class TerminalQuery(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.text_query = tk.Text(self, height=8, width=50)
        self.text_query.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.text_query.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.text_query.configure(yscrollcommand=scrollbar.set)


class TreeResult(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Treeview para resultados hierárquicos
        self.tree = ttk.Treeview(self)
        self.tree.grid(row=0, column=0, sticky="nsew", padx=0, pady=0)
        doc_id = self.tree.insert("", "end", text="Documento 1")
        self.tree.insert(doc_id, "end", text="_id: 507f1f77bcf86cd799439011")
        self.tree.insert(doc_id, "end", text="nome: João")
        self.tree.insert(doc_id, "end", text="idade: 26")

        doc_id2 = self.tree.insert("", "end", text="Documento 2")
        self.tree.insert(doc_id2, "end", text="_id: 507f1f77bcf86cd799439357")
        self.tree.insert(doc_id2, "end", text="nome: Alberto")
        self.tree.insert(doc_id2, "end", text="idade: 34")

        doc_id3 = self.tree.insert("", "end", text="Documento 2")
        self.tree.insert(doc_id3, "end", text="_id: 507f1f77bcf86cd799439z14")
        self.tree.insert(doc_id3, "end", text="nome: Gabriel")
        self.tree.insert(doc_id3, "end", text="idade: 25")

        # Scrollbar para o treeview
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)


class ConnectionDialog:
    def __init__(self, parent):
        self.conectar_btn = None
        self.cancelar_btn = None
        self.result = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nova Conexão MongoDB")
        self.dialog.geometry("350x200")
        self.dialog.resizable(False, False)
        self.dialog.transient(parent)
        self.dialog.grab_set()

        # Centralizar
        self.dialog.geometry("+%d+%d" % (parent.winfo_rootx() + 50, parent.winfo_rooty() + 50))

        self.create_widgets()

    def create_widgets(self):
        # Host
        ttk.Label(self.dialog, text="Host:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
        self.host_var = tk.StringVar(value="localhost")
        ttk.Entry(self.dialog, textvariable=self.host_var).grid(row=0, column=1, padx=10, pady=5)

        # Port
        ttk.Label(self.dialog, text="Port:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.port_var = tk.StringVar(value="27017")
        ttk.Entry(self.dialog, textvariable=self.port_var).grid(row=1, column=1, padx=10, pady=5)

        btn_frame = tk.Frame(self.dialog)
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        self.conectar_btn = ttk.Button(btn_frame, text="Conectar", command=self.ok_clicked)  # sem ()
        self.cancelar_btn = ttk.Button(btn_frame, text="Cancelar", command=self.dialog.destroy)
        self.conectar_btn.pack(side="left", padx=5)
        self.cancelar_btn.pack(side="left", padx=5)

    def ok_clicked(self):
        self.result = {
            'host': self.host_var.get(),
            'port': self.port_var.get()
        }
        print(self.result)
        self.dialog.destroy()


if __name__ == "__main__":
    main()