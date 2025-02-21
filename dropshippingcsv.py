import csv
from tkinter import filedialog, Tk, messagebox
import tkinter as tk

# 功能1：整合多个CSV文件
def merge_csv_files():
    # 选择多个CSV文件
    Tk().withdraw()
    csv_files = filedialog.askopenfilenames(title="选择多个CSV文件进行整合", filetypes=[("CSV files", "*.csv")])
    
    if not csv_files:
        messagebox.showinfo("提示", "未选择文件")
        return

    # 保存整合后的CSV文件
    save_path = filedialog.asksaveasfilename(title="保存整合后的CSV文件", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if not save_path:
        messagebox.showinfo("提示", "没有选择保存路径")
        return

    # 整合数据并保存到新CSV文件
    with open(save_path, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        for file in csv_files:
            with open(file, 'r', newline='', encoding='utf-8') as in_csv:
                reader = csv.reader(in_csv)
                for row in reader:
                    writer.writerow(row)
    
    messagebox.showinfo("完成", f"CSV文件已整合并保存到 {save_path}")

# 功能2：生成“未出Label”的CSV文件
def generate_label_csv():
    # 选择要查找的CSV文件
    Tk().withdraw()
    csv_file = filedialog.askopenfilename(title="选择要查找的CSV文件", filetypes=[("CSV files", "*.csv")])
    
    if not csv_file:
        messagebox.showinfo("提示", "没有选择文件")
        return

    # 弹出窗口，输入要查找的姓名
    root = tk.Tk()
    root.title("输入姓名")
    root.geometry("400x200")
    
    tk.Label(root, text="请复制姓名并按空格键分隔:").pack(pady=10)
    name_entry = tk.Entry(root, width=50)
    name_entry.pack(pady=5)
    
    # 存储所有输入的姓名
    name_list = []
    
    # 更新输入框内容，按空格键分隔姓名
    def update_name_entry(event):
        name = name_entry.get().strip()
        if name:
            name_list.append(name)
            name_entry.delete(0, tk.END)
            name_entry.insert(0, ', '.join(name_list) + ', ')
            name_entry.icursor(len(name_entry.get()))  # 将光标移到行末

    name_entry.bind("<space>", update_name_entry)

    def on_generate():
        if not name_list:
            messagebox.showinfo("提示", "请至少输入一个姓名")
            return
        
        # 选择保存路径和文件名
        save_path = filedialog.asksaveasfilename(title="保存生成的CSV文件", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        
        if not save_path:
            messagebox.showinfo("提示", "没有选择保存路径")
            return
        
        # 从CSV文件中筛选出匹配的姓名
        with open(csv_file, 'r', newline='', encoding='utf-8') as in_csv:
            reader = csv.reader(in_csv)
            matching_rows = [row for row in reader if any(name == ' '.join(row) for name in name_list)]
        
        # 写入新的CSV文件
        with open(save_path, 'w', newline='', encoding='utf-8') as out_csv:
            writer = csv.writer(out_csv)
            writer.writerows(matching_rows)
        
        messagebox.showinfo("完成", f"新CSV文件已生成并保存到 {save_path}")
        root.destroy()

    # 按钮以生成CSV文件
    generate_button = tk.Button(root, text="生成", command=on_generate)
    generate_button.pack(pady=20)
    
    root.mainloop()

# 功能3：修改PTI8数据中的state字段
def modify_pti8_data():
    # 选择PTI8格式的CSV文件
    Tk().withdraw()
    csv_file = filedialog.askopenfilename(title="选择PTI8格式的CSV文件", filetypes=[("CSV files", "*.csv")])
    
    if not csv_file:
        messagebox.showinfo("提示", "没有选择文件")
        return

    # 选择保存修改后的CSV文件
    save_path = filedialog.asksaveasfilename(title="保存修改后的CSV文件", defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    
    if not save_path:
        messagebox.showinfo("提示", "没有选择保存路径")
        return

    # 修改数据并保存到新CSV文件
    with open(csv_file, 'r', newline='', encoding='utf-8') as in_csv:
        reader = csv.reader(in_csv)
        modified_rows = []
        for row in reader:
            if "PTI8" in row and len(row) >= 3:
                # 检查state是否超过10个字符
                state = row[2]
                if len(state) >= 10:
                    # 将town和state向前移动一格
                    town = row[1]
                    row[1] = state[:9]  # 保留前9个字符
                    row[2] = town  # 移动town
            modified_rows.append(row)

    # 写入修改后的数据
    with open(save_path, 'w', newline='', encoding='utf-8') as out_csv:
        writer = csv.writer(out_csv)
        writer.writerows(modified_rows)
    
    messagebox.showinfo("完成", f"修改后的CSV文件已保存到 {save_path}")

# 主菜单
def main():
    root = tk.Tk()
    root.title("CSV处理工具")
    root.geometry("300x200")
    
    tk.Label(root, text="选择一个功能:").pack(pady=10)
    
    # 功能按钮
    merge_button = tk.Button(root, text="整合CSV文件", command=merge_csv_files)
    merge_button.pack(pady=5)

    generate_button = tk.Button(root, text="生成未出Label的CSV", command=generate_label_csv)
    generate_button.pack(pady=5)
    
    modify_button = tk.Button(root, text="修改PTI8数据", command=modify_pti8_data)
    modify_button.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    main()
