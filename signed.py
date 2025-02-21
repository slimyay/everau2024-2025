import io
import fitz  # PyMuPDF
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from tkinter import Tk, filedialog, Button
from datetime import datetime
from PIL import Image

# 创建签名叠加页面并保存到临时文件
def create_signature_overlay(date, x_date, y_date):
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.drawString(x_date, y_date, f"{date}")
    can.save()
    packet.seek(0)

    temp_pdf_path = "temp_signature_overlay.pdf"
    with open(temp_pdf_path, "wb") as f:
        f.write(packet.getbuffer())

    return temp_pdf_path

# 查找特定文本的位置
def find_text_position(pdf_path, search_text):
    doc = fitz.open(pdf_path)
    positions = []
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text_instances = page.search_for(search_text)
        if text_instances:
            positions.append((page_num, text_instances[0]))
    return positions

# 合并签名叠加页和原始PDF
def sign_pdf(pdf_path, signature_image_path, output_path):
    # 获取今天的日期并格式化为 dd/mm
    today_date = datetime.now().strftime("%d/%m")

    # 查找“Signature of Sender”和“Date”字段的位置
    signature_positions = find_text_position(pdf_path, "Signature of Sender")
    date_positions = find_text_position(pdf_path, "Date")

    if not signature_positions or not date_positions:
        print("未找到“Signature of Sender”或“Date”字段。")
        return

    # 读取原始PDF
    existing_pdf = fitz.open(pdf_path)
    
    # 创建输出PDF
    output_pdf = fitz.open()

    # 打开图像并调整清晰度
    signature_image = Image.open(signature_image_path)
    signature_image = signature_image.resize((200, 100), Image.LANCZOS)  # 保持高分辨率
    signature_image.save("high_res_signature.png", "PNG")  # 保存调整后的图像

    # 遍历每一页并在相应位置签名
    for page_num in range(len(existing_pdf)):
        page = existing_pdf.load_page(page_num)
        
        # 获取当前页的签名和日期位置
        sig_pos = next((pos for p_num, pos in signature_positions if p_num == page_num), None)
        date_pos = next((pos for p_num, pos in date_positions if p_num == page_num), None)

        if sig_pos and date_pos:
            # 创建叠加PDF文件
            overlay_pdf_path = create_signature_overlay(today_date, date_pos[2] + 10, date_pos[1] )  # 将日期向下移动两行

            overlay_pdf_reader = fitz.open(overlay_pdf_path)
            page.show_pdf_page(overlay_pdf_reader[0].rect, overlay_pdf_reader, 0)

            # 插入清晰的签名图像
            img_rect = fitz.Rect(sig_pos[2] + 10, sig_pos[1] - 30, sig_pos[2] + 10 + 120, sig_pos[1] - 30 + 60)  # 向上移动两行
            page.insert_image(img_rect, filename="high_res_signature.png", keep_proportion=True)  # 保持比例插入图像

        output_pdf.insert_pdf(existing_pdf, from_page=page_num, to_page=page_num)

    # 保存输出PDF
    output_pdf.save(output_path)
    output_pdf.close()
    print(f"签名的PDF已保存到: {output_path}")

# 选择PDF文件并进行签名处理
def select_file():
    pdf_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    if pdf_path:
        output_path = pdf_path.replace(".pdf", "_signed.pdf")
        signature_image_path = r"C:\Users\ever\Desktop\temp\pdf signature\Screenshot 2024-07-15 110634.png"
        sign_pdf(pdf_path, signature_image_path, output_path)

# 创建简单的Tkinter窗口
root = Tk()
root.title("PDF签名工具")

button = Button(root, text="选择PDF文件并签名", command=select_file)
button.pack(pady=20)

root.mainloop()
