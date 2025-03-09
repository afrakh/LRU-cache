import sqlite3
from tkinter import Tk, Label, Entry, Button, messagebox, ttk, Frame, StringVar



def init_db():
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS cache (
            key INTEGER PRIMARY KEY,
            value INTEGER,
            order_index INTEGER
        )
    ''')
    conn.commit()
    conn.close()


def clear_database():
    conn = sqlite3.connect('cache.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM cache')
    conn.commit()
    conn.close()


    cache.dict.clear()
    cache.dummy_head.right = cache.dummy_tail
    cache.dummy_tail.left = cache.dummy_head

    show_cache()
    messagebox.showinfo('cache Cleared', 'The cache has been cleared.')


class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.left = None
        self.right = None


class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.misses = 0
        self.hits = 0
        self.accesses = 0
        self.dict = dict()
        self.dummy_head = Node(0, 0)
        self.dummy_tail = Node(-1, -1)
        self.dummy_head.right = self.dummy_tail
        self.dummy_tail.left = self.dummy_head
        self.load_cache_from_db()

    def load_cache_from_db(self):
        conn = sqlite3.connect('cache.db')
        cursor = conn.cursor()
        cursor.execute('SELECT key, value, order_index FROM cache ORDER BY order_index DESC')
        rows = cursor.fetchall()
        for key, value, _ in rows:
            node = Node(key, value)
            self.insert_after_node(node)
            self.dict[key] = node
        conn.close()

    def update_db(self):
        conn = sqlite3.connect('cache.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM cache')
        current = self.dummy_head.right
        order_index = 0
        while current != self.dummy_tail:
            cursor.execute('INSERT INTO cache (key, value, order_index) VALUES (?, ?, ?)',
                           (current.key, current.value, order_index))
            current = current.right
            order_index += 1
        conn.commit()
        conn.close()

    def insert_after_node(self, node):
        node.right = self.dummy_head.right
        node.left = self.dummy_head
        self.dummy_head.right.left = node
        self.dummy_head.right = node

    def delete_node(self, node):
        node.left.right = node.right
        node.right.left = node.left

    def get(self, key: int) -> int:
        self.accesses += 1
        if key in self.dict:
            self.hits += 1
            self.delete_node(self.dict[key])
            self.insert_after_node(self.dict[key])
            return self.dict[key].value
        self.misses += 1
        return -1

    def put(self, key: int, value: int) -> None:
        self.accesses += 1
        if key in self.dict:
            self.dict[key].value = value
            self.delete_node(self.dict[key])
            self.insert_after_node(self.dict[key])
        elif len(self.dict) < self.capacity:
            node = Node(key, value)
            self.insert_after_node(node)
            self.dict[key] = node
        else:
            self.misses += 1
            lru_node = self.dummy_tail.left
            self.delete_node(lru_node)
            self.dict.pop(lru_node.key)
            new_node = Node(key, value)
            self.insert_after_node(new_node)
            self.dict[key] = new_node

    def calculate_miss_and_hit_rate(self):
        if self.accesses == 0:
            return "No accesses yet."
        hit_ratio = self.hits / self.accesses
        miss_ratio = self.misses / self.accesses
        return (
            f"Total Accesses: {self.accesses}\n"
            f"Total Hits: {self.hits}\n"
            f"Total Misses: {self.misses}\n"
            f"Hit Ratio: {hit_ratio * 100:.2f}%\n"
            f"Miss Ratio: {miss_ratio * 100:.2f}%"
        )

    def traverse(self, tree_widget):
        for item in tree_widget.get_children():
            tree_widget.delete(item)

        current = self.dummy_head.right
        while current != self.dummy_tail:
            status = ''
            tags = ()
            if current == self.dummy_head.right:
                status = 'MRU'
                tags = ('mru',)
            elif current.right == self.dummy_tail:
                status = 'LRU'
                tags = ('lru',)
            tree_widget.insert('', 'end', values=(current.key, current.value, status), tags=tags)
            current = current.right



def put_key():
    try:
        key = int(key_var.get())
        value = int(value_var.get())
        cache.put(key, value)
        show_cache()
        key_var.set('')
        value_var.set('')
    except ValueError:
        messagebox.showerror('Error', 'Please enter valid integer values for key and value')


def get_value():
    try:
        key = int(get_var.get())
        value = cache.get(key)
        if value == -1:
            messagebox.showinfo('Cache Miss', f'Key {key} not found in cache.')
        else:
            messagebox.showinfo('Cache Hit', f'Value for key {key} is {value}')
        show_cache()
        get_var.set('')
    except ValueError:
        messagebox.showerror('Error', 'Please enter an integer value for key')


def show_cache():
    cache.traverse(cache_tree)
    key_entry.focus_set()


def save_cache():
    cache.update_db()
    messagebox.showinfo('Cache Saved', 'Cache successfully saved to the database.')


def show_miss_and_hit_rate():
    message = cache.calculate_miss_and_hit_rate()
    messagebox.showinfo('Cache Performance', message)


def fill_cache():
    for i in range(50):
        cache.put(i, i)
    info = "INFO AFTER FILLING CACHE WITH 50 KEYS\n" + cache.calculate_miss_and_hit_rate()
    messagebox.showinfo('Cache Performance', info)
    show_cache()


def retrieve_odd_keys():
    for j in range(1, 50, 2):
        cache.get(j)
    info = "INFO AFTER RETRIEVING ODD KEY VALUES\n" + cache.calculate_miss_and_hit_rate()
    messagebox.showinfo('Cache Performance', info)
    show_cache()


def factors(n):
    """Check if 'n' is a prime number."""
    if n <= 1:
        return False
    count = 0
    for i in range(1, n + 1):
        if n % i == 0:
            count += 1
    return count == 2


def put_factors():
    for i in range(1, 101):
        if factors(i):
            cache.put(i, i)
    messagebox.showinfo('Cache Performance', cache.calculate_miss_and_hit_rate())
    show_cache()



init_db()


cache = LRUCache(50)


root = Tk()
root.title('LRU Cache')
root.geometry('1200x700')
root.minsize(1000, 600)


root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=3)
root.rowconfigure(0, weight=1)


controls_frame = Frame(root, bg='#f0f0f0', padx=10, pady=10)
controls_frame.grid(row=0, column=0, sticky='nsew')

tree_frame = Frame(root, bg='#f0f0f0', padx=10, pady=10)
tree_frame.grid(row=0, column=1, sticky='nsew')


controls_frame.columnconfigure(0, weight=1)
controls_frame.columnconfigure(1, weight=2)
controls_frame.columnconfigure(2, weight=1)

tree_frame.columnconfigure(0, weight=1)
tree_frame.rowconfigure(1, weight=1)


key_var = StringVar()
value_var = StringVar()
get_var = StringVar()


instruction_label = Label(controls_frame, text='Enter items for your cache memory (Capacity: 50)',
                          font=('Arial', 14, 'bold'), bg='#f0f0f0')
instruction_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))

key_label = Label(controls_frame, text='Key:', font=('Arial', 12), bg='#f0f0f0')
key_label.grid(row=1, column=0, sticky='e', pady=5)

key_entry = Entry(controls_frame, textvariable=key_var, font=('Arial', 12))
key_entry.grid(row=1, column=1, sticky='w', pady=5)

value_label = Label(controls_frame, text='Value:', font=('Arial', 12), bg='#f0f0f0')
value_label.grid(row=2, column=0, sticky='e', pady=5)

value_entry = Entry(controls_frame, textvariable=value_var, font=('Arial', 12))
value_entry.grid(row=2, column=1, sticky='w', pady=5)


enter_button = Button(controls_frame, text='Enter', command=put_key, font=('Arial', 12, 'bold'), bg='#e0e0e0', width=10)
enter_button.grid(row=1, column=2, rowspan=2, padx=10, pady=5, sticky='nsew')

retrieve_label = Label(controls_frame, text='Enter key to retrieve value:', font=('Arial', 14, 'bold'), bg='#f0f0f0')
retrieve_label.grid(row=3, column=0, columnspan=3, pady=(20, 10))

get_entry = Entry(controls_frame, textvariable=get_var, font=('Arial', 12))
get_entry.grid(row=4, column=0, columnspan=2, sticky='we', pady=5)

retrieve_button = Button(controls_frame, text='Retrieve', command=get_value, font=('Arial', 12, 'bold'), bg='#e0e0e0',
                         width=10)
retrieve_button.grid(row=4, column=2, padx=10, pady=5, sticky='nsew')


action_buttons_frame = Frame(controls_frame, bg='#f0f0f0')
action_buttons_frame.grid(row=5, column=0, columnspan=2, pady=(30, 10), sticky='we')


save_button = Button(action_buttons_frame, text='Save Cache', command=save_cache, font=('Arial', 12, 'bold'),
                     bg='#e0e0e0', width=12)
save_button.grid(row=0, column=0, padx=5, pady=5)

clear_db_button = Button(action_buttons_frame, text='Clear cache', command=clear_database, font=('Arial', 12, 'bold'),
                         bg='#e0e0e0', width=15)
clear_db_button.grid(row=0, column=1, padx=5, pady=5)

rate_button = Button(action_buttons_frame, text='Show Miss/Hit Rate', command=show_miss_and_hit_rate,
                     font=('Arial', 12, 'bold'), bg='#e0e0e0', width=18)
rate_button.grid(row=0, column=2, padx=5, pady=5)

batch_buttons_frame = Frame(controls_frame, bg='#f0f0f0')
batch_buttons_frame.grid(row=6, column=0, columnspan=3, pady=(10, 10), sticky='we')


fill_cache_button = Button(batch_buttons_frame, text='Fill Cache with 50 Keys', command=fill_cache,
                           font=('Arial', 12, 'bold'), bg='#add8e6', width=20)
fill_cache_button.grid(row=0, column=0, padx=5, pady=5)


retrieve_odd_button = Button(batch_buttons_frame, text='Retrieve Odd Keys', command=retrieve_odd_keys,
                             font=('Arial', 12, 'bold'), bg='#90ee90', width=20)
retrieve_odd_button.grid(row=0, column=1, padx=5, pady=5)


put_factors_button = Button(batch_buttons_frame, text='Put primes 1-100', command=put_factors,
                            font=('Arial', 12, 'bold'), bg='#ffb6c1', width=20)
put_factors_button.grid(row=0, column=2, padx=5, pady=5)


theme_button = Button(controls_frame, text='Switch to Dark Theme', command=lambda: toggle_theme(),
                      font=('Arial', 12, 'bold'), bg='#e0e0e0', width=20)
theme_button.grid(row=7, column=0, columnspan=3, pady=(20, 0))


cache_label = Label(tree_frame, text='Cache Contents:', font=('Arial', 14, 'bold'), bg='#f0f0f0')
cache_label.pack(pady=(0, 10))


tree_scroll = ttk.Scrollbar(tree_frame)
tree_scroll.pack(side='right', fill='y')

cache_tree = ttk.Treeview(tree_frame, columns=('Key', 'Value', 'Status'), show='headings',
                          yscrollcommand=tree_scroll.set, height=20)
cache_tree.pack(fill='both', expand=True)
tree_scroll.config(command=cache_tree.yview)

cache_tree.heading('Key', text='Key')
cache_tree.heading('Value', text='Value')
cache_tree.heading('Status', text='Status')

cache_tree.column('Key', anchor='center', width=100, stretch=True)
cache_tree.column('Value', anchor='center', width=100, stretch=True)
cache_tree.column('Status', anchor='center', width=100, stretch=True)

cache_tree.tag_configure('mru', background='#b3ffb3')
cache_tree.tag_configure('lru', background='#ff9999')



def apply_light_theme():
    root.config(bg='#f0f0f0')
    controls_frame.config(bg='#f0f0f0')
    tree_frame.config(bg='#f0f0f0')

    instruction_label.config(bg='#f0f0f0', fg='black')
    key_label.config(bg='#f0f0f0', fg='black')
    value_label.config(bg='#f0f0f0', fg='black')
    retrieve_label.config(bg='#f0f0f0', fg='black')
    cache_label.config(bg='#f0f0f0', fg='black')

    for button in [enter_button, retrieve_button, save_button, clear_db_button, rate_button, theme_button,
                   fill_cache_button, retrieve_odd_button, put_factors_button]:
        button.config(bg='#e0e0e0', fg='black')

    for entry in [key_entry, value_entry, get_entry]:
        entry.config(bg='white', fg='black', insertbackground='black')

    style = ttk.Style()
    style.theme_use('default')
    style.configure('Treeview', background='white', foreground='black', fieldbackground='white')
    style.configure('Treeview.Heading', background='#e0e0e0', foreground='black', font=('Arial', 12, 'bold'))
    style.map('Treeview', background=[('selected', '#d9d9d9')], foreground=[('selected', 'black')])

    cache_tree.tag_configure('mru', background='#b3ffb3')
    cache_tree.tag_configure('lru', background='#ff9999')


def apply_dark_theme():
    root.config(bg='#2c2f38')
    controls_frame.config(bg='#2c2f38')
    tree_frame.config(bg='#2c2f38')

    instruction_label.config(bg='#2c2f38', fg='white')
    key_label.config(bg='#2c2f38', fg='white')
    value_label.config(bg='#2c2f38', fg='white')
    retrieve_label.config(bg='#2c2f38', fg='white')
    cache_label.config(bg='#2c2f38', fg='white')

    dark_button_bg = '#444c56'
    for button in [enter_button, retrieve_button, save_button, clear_db_button, rate_button, theme_button,
                   fill_cache_button, retrieve_odd_button, put_factors_button]:
        button.config(bg=dark_button_bg, fg='white')

    for entry in [key_entry, value_entry, get_entry]:
        entry.config(bg='#555c67', fg='white', insertbackground='white')

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Treeview',
                    background='#333842',
                    foreground='white',
                    fieldbackground='#333842',
                    rowheight=25)
    style.configure('Treeview.Heading',
                    background='#444c56',
                    foreground='white',
                    font=('Arial', 12, 'bold'))
    style.map('Treeview',
              background=[('selected', '#555c67')],
              foreground=[('selected', 'white')])

    cache_tree.tag_configure('mru', background='#4caf50')
    cache_tree.tag_configure('lru', background='#e57373')


def toggle_theme():
    current_text = theme_button.config('text')[-1]
    if current_text == 'Switch to Dark Theme':
        apply_dark_theme()
        theme_button.config(text='Switch to Light Theme')
    else:
        apply_light_theme()
        theme_button.config(text='Switch to Dark Theme')


apply_light_theme()
show_cache()
key_entry.focus_set()

root.mainloop()