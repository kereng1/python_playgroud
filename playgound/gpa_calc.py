import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

class Course:
    def __init__(self, course_name, weight, grade):
        self.course_name = course_name
        self.weight = float(weight)
        self.grade = float(grade)
    
    def to_dict(self):
        return {
            'Course Name': self.course_name,
            'Weight': self.weight,
            'Grade': self.grade
        }

class GPACalculator:
    def __init__(self):
        self.courses = []
    
    def add_course(self, course):
        self.courses.append(course)
    
    def remove_course(self, index):
        del self.courses[index]
    
    def edit_course(self, index, new_course):
        self.courses[index] = new_course
    
    def calculate_gpa(self):
        total_weight = self.get_total_weight()
        if total_weight == 0:
            return 0
        total_points = sum(course.grade * course.weight for course in self.courses)
        return total_points / total_weight
    
    def get_total_weight(self):
        return sum(course.weight for course in self.courses)

class FileHandler:
    @staticmethod
    def save_to_csv(file_path, courses):
        with open(file_path, 'w', newline='') as csvfile:
            fieldnames = ['Course Name', 'Weight', 'Grade']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for course in courses:
                writer.writerow(course.to_dict())
    
    @staticmethod
    def load_from_csv(file_path):
        courses = []
        with open(file_path, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                course = Course(row['Course Name'], row['Weight'], row['Grade'])
                courses.append(course)
        return courses

class GPAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPA Calculator")
        self.calculator = GPACalculator()
        self.create_widgets()
    
    def create_widgets(self):
        # Course Entry Section
        entry_frame = ttk.LabelFrame(self.root, text="Add Course")
        entry_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(entry_frame, text="Course Name:").grid(row=0, column=0, padx=5, pady=5)
        self.course_name_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.course_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Weight (Credit Hours):").grid(row=1, column=0, padx=5, pady=5)
        self.weight_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.weight_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(entry_frame, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
        self.grade_var = tk.StringVar()
        ttk.Entry(entry_frame, textvariable=self.grade_var).grid(row=2, column=1, padx=5, pady=5)

        ttk.Button(entry_frame, text="Add Course", command=self.add_course).grid(row=3, column=0, columnspan=2, pady=5)

        # Course List Section
        list_frame = ttk.Frame(self.root)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ('Course Name', 'Weight', 'Grade')
        self.course_tree = ttk.Treeview(list_frame, columns=columns, show='headings')
        for col in columns:
            self.course_tree.heading(col, text=col)
        self.course_tree.pack(side='left', fill='both', expand=True)

        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.course_tree.yview)
        self.course_tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

        self.course_tree.bind('<Double-1>', self.on_edit_course)

        # GPA Display Section
        gpa_frame = ttk.Frame(self.root)
        gpa_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(gpa_frame, text="Total Weights:").grid(row=0, column=0, padx=5, pady=5)
        self.total_weight_var = tk.StringVar(value="0")
        ttk.Label(gpa_frame, textvariable=self.total_weight_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(gpa_frame, text="Calculated GPA:").grid(row=1, column=0, padx=5, pady=5)
        self.gpa_var = tk.StringVar(value="0.00")
        ttk.Label(gpa_frame, textvariable=self.gpa_var).grid(row=1, column=1, padx=5, pady=5)

        # Menu
        menubar = tk.Menu(self.root)
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Save Data", command=self.save_data)
        file_menu.add_command(label="Load Data", command=self.load_data)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        self.root.config(menu=menubar)

    def add_course(self):
        course_name = self.course_name_var.get()
        weight = self.weight_var.get()
        grade = self.grade_var.get()
        if not course_name or not weight or not grade:
            messagebox.showwarning("Input Error", "Please fill all fields.")
            return
        try:
            course = Course(course_name, weight, grade)
            self.calculator.add_course(course)
            self.update_course_list()
            self.clear_entry_fields()
            self.update_gpa_display()
        except ValueError:
            messagebox.showwarning("Input Error", "Please enter valid numbers for weight and grade.")

    def update_course_list(self):
        for item in self.course_tree.get_children():
            self.course_tree.delete(item)
        for idx, course in enumerate(self.calculator.courses):
            self.course_tree.insert('', 'end', iid=idx, values=(course.course_name, course.weight, course.grade))

    def clear_entry_fields(self):
        self.course_name_var.set('')
        self.weight_var.set('')
        self.grade_var.set('')

    def update_gpa_display(self):
        total_weight = self.calculator.get_total_weight()
        gpa = self.calculator.calculate_gpa()
        self.total_weight_var.set(f"{total_weight:.2f}")
        self.gpa_var.set(f"{gpa:.2f}")

    def on_edit_course(self, event):
        selected_item = self.course_tree.focus()
        if selected_item:
            idx = int(selected_item)
            course = self.calculator.courses[idx]
            self.open_edit_window(idx, course)

    def open_edit_window(self, idx, course):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Course")

        ttk.Label(edit_window, text="Course Name:").grid(row=0, column=0, padx=5, pady=5)
        course_name_var = tk.StringVar(value=course.course_name)
        ttk.Entry(edit_window, textvariable=course_name_var).grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Weight (Credit Hours):").grid(row=1, column=0, padx=5, pady=5)
        weight_var = tk.StringVar(value=str(course.weight))
        ttk.Entry(edit_window, textvariable=weight_var).grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(edit_window, text="Grade:").grid(row=2, column=0, padx=5, pady=5)
        grade_var = tk.StringVar(value=str(course.grade))
        ttk.Entry(edit_window, textvariable=grade_var).grid(row=2, column=1, padx=5, pady=5)

        def save_changes():
            try:
                new_course = Course(course_name_var.get(), weight_var.get(), grade_var.get())
                self.calculator.edit_course(idx, new_course)
                self.update_course_list()
                self.update_gpa_display()
                edit_window.destroy()
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter valid numbers for weight and grade.")

        def delete_course():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this course?"):
                self.calculator.remove_course(idx)
                self.update_course_list()
                self.update_gpa_display()
                edit_window.destroy()

        ttk.Button(edit_window, text="Save Changes", command=save_changes).grid(row=3, column=0, pady=5)
        ttk.Button(edit_window, text="Delete Course", command=delete_course).grid(row=3, column=1, pady=5)

    def save_data(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv")])
        if file_path:
            FileHandler.save_to_csv(file_path, self.calculator.courses)
            messagebox.showinfo("Data Saved", "Course data has been saved successfully.")

    def load_data(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            try:
                courses = FileHandler.load_from_csv(file_path)
                self.calculator.courses = courses
                self.update_course_list()
                self.update_gpa_display()
                messagebox.showinfo("Data Loaded", "Course data has been loaded successfully.")
            except Exception as e:
                messagebox.showerror("Load Error", f"An error occurred while loading data: {e}")

def main():
    root = tk.Tk()
    app = GPAApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
