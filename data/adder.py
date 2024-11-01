import json
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# Load data from JSON file
def load_data():
    try:
        with open('contenu.json', 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Save data to JSON file
def save_data(data):
    with open('contenu.json', 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Update series list
def update_series_list():
    series_listbox.delete(0, tk.END)
    for series in data:
        series_listbox.insert(tk.END, series["title"])

# Update episodes list for the selected series and season
def update_episodes_list(selected_series):
    episodes_listbox.delete(0, tk.END)
    season_index = season_combobox.current()  # Get the currently selected season index
    episodes = selected_series.get('seasons', [])[season_index].get('episodes', [])
    for episode in episodes:
        episodes_listbox.insert(tk.END, episode["title"])

# Update seasons list for selected series
def update_season_combobox(selected_series):
    season_combobox['values'] = [season["season"] for season in selected_series.get('seasons', [])]
    if selected_series.get('seasons'):
        season_combobox.current(0)  # Default to the first season
        update_episodes_list(selected_series)  # Update episodes for the first season

# Show form for adding or editing series
def show_series_form(edit=False):
    form_window = tk.Toplevel(root)
    form_window.title("Ajouter/Modifier une Série")
    form_window.configure(bg="#121212")

    tk.Label(form_window, text="Titre:", bg="#121212", fg="white").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(form_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_window, text="Description:", bg="#121212", fg="white").grid(row=1, column=0, padx=5, pady=5)
    description_entry = tk.Entry(form_window)
    description_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(form_window, text="Image:", bg="#121212", fg="white").grid(row=2, column=0, padx=5, pady=5)
    image_entry = tk.Entry(form_window)
    image_entry.grid(row=2, column=1, padx=5, pady=5)

    if edit:
        title_entry.insert(0, current_series["title"])
        description_entry.insert(0, current_series["description"])
        image_entry.insert(0, current_series["image"])

    def submit_series():
        title = title_entry.get()
        description = description_entry.get()
        image = image_entry.get()

        if not title or not description or not image:
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return

        if edit:
            current_series["title"] = title
            current_series["description"] = description
            current_series["image"] = image
        else:
            series = {
                "title": title,
                "description": description,
                "image": image,
                "seasons": [{"season": "Saison 1", "episodes": []}]
            }
            data.append(series)

        save_data(data)
        update_series_list()
        update_season_combobox(current_series)  # Update the season combobox if necessary
        form_window.destroy()

    tk.Button(form_window, text="Soumettre", command=submit_series, bg="#8b0000", fg="white").grid(row=3, columnspan=2, pady=10)

# Show form for adding or editing episodes
def show_episode_form(edit=False):
    if not current_series:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une série.")
        return

    form_window = tk.Toplevel(root)
    form_window.title("Ajouter/Modifier un Épisode")
    form_window.configure(bg="#121212")

    tk.Label(form_window, text="Titre de l'épisode:", bg="#121212", fg="white").grid(row=0, column=0, padx=5, pady=5)
    title_entry = tk.Entry(form_window)
    title_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(form_window, text="Lien:", bg="#121212", fg="white").grid(row=1, column=0, padx=5, pady=5)
    link_entry = tk.Entry(form_window)
    link_entry.grid(row=1, column=1, padx=5, pady=5)

    if edit:
        episode_index = episodes_listbox.curselection()[0]
        episode = current_series['seasons'][season_combobox.current()]['episodes'][episode_index]
        title_entry.insert(0, episode["title"])
        link_entry.insert(0, episode["link"])

    def submit_episode():
        title = title_entry.get()
        link = link_entry.get()

        if not title or not link:
            messagebox.showwarning("Erreur", "Tous les champs doivent être remplis.")
            return

        if edit:
            episode = current_series['seasons'][season_combobox.current()]['episodes'][episode_index]
            episode["title"] = title
            episode["link"] = link
        else:
            current_series['seasons'][season_combobox.current()]['episodes'].append({
                "title": title,
                "link": link
            })

        save_data(data)
        update_episodes_list(current_series)
        form_window.destroy()

    tk.Button(form_window, text="Soumettre", command=submit_episode, bg="#8b0000", fg="white").grid(row=2, columnspan=2, pady=10)

# Function to delete an episode
def delete_episode():
    if not current_series:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une série.")
        return

    episode_index = episodes_listbox.curselection()
    if not episode_index:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner un épisode à supprimer.")
        return

    season_index = season_combobox.current()
    del current_series['seasons'][season_index]['episodes'][episode_index[0]]

    save_data(data)
    update_episodes_list(current_series)

# Add a new season
def add_season():
    if not current_series:
        messagebox.showwarning("Avertissement", "Veuillez sélectionner une série.")
        return
    
    season_title = simpledialog.askstring("Titre de la saison", "Entrez le titre de la saison:")
    
    if not season_title:
        messagebox.showwarning("Erreur", "Le titre de la saison ne peut pas être vide.")
        return
    
    current_series['seasons'].append({"season": season_title, "episodes": []})
    save_data(data)
    update_series_list()
    update_season_combobox(current_series)  # Update the season combobox for the new season

# Function to handle series selection change
def on_series_select(event):
    global current_series
    selected_index = series_listbox.curselection()
    if selected_index:
        current_series = data[selected_index[0]]
        current_series_label.config(text=f"Série sélectionnée: {current_series['title']}")
        update_season_combobox(current_series)  # Update seasons when a series is selected

# Function to handle season selection change
def on_season_select(event):
    if current_series:
        update_episodes_list(current_series)

# Create main window
root = tk.Tk()
root.title("Gestionnaire d'Animes")
root.configure(bg="#121212")

# Create a style
style = ttk.Style()
style.theme_use("clam")
style.configure("TButton", padding=6, relief="flat", background="#8b0000", foreground="white", borderwidth=0)
style.map("TButton", background=[("active", "#a00000")])
style.configure("TLabel", background="#121212", foreground="white")
style.configure("TFrame", background="#121212")
style.configure("TListbox", background="#444", foreground="white", selectbackground="#8b0000", selectforeground="white", borderwidth=0)

# Create custom styles for LabelFrames
style.configure("Custom.TLabelframe", background="#121212", bordercolor="#121212", foreground="white")
style.map("Custom.TLabelframe", background=[("active", "#121212")])

# Series frame
series_frame = ttk.LabelFrame(root, text="Séries", padding=(10, 10), style="Custom.TLabelframe")
series_frame.pack(padx=10, pady=10, fill="both", expand="yes")
series_frame.configure(borderwidth=0)

# Series list
series_listbox = tk.Listbox(series_frame, width=50, height=10)
series_listbox.pack(padx=5, pady=5)
series_listbox.bind("<<ListboxSelect>>", on_series_select)

# Display selected series
current_series_label = tk.Label(root, text="Série sélectionnée: Aucune", font=("Arial", 10, "bold"))
current_series_label.pack(pady=5)

# Seasons selection
season_combobox = ttk.Combobox(root, values=[], state="readonly")
season_combobox.pack(pady=5)
season_combobox.bind("<<ComboboxSelected>>", on_season_select)  # Bind the selection event to update episodes

# Episodes frame
episodes_frame = ttk.LabelFrame(root, text="Épisodes", padding=(10, 10), style="Custom.TLabelframe")
episodes_frame.pack(padx=10, pady=10, fill="both", expand="yes")
episodes_frame.configure(borderwidth=0)

# Episodes list
episodes_listbox = tk.Listbox(episodes_frame, width=50, height=10)
episodes_listbox.pack(padx=5, pady=5)

# Make the listbox more visually appealing
series_listbox.config(bg="#444", fg="white", highlightbackground="#444", highlightcolor="#444", selectbackground="#8b0000", selectforeground="white")
episodes_listbox.config(bg="#444", fg="white", highlightbackground="#444", highlightcolor="#444", selectbackground="#8b0000", selectforeground="white")

# Initialize data and current series
data = load_data()
current_series = None
update_series_list()

# Buttons to add series and episodes
button_frame = tk.Frame(root, bg="#121212")
button_frame.pack(pady=10)

add_series_button = tk.Button(button_frame, text="Ajouter une Série", command=lambda: show_series_form(edit=False), bg="#8b0000", fg="white")
add_series_button.pack(side=tk.LEFT, padx=5)

# Remove the edit series button and add delete episode button
delete_episode_button = tk.Button(button_frame, text="Supprimer l'Épisode", command=delete_episode, bg="#8b0000", fg="white")
delete_episode_button.pack(side=tk.LEFT, padx=5)

add_episode_button = tk.Button(button_frame, text="Ajouter un Épisode", command=lambda: show_episode_form(edit=False), bg="#8b0000", fg="white")
add_episode_button.pack(side=tk.LEFT, padx=5)

edit_episode_button = tk.Button(button_frame, text="Modifier l'Épisode", command=lambda: show_episode_form(edit=True), bg="#8b0000", fg="white")
edit_episode_button.pack(side=tk.LEFT, padx=5)

add_season_button = tk.Button(button_frame, text="Ajouter une Saison", command=add_season, bg="#8b0000", fg="white")
add_season_button.pack(side=tk.LEFT, padx=5)

root.mainloop()
