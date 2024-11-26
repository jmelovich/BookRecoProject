import tkinter as tk
from PIL import Image, ImageTk
import requests
from io import BytesIO

genres_autocomplete_list = []
authors_autocomplete_list = []
bookformats_autocomplete_list = []
titles_autocomplete_list = []


def load_genre_list():
    # Open the file and read each line into the list
    with open('data/unique_genres.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Strip any whitespace or newline characters and append to the list
            genres_autocomplete_list.append(line.strip())


def load_author_list():
    with open('data/unique_authors.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Strip any whitespace or newline characters and append to the list
            authors_autocomplete_list.append(line.strip())


def load_bookformat_list():
    with open('data/unique_bookformats.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Strip any whitespace or newline characters and append to the list
            bookformats_autocomplete_list.append(line.strip())


def load_title_list():
    with open('data/unique_titles.txt', 'r', encoding='utf-8') as f:
        for line in f:
            # Strip any whitespace or newline characters and append to the list
            titles_autocomplete_list.append(line.strip())


# Function for creating and displaying text on the program's window
def create_label(parent, text, font, background, row, column):
    label = tk.Label(parent, text=text, font=font, background=background)
    label.grid(row=row, column=column, sticky='w', padx=10, pady=5)
    return label


# Function for creating functional text boxes to store user inputs
def create_entry(parent, width, row, column):
    entry = tk.Entry(parent, width=width)
    entry.grid(row=row, column=column, padx=10, pady=5)
    return entry


# Function for creating button that activate additional functions when pressed
def create_button(parent, text, command, font, width, height, row, column):
    button = tk.Button(parent, text=text, command=command, font=font, width=width, height=height)
    button.grid(row=row, column=column, padx=10, pady=5)
    return button


# Function for creating drop down menus to store different program operations
def create_option_menu(parent, options, default, row, column):
    var = tk.StringVar(parent)
    var.set(default)
    option_menu = tk.OptionMenu(parent, var, *options)
    option_menu.grid(row=row, column=column, padx=10, pady=5)
    return var


# Function that takes in an image url and returns a colored image that can be displayed on the UI.
def loadImageFromURL(url, root):
    if not isinstance(url, str):
        return None
    if not url.startswith("http"):
        return None
    response = requests.get(url)
    image = Image.open(BytesIO(response.content))
    return ImageTk.PhotoImage(image, master=root)


# Function to desplay information as users hover their mouse over book images
def on_hover(event, title, author, rating):
    event.widget.config(relief="raised", bd=0)
    tooltip = tk.Toplevel(event.widget)
    tooltip.wm_overrideredirect(True)
    tooltip.wm_geometry(f"+{event.widget.winfo_rootx()}+{event.widget.winfo_rooty()}")
    label = tk.Label(tooltip, text=f"{title}\n{author}\nRating: {rating}", background="yellow", relief="solid", borderwidth=1)
    label.pack()
    event.widget.tooltip = tooltip


# Function to handle when users try to escape from the program
def on_leave(event):
    event.widget.config(relief="flat", bd=0)
    if hasattr(event.widget, 'tooltip'):
        event.widget.tooltip.destroy()
        del event.widget.tooltip


# Class for storing all elements used to develop the front end UI
class BookGridUI:
    def __init__(self, root):
        self.root = root
        self.grid_columns = 3
        self.img_width = 130
        self.img_height = self.img_width * (20/15)
        
        self.grid_canvas = tk.Canvas(root, bg='#172038')
        self.grid_canvas.pack(side='right', fill='both', expand=True)

        self.grid_frame = tk.Frame(self.grid_canvas, bg='#172038')
        self.grid_window = self.grid_canvas.create_window((0, 0), window=self.grid_frame, anchor='nw')

        self.scrollbar = tk.Scrollbar(root, orient="vertical", command=self.grid_canvas.yview)
        self.grid_canvas.configure(yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side='right', fill='y')

        self.grid_frame.bind("<Configure>", self.on_frame_configure)
        self.grid_canvas.bind_all("<MouseWheel>", 
            lambda event: self.grid_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

    # Function to update the scroll region for the grid as the window changes
    def on_frame_configure(self, event):
        self.grid_canvas.configure(scrollregion=self.grid_canvas.bbox("all"))

    # Function to adjust the number of columns in the grid
    def adjust_grid(self, event):
        self.grid_canvas.update_idletasks()
        width = self.grid_canvas.winfo_width()
        new_columns = max(1, width // 150)
        if new_columns != self.grid_columns:
            self.grid_columns = new_columns
            self.rearrange_grid()

    # Function to reorganize all UI elements to fit in the window's grid
    def rearrange_grid(self):
        children = self.grid_frame.winfo_children()
        for index, widget in enumerate(children):
            widget.grid_forget()
            widget.grid(row=index // self.grid_columns, 
                       column=index % self.grid_columns, 
                       padx=5, pady=5, sticky="nsew")

    # Function to add and update elements displayed on the window's grid
    def populate_grid(self, dataframe, on_click_callback):
        for widget in self.grid_frame.winfo_children():
            widget.destroy()
            
        for index, row in dataframe.iterrows():
            image = loadImageFromURL(row['img'], self.root)
            if image is not None:
                image = image._PhotoImage__photo.subsample(
                    max(1, int(image.height() // self.img_height)))
                label = tk.Label(
                    self.grid_frame,
                    image=image,
                    background="#3C5291",
                    width=self.img_width,
                    height=self.img_height
                )
            else:
                image = ImageTk.PhotoImage(Image.new('RGB', 
                    (int(self.img_width), int(self.img_height)), 
                    color='#172038'))
                label = tk.Label(
                    self.grid_frame,
                    image=image,
                    text=row['title'],
                    compound='center',
                    background="#3C5291",
                    fg="white",
                    wraplength=self.img_width,
                    justify="center",
                    width=self.img_width,
                    height=self.img_height
                )

            label.image = image
            label.grid(row=index // self.grid_columns, 
                      column=index % self.grid_columns, 
                      padx=5, pady=5, sticky="nsew")
            label.bind("<Enter>", 
                lambda event, title=row['title'], 
                author=row['author'], 
                rating=row['rating']: on_hover(event, title, author, rating))
            label.bind("<Leave>", on_leave)
            label.bind("<Button-1>", 
                lambda event, idx=index: on_click_callback(event, idx))
            label.row_index = index
            self.root.update()
            
            
class CustomAutocompleteEntry(tk.Entry):
    def __init__(self, master=None, completevalues=None, add_callback=None, **kwargs):
        self.string_var = tk.StringVar()
        super().__init__(master, textvariable=self.string_var, **kwargs)
        
        self.completevalues = completevalues or []
        self.filled = False
        self.add_callback = add_callback
        
        # Create dropdown listbox in a top-level window
        self.dropdown = tk.Toplevel(master)
        self.dropdown.withdraw()  # Hide initially
        self.dropdown.overrideredirect(True)  # Remove window decorations
        self.dropdown.attributes('-topmost', True)  # Keep on top
        
        self.listbox = tk.Listbox(self.dropdown, width=self['width'], 
                                 font=kwargs.get('font', None),
                                 background='white', 
                                 selectmode=tk.SINGLE)
        self.listbox.pack(fill=tk.BOTH, expand=True)
        
        # Bind events
        self.bind('<KeyRelease>', self._on_key_release)
        self.bind('<Key>', self._on_key_press)
        self.bind('<FocusOut>', lambda e: self._schedule_hide())
        self.bind('<Tab>', self._on_tab)
        self.bind('<Return>', self._on_enter)
        self.bind('<Escape>', lambda e: self._hide_listbox())
        self.bind('<Down>', self._on_down)
        self.bind('<Up>', self._on_up)
        
        self.listbox.bind('<<ListboxSelect>>', self._on_select)
        self.listbox.bind('<Enter>', lambda e: self.focus_set())
        
        # Add a small delay before hiding to allow for clicks
        self._hide_after_id = None
    
    def _schedule_hide(self):
        if self._hide_after_id:
            self.dropdown.after_cancel(self._hide_after_id)
        self._hide_after_id = self.dropdown.after(100, self._hide_listbox)
    
    def _match_string(self):
        hits = []
        current_text = self.string_var.get().lower()
        if current_text:
            for item in self.completevalues:
                if item.lower().startswith(current_text):
                    hits.append(item)
        return hits
    
    def _show_listbox(self, hits):
        if not hits:
            self._hide_listbox()
            return
        
        # Position dropdown below entry
        x = self.winfo_rootx()
        y = self.winfo_rooty() + self.winfo_height()
        self.dropdown.geometry(f"+{x}+{y}")
        
        # Update listbox contents
        self.listbox.delete(0, tk.END)
        for item in hits:
            self.listbox.insert(tk.END, item)
            
        # Select first item
        if self.listbox.size() > 0:
            self.listbox.selection_set(0)
        
        self.dropdown.deiconify()
    
    def _hide_listbox(self):
        self.dropdown.withdraw()
        if self._hide_after_id:
            self.dropdown.after_cancel(self._hide_after_id)
            self._hide_after_id = None
    
    def _on_key_release(self, event):
        # Ignore special keys
        if event.keysym in ('Up', 'Down', 'Return', 'Tab', 'Escape'):
            return
            
        hits = self._match_string()
        if hits:
            self._show_listbox(hits)
        else:
            self._hide_listbox()
    
    def _on_key_press(self, event):
        if len(event.keysym) == 1 and self.filled:
            pos = self.index(tk.INSERT)
            self.delete(pos, tk.END)
            self.filled = False
    
    def _on_select(self, event):
        if self.listbox.curselection():
            selected = self.listbox.get(self.listbox.curselection())
            self.string_var.set(selected)
            self.filled = True
            self.icursor(tk.END)
            self._hide_listbox()
    
    def _on_tab(self, event):
        if self.dropdown.winfo_viewable():
            if self.listbox.curselection():
                selected = self.listbox.get(self.listbox.curselection())
                self.string_var.set(selected)
                self.filled = True
                self.icursor(tk.END)
            self._hide_listbox()
            return 'break'  # Prevent default Tab behavior
    
    def _on_enter(self, event):
        if self.add_callback:
            self.add_callback()
        return 'break'
    
    def _on_down(self, event):
        if self.dropdown.winfo_viewable():
            if self.listbox.curselection():
                current = self.listbox.curselection()[0]
                if current < self.listbox.size() - 1:
                    self.listbox.selection_clear(current)
                    self.listbox.selection_set(current + 1)
                    self.listbox.see(current + 1)
            event.widget.focus_set()
            return 'break'
    
    def _on_up(self, event):
        if self.dropdown.winfo_viewable():
            if self.listbox.curselection():
                current = self.listbox.curselection()[0]
                if current > 0:
                    self.listbox.selection_clear(current)
                    self.listbox.selection_set(current - 1)
                    self.listbox.see(current - 1)
            event.widget.focus_set()
            return 'break'
            
    def get(self):
        return self.string_var.get()
    
    def set(self, value):
        self.string_var.set(value)