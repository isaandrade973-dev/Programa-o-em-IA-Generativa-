import os
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import spacy
from ultralytics import YOLO

# Classe principal da aplicação Tkinter para detecção de objetos com YOLO
class YoloScannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanner com Yolo")
        self.root.geometry("800x650")
        self.root.configure(bg="#f0f2f5")

        # Inicialização e carregamento do modelo YOLO e do processador spaCy
        self.yolo_model = self._carregar_modelo_yolo()
        self.nlp_model = self._carregar_modelo_spacy()

        # Armazenamento de estado da imagem
        self.caminho_imagem = None
        self.imagem_tk = None

        # Construção dos componentes da interface gráfica
        self._configurar_interface()

    def _carregar_modelo_yolo(self):
        """Carrega o modelo leve YOLOv8 nano para detecção rápida de objetos."""
        try:
            return YOLO("yolov8n.pt")
        except Exception as e:
            print(f"Erro ao carregar o modelo YOLO: {e}")
            return None

    def _carregar_modelo_spacy(self):
        """Carrega o modelo de processamento de linguagem natural spaCy."""
        try:
            return spacy.load("en_core_web_sm")
        except Exception:
            # Fallback caso o modelo spaCy não esteja instalado localmente
            return None

    def _configurar_interface(self):
        """Constrói o layout centralizado do Tkinter."""
        # Container centralizado
        main_frame = tk.Frame(self.root, bg="#f0f2f5")
        main_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        # Título da janela
        label_titulo = tk.Label(
            main_frame,
            text="Scanner com Yolo",
            font=("Helvetica", 18, "bold"),
            bg="#f0f2f5",
            fg="#1a1a1a"
        )
        label_titulo.pack(pady=(0, 15))

        # Painel para exibição da imagem
        self.panel_imagem = tk.Label(
            main_frame,
            text="Nenhuma imagem selecionada",
            bg="#e4e7eb",
            width=60,
            height=15,
            relief=tk.RIDGE
        )
        self.panel_imagem.pack(pady=10, fill=tk.BOTH, expand=True)

        # Botão para seleção de imagem
        btn_carregar = tk.Button(
            main_frame,
            text="Selecionar Imagem",
            command=self.selecionar_imagem,
            font=("Helvetica", 12, "bold"),
            bg="#0066cc",
            fg="white",
            padx=15,
            pady=8,
            relief=tk.FLAT,
            cursor="hand2"
        )
        btn_carregar.pack(pady=10)

        # Exibição dos resultados e objetos detectados
        label_resultado = tk.Label(
            main_frame,
            text="Objetos Detectados:",
            font=("Helvetica", 12, "bold"),
            bg="#f0f2f5"
        )
        label_resultado.pack(anchor="w", pady=(10, 5))

        self.txt_resultado = tk.Text(
            main_frame,
            height=6,
            font=("Courier", 10),
            bg="#ffffff",
            relief=tk.SOLID,
            bd=1
        )
        self.txt_resultado.pack(fill=tk.X, pady=(0, 10))

    def selecionar_imagem(self):
        """Abre o seletor de arquivos e executa a detecção de objetos."""
        tipos_arquivo = [("Imagens", "*.jpg *.jpeg *.png *.bmp")]
        caminho = filedialog.askopenfilename(title="Escolha uma Imagem", filetypes=tipos_arquivo)

        if caminho:
            self.caminho_imagem = caminho
            self._exibir_preview_imagem(caminho)
            self._processar_deteccao()

    def _exibir_preview_imagem(self, caminho):
        """Redimensiona e renderiza a imagem no painel Tkinter."""
        imagem_pil = Image.open(caminho)
        imagem_pil.thumbnail((500, 300))
        self.imagem_tk = ImageTk.PhotoImage(imagem_pil)
        self.panel_imagem.config(image=self.imagem_tk, text="")

    def _processar_deteccao(self):
        """Executa a inferência YOLO para identificar os objetos presentes na imagem."""
        if not self.yolo_model or not self.caminho_imagem:
            return

        # Inferência do YOLO na imagem
        resultados = self.yolo_model(self.caminho_imagem)
        objetos_detectados = []

        # Extração das classes rotuladas pelo modelo
        for resultado in resultados:
            for box in resultado.boxes:
                cls_id = int(box.cls[0])
                nome_classe = self.yolo_model.names[cls_id]
                objetos_detectados.append(nome_classe)

        # Formatação do resultado com spaCy ou texto simples
        texto_deteccao = ", ".join(objetos_detectados) if objetos_detectados else "Nenhum objeto detectado."
        
        if self.nlp_model and objetos_detectados:
            doc = self.nlp_model(texto_deteccao)
            texto_formatado = f"Total de Objetos: {len(objetos_detectados)}\nClasses identificadas: {texto_deteccao}"
        else:
            texto_formatado = f"Total de Objetos: {len(objetos_detectados)}\nClasses identificadas: {texto_deteccao}"

        # Atualização do componente visual de texto
        self.txt_resultado.delete("1.0", tk.END)
        self.txt_resultado.insert(tk.END, texto_formatado)


if __name__ == "__main__":
    # Inicialização da janela principal Tkinter
    root = tk.Tk()
    app = YoloScannerApp(root)
    root.mainloop()