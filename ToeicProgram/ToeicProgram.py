import tkinter as tk
from tkinter import messagebox, ttk

class VocabApp:
    def __init__(self, root):
        self.root = root
        self.root.title("영단어장")
        
        # 창 크기를 800x500으로 설정하고 고정
        self.root.geometry('900x500')
        self.root.resizable(False, False)
        
        self.word_dict = {}
        
        self.setup_ui()
    
    def setup_ui(self):
        # 스타일 설정
        self.style = ttk.Style()
        self.style.configure("TLabel", font=("Segoe UI", 12), padding=10)
        self.style.configure("TEntry", font=("Segoe UI", 12), padding=10)
        self.style.configure("TButton", font=("Segoe UI", 12), padding=10)
        self.style.configure("Treeview", font=("Segoe UI", 12), rowheight=25)
        
        self.input_frame = ttk.Frame(self.root)
        self.input_frame.pack(pady=10)

        self.words_frame = ttk.Frame(self.root)
        self.words_frame.pack(pady=10)
        
        self.quiz_frame = ttk.Frame(self.root)
        self.quiz_frame.pack(pady=10)

        # 영단어 입력 필드
        self.eng_label = ttk.Label(self.input_frame, text="영단어:", font=("Segoe UI", 14))
        self.eng_label.pack(side=tk.LEFT)

        self.eng_entry = ttk.Entry(self.input_frame, font=("Segoe UI", 12))
        self.eng_entry.pack(side=tk.LEFT)

        # 한국어 뜻 입력 필드
        self.kor_label = ttk.Label(self.input_frame, text="한국어 뜻:", font=("Segoe UI", 14))
        self.kor_label.pack(side=tk.LEFT)

        self.kor_entry = ttk.Entry(self.input_frame, font=("Segoe UI", 12))
        self.kor_entry.pack(side=tk.LEFT)

        # 단어 추가 버튼
        self.add_button = ttk.Button(self.input_frame, text="추가", command=self.add_word, style="Custom.TButton")
        self.add_button.pack(side=tk.LEFT)

        # 퀴즈 시작 버튼
        self.finish_button = ttk.Button(self.input_frame, text="퀴즈 시작", command=self.start_quiz, style="Custom.TButton")
        self.finish_button.pack(side=tk.LEFT)

        # 키보드 이벤트 바인딩
        self.eng_entry.bind("<Return>", self.add_word)
        self.kor_entry.bind("<Return>", self.add_word)
        self.eng_entry.bind("0", self.start_quiz)
        self.kor_entry.bind("0", self.start_quiz)

        # 입력한 단어 목록 표시
        self.words_tree = ttk.Treeview(self.words_frame, columns=("영단어", "한국어"), show="headings")
        self.words_tree.heading("영단어", text="영단어")
        self.words_tree.heading("한국어", text="한국어")
        self.words_tree.pack()

        # 퀴즈 화면
        self.quiz_label = ttk.Label(self.quiz_frame, text="", font=("Segoe UI", 14, "bold"))
        self.quiz_label.pack(pady=5)

        self.answer_entry = ttk.Entry(self.quiz_frame, font=("Segoe UI", 12))
        self.answer_entry.pack(pady=5)

        self.check_button = ttk.Button(self.quiz_frame, text="확인", command=self.check_answer, style="Custom.TButton")
        self.check_button.pack(pady=5)

        self.quiz_frame.pack_forget()
    
    def add_word(self, event=None):
        english = self.eng_entry.get().strip()
        korean = self.kor_entry.get().strip()
        
        if english and korean:
            self.word_dict[english] = korean
            self.eng_entry.delete(0, tk.END)
            self.kor_entry.delete(0, tk.END)
            self.words_tree.insert("", "end", values=(english, korean))
            messagebox.showinfo("단어 추가", f"단어 '{english}'가 추가되었습니다.")
            self.eng_entry.focus_set()
        else:
            messagebox.showerror("입력 오류", "영단어와 한국어 뜻을 모두 입력하세요.")

    def start_quiz(self, event=None):
        if not self.word_dict:
            messagebox.showerror("단어 없음", "단어장을 먼저 입력하세요.")
            return

        self.input_frame.pack_forget()
        self.words_frame.pack_forget()
        self.quiz_frame.pack()
        
        self.words = list(self.word_dict.items())
        self.current_index = 0
        self.next_word()

    def next_word(self):
        if self.current_index < len(self.words):
            english, korean = self.words[self.current_index]
            self.current_english = english
            self.current_korean = korean
            self.quiz_label.config(text=f"{english}의 뜻은?")
        else:
            self.quiz_label.config(text="모든 단어를 맞추셨습니다.")
            self.answer_entry.pack_forget()
            self.check_button.pack_forget()

    def check_answer(self):
        user_answer = self.answer_entry.get().strip()
        if user_answer == self.current_korean:
            messagebox.showinfo("정답", "정답입니다!")
            self.current_index += 1
            self.next_word()
        else:
            messagebox.showerror("오답", "틀렸습니다. 다시 시도하세요.")
        self.answer_entry.delete(0, tk.END)

def main():
    root = tk.Tk()
    app = VocabApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
