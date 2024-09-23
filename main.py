import sqlite3
from tkinter import *
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
import os

# Conexão com o banco de dados
conn = sqlite3.connect('petshop.db')
cursor = conn.cursor()

# Criar a tabela (se não existir)
cursor.execute('''
    CREATE TABLE IF NOT EXISTS animais (
        cod_animal INTEGER PRIMARY KEY AUTOINCREMENT,
        animal TEXT,
        especie TEXT,
        raca TEXT,
        cor_predom TEXT,
        nascimento DATE,
        observacao TEXT,
        foto_animal TEXT,
        tutor TEXT,
        fone TEXT
    )
''')
conn.commit()

# Variável global para armazenar o caminho da imagem
imagem_path = None

# Função para salvar a imagem e retornar o caminho
def salvar_imagem(imagem):
    caminho_imagem = "imagens/"  # Diretório onde as imagens serão salvas
    if not os.path.exists(caminho_imagem):
        os.makedirs(caminho_imagem)
    imagem_path = os.path.join(caminho_imagem, "imagem.jpg")  # Nome fixo para simplificação
    imagem.save(imagem_path)
    return imagem_path

# Função para selecionar a imagem
def selecionar_imagem():
    global imagem_path
    caminho_arquivo = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
    if caminho_arquivo:
        imagem_path = caminho_arquivo
        imagem = Image.open(imagem_path)
        imagem = imagem.resize((200, 200), Image.Resampling.LANCZOS)
        imagem_tk = ImageTk.PhotoImage(imagem)
        label_imagem.config(image=imagem_tk)
        label_imagem.image = imagem_tk

