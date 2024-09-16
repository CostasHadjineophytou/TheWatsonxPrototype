import tkinter as tk
from tkinter import ttk, messagebox
from logic.nlu_services import analyze_text

def create_nlu_tab(app):
    label = tk.Label(app.nlu_tab, text="Enter text:")
    app.text_input = tk.Text(app.nlu_tab, height=10, width=50)
    app.option_var = tk.StringVar()
    app.option_var.set("sentiment")
    
    options = [
        "sentiment",
        "emotion",
        "entities",
        "keywords",
        "categories",
        "concepts",
        "relations",
        "semantic_roles",
        "all"
    ]
    
    option_menu = ttk.OptionMenu(app.nlu_tab, app.option_var, options[0], *options)
    analyze_button = tk.Button(app.nlu_tab, text="Analyze", command=app.analyze_text_ui)
    
    result_frame = tk.Frame(app.nlu_tab)
    
    app.sentiment_label = tk.Label(result_frame, text="Sentiment: ")
    app.emotion_label = tk.Label(result_frame, text="Emotion: ")
    app.language_label = tk.Label(result_frame, text="Language: ")
    app.entities_label = tk.Label(result_frame, text="Entities: ")
    app.keywords_label = tk.Label(result_frame, text="Keywords: ")
    app.categories_label = tk.Label(result_frame, text="Categories: ")
    app.concepts_label = tk.Label(result_frame, text="Concepts: ")
    app.relations_label = tk.Label(result_frame, text="Relations: ")
    app.semantic_roles_label = tk.Label(result_frame, text="Semantic Roles: ")
    
    label.pack()
    app.text_input.pack()
    option_menu.pack()
    analyze_button.pack()
    result_frame.pack()
    
    app.sentiment_label.grid(row=0, column=0, sticky="w")
    app.emotion_label.grid(row=1, column=0, sticky="w")
    app.language_label.grid(row=2, column=0, sticky="w")
    app.entities_label.grid(row=3, column=0, sticky="w")
    app.keywords_label.grid(row=4, column=0, sticky="w")
    app.categories_label.grid(row=5, column=0, sticky="w")
    app.concepts_label.grid(row=6, column=0, sticky="w")
    app.relations_label.grid(row=7, column=0, sticky="w")
    app.semantic_roles_label.grid(row=8, column=0, sticky="w")

def analyze_text_ui(app):
    text = app.text_input.get("1.0", "end-1c")
    analysis_type = app.option_var.get()
    print(f"Analyzing text: {text} with analysis_type: {analysis_type}")
    result = analyze_text(text, analysis_type)
    if result:
        app.update_labels(result)
    else:
        messagebox.showerror("Analysis Failed", "Error occurred during analysis.")

def update_labels(app, result):
    def set_label(label, text, is_na):
        label.config(text=text)
        if is_na:
            label.config(fg="grey")
        else:
            label.config(fg="black")

    if "sentiment" in result:
        sentiment = result["sentiment"]["document"]["label"]
        set_label(app.sentiment_label, f"Sentiment: {sentiment}", False)
    else:
        set_label(app.sentiment_label, "Sentiment: N/A", True)
    
    if "emotion" in result:
        emotions = result["emotion"]["document"]["emotion"]
        emotion_str = ", ".join([f"{k}: {v:.2f}" for k, v in emotions.items()])
        set_label(app.emotion_label, f"Emotion: {emotion_str}", False)
    else:
        set_label(app.emotion_label, "Emotion: N/A", True)
    
    if "language" in result:
        language = result["language"]
        set_label(app.language_label, f"Language: {language}", False)
    else:
        set_label(app.language_label, "Language: N/A", True)
    
    if "entities" in result:
        entities = result["entities"]
        entities_str = ", ".join([entity["text"] for entity in entities])
        set_label(app.entities_label, f"Entities: {entities_str}", False)
    else:
        set_label(app.entities_label, "Entities: N/A", True)
    
    if "keywords" in result:
        keywords = result["keywords"]
        keywords_str = ", ".join([keyword["text"] for keyword in keywords])
        set_label(app.keywords_label, f"Keywords: {keywords_str}", False)
    else:
        set_label(app.keywords_label, "Keywords: N/A", True)
    
    if "categories" in result:
        categories = result["categories"]
        categories_str = ", ".join([category["label"] for category in categories])
        set_label(app.categories_label, f"Categories: {categories_str}", False)
    else:
        set_label(app.categories_label, "Categories: N/A", True)
    
    if "concepts" in result:
        concepts = result["concepts"]
        concepts_str = ", ".join([concept["text"] for concept in concepts])
        set_label(app.concepts_label, f"Concepts: {concepts_str}", False)
    else:
        set_label(app.concepts_label, "Concepts: N/A", True)
    
    if "relations" in result:
        relations = result["relations"]
        relations_str = ", ".join([f"{relation['type']} between {relation['arguments'][0]['text']} and {relation['arguments'][1]['text']}" for relation in relations])
        set_label(app.relations_label, f"Relations: {relations_str}", False)
    else:
        set_label(app.relations_label, "Relations: N/A", True)
    
    if "semantic_roles" in result:
        semantic_roles = result["semantic_roles"]
        semantic_roles_str = ", ".join([f"{role['subject']['text']} {role['action']['verb']['text']} {role['object']['text']}" for role in semantic_roles])
        set_label(app.semantic_roles_label, f"Semantic Roles: {semantic_roles_str}", False)
    else:
        set_label(app.semantic_roles_label, "Semantic Roles: N/A", True)