# Funções para interagir com o banco de dados
def criar_animal():
    global imagem_path
    nome = nome_entry.get()
    especie = especie_entry.get()
    raca = raca_entry.get()
    cor_predom = cor_predom_entry.get()
    nascimento = nascimento_entry.get()
    observacao = observacao_text.get("1.0", END).strip()
    tutor = tutor_entry.get()
    fone = fone_entry.get()

    # Caso não tenha uma imagem carregada, defina como uma string vazia
    imagem_final_path = imagem_path if imagem_path else ""

    cursor.execute('''
        INSERT INTO animais (animal, especie, raca, cor_predom, nascimento, observacao, foto_animal, tutor, fone)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (nome, especie, raca, cor_predom, nascimento, observacao, imagem_final_path, tutor, fone))
    conn.commit()

    messagebox.showinfo("Sucesso", "Animal cadastrado com sucesso!")

def consultar_animal():
    global imagem_path
    cod_animal = codigo_entry.get()
    
    cursor.execute('SELECT * FROM animais WHERE cod_animal = ?', (cod_animal,))
    resultado = cursor.fetchone()

    if resultado:
        nome_entry.delete(0, END)
        nome_entry.insert(0, resultado[1])
        especie_entry.delete(0, END)
        especie_entry.insert(0, resultado[2])
        raca_entry.delete(0, END)
        raca_entry.insert(0, resultado[3])
        cor_predom_entry.delete(0, END)
        cor_predom_entry.insert(0, resultado[4])
        nascimento_entry.delete(0, END)
        nascimento_entry.insert(0, resultado[5])
        observacao_text.delete("1.0", END)
        observacao_text.insert("1.0", resultado[6])
        tutor_entry.delete(0, END)
        tutor_entry.insert(0, resultado[8])
        fone_entry.delete(0, END)
        fone_entry.insert(0, resultado[9])

        # Carregar e exibir a imagem
        imagem_path = resultado[7]
        if imagem_path and os.path.exists(imagem_path):
            imagem = Image.open(imagem_path)
            imagem = imagem.resize((200, 200), Image.Resampling.LANCZOS)
            imagem_tk = ImageTk.PhotoImage(imagem)
            label_imagem.config(image=imagem_tk)
            label_imagem.image = imagem_tk

        # Atualizar o rótulo com o caminho da imagem
        caminho_imagem_label.config(text=f"Caminho da Imagem: {imagem_path}")

        messagebox.showinfo("Sucesso", "Animal encontrado com sucesso!")
    else:
        messagebox.showinfo("Erro", "Animal não encontrado.")
        limpar_campos()

def atualizar_animal():
    global imagem_path
    cod_animal = codigo_entry.get()
    nome = nome_entry.get()
    especie = especie_entry.get()
    raca = raca_entry.get()
    cor_predom = cor_predom_entry.get()
    nascimento = nascimento_entry.get()
    observacao = observacao_text.get("1.0", END).strip() 
    tutor = tutor_entry.get()
    fone = fone_entry.get()

    # Caso não tenha uma imagem carregada, defina como uma string vazia
    imagem_final_path = imagem_path if imagem_path else ""

    cursor.execute('''
        UPDATE animais
        SET animal = ?, especie = ?, raca = ?, cor_predom = ?, nascimento = ?, observacao = ?, foto_animal = ?, tutor = ?, fone = ?
        WHERE cod_animal = ?
    ''', (nome, especie, raca, cor_predom, nascimento, observacao, imagem_final_path, tutor, fone, cod_animal))
    conn.commit()

    messagebox.showinfo("Sucesso", "Animal atualizado com sucesso!")

def excluir_animal():
    cod_animal = codigo_entry.get()
    resposta = messagebox.askyesno("Confirmação", "Tem certeza que deseja excluir este animal?")
    if resposta:
        cursor.execute('DELETE FROM animais WHERE cod_animal = ?', (cod_animal,))
        conn.commit()
        messagebox.showinfo("Sucesso", "Animal excluído com sucesso!")
        limpar_campos()
    else:
        messagebox.showinfo("Cancelado", "A exclusão do animal foi cancelada.")

def contar_animais():
    cursor.execute('SELECT COUNT(*) FROM animais')
    total_animais = cursor.fetchone()[0]
    messagebox.showinfo("Total de Animais", f"Total de animais cadastrados: {total_animais}")

def limpar_campos():
    nome_entry.delete(0, END)
    especie_entry.delete(0, END)
    raca_entry.delete(0, END)
    cor_predom_entry.delete(0, END)
    nascimento_entry.delete(0, END)
    observacao_text.delete("1.0", END) 
    tutor_entry.delete(0, END)
    fone_entry.delete(0, END)
    label_imagem.config(image='')  
    caminho_imagem_label.config(text="Caminho da Imagem:")

# Interface gráfica
root = Tk()
root.title("Sistema Petshop")

# Tamanho padrão dos botões
button_width = 15
button_height = 2

# Configuração da interface
frame_campos = Frame(root)
frame_campos.pack(padx=10, pady=10)

# Criar os elementos da interface
Label(frame_campos, text="Código do Animal:").grid(row=0, column=0, sticky=E, padx=5, pady=5)
codigo_entry = Entry(frame_campos)
codigo_entry.grid(row=0, column=1, padx=5, pady=5)

Label(frame_campos, text="Animal:").grid(row=1, column=0, sticky=E, padx=5, pady=5)
nome_entry = Entry(frame_campos)
nome_entry.grid(row=1, column=1, padx=5, pady=5)

Label(frame_campos, text="Espécie:").grid(row=2, column=0, sticky=E, padx=5, pady=5)
especie_entry = Entry(frame_campos)
especie_entry.grid(row=2, column=1, padx=5, pady=5)

Label(frame_campos, text="Raça:").grid(row=3, column=0, sticky=E, padx=5, pady=5)
raca_entry = Entry(frame_campos)
raca_entry.grid(row=3, column=1, padx=5, pady=5)

Label(frame_campos, text="Cor Predominante:").grid(row=4, column=0, sticky=E, padx=5, pady=5)
cor_predom_entry = Entry(frame_campos)
cor_predom_entry.grid(row=4, column=1, padx=5, pady=5)

Label(frame_campos, text="Nascimento:").grid(row=5, column=0, sticky=E, padx=5, pady=5)
nascimento_entry = Entry(frame_campos)
nascimento_entry.grid(row=5, column=1, padx=5, pady=5)

Label(frame_campos, text="Observação:").grid(row=6, column=0, sticky=NE, padx=5, pady=5)
observacao_text = Text(frame_campos, height=4, width=30)
observacao_text.grid(row=6, column=1, padx=5, pady=5)

Label(frame_campos, text="Tutor:").grid(row=7, column=0, sticky=E, padx=5, pady=5)
tutor_entry = Entry(frame_campos)
tutor_entry.grid(row=7, column=1, padx=5, pady=5)

Label(frame_campos, text="Fone:").grid(row=8, column=0, sticky=E, padx=5, pady=5)
fone_entry = Entry(frame_campos)
fone_entry.grid(row=8, column=1, padx=5, pady=5)

# Imagem
frame_imagem = Frame(root)
frame_imagem.pack(padx=10, pady=10)

Label(frame_imagem, text="Foto Animal:").pack()

label_imagem = Label(frame_imagem)
label_imagem.pack(pady=5)

btn_selecionar_imagem = Button(frame_imagem, text="Selecionar Imagem", command=selecionar_imagem)
btn_selecionar_imagem.pack()

caminho_imagem_label = Label(frame_imagem, text="Caminho da Imagem:")
caminho_imagem_label.pack()

# Botões
frame_botoes = Frame(root)
frame_botoes.pack(padx=10, pady=10)

btn_criar = Button(frame_botoes, text="Criar", command=criar_animal, width=button_width, height=button_height)
btn_criar.grid(row=0, column=0, padx=5, pady=5)

btn_consultar = Button(frame_botoes, text="Consultar", command=consultar_animal, width=button_width, height=button_height)
btn_consultar.grid(row=0, column=1, padx=5, pady=5)

btn_atualizar = Button(frame_botoes, text="Atualizar", command=atualizar_animal, width=button_width, height=button_height)
btn_atualizar.grid(row=0, column=2, padx=5, pady=5)

btn_excluir = Button(frame_botoes, text="Excluir", command=excluir_animal, width=button_width, height=button_height)
btn_excluir.grid(row=0, column=3, padx=5, pady=5)

btn_contar = Button(frame_botoes, text="Contar Animais", command=contar_animais, width=button_width, height=button_height)
btn_contar.grid(row=1, column=1, padx=5, pady=5)

btn_limpar = Button(frame_botoes, text="Limpar Campos", command=limpar_campos, width=button_width, height=button_height)
btn_limpar.grid(row=1, column=2, padx=5, pady=5)

root.mainloop()
