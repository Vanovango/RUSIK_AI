import tkinter as tk
from tkinter import filedialog, font

from PIL import Image, ImageTk
from ultralytics import YOLO


class ImagePlacer:
    def __init__(self, master):
        self.master = master
        self.master.title("Image Placer with Movable Images")

        # my font to buttons
        self.my_font = font.Font(size=15)
        # size of window and image
        self.W = 900
        self.H = 600

        # Создаем canvas для отображения изображения
        self.canvas = tk.Canvas(master, width=self.W, height=self.H, bg='white')
        self.canvas.pack()

        # Кнопка загрузки изображения фона
        self.button_load_background = tk.Button(master, text="Отобразить карту местности",
                                                command=self.load_background_image)
        self.button_load_background['font'] = self.my_font
        self.button_load_background.pack()

        # Кнопка загрузки фигур
        self.button_load_shape = tk.Button(master, text="Выбрать условное обозначение", command=self.load_shape_image)
        self.button_load_shape['font'] = self.my_font
        self.button_load_shape.pack()

        # Кнопка отображения линий связи
        self.button_load_shape = tk.Button(master, text="Отобразить линии связи", command=self.draw_communication)
        self.button_load_shape['font'] = self.my_font
        self.button_load_shape.pack()

        # Массивы данных для хранения информации об различных объектах
        self.shapes = []  # Список для хранения объектов фигур
        self.image_refs = []  # Список для хранения ссылок на изображения (чтобы не удалялись сборщиком мусора)
        self.commutation_lines = []     # Список для хранения ссылок на линии коммутации
        self.background_image = ''

        self.drag_data = {}

    def load_background_image(self):
        # open file
        file_path = filedialog.askopenfilename(title="Choose a background image",
                                               filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        print(file_path)

        if file_path:
            image = Image.open(file_path)

            # predict image by train model
            model = YOLO('./ready_models/model2.pt')
            predict_image = model(image, save=True, save_crop=True, project="./predict", name="test",
                                  exist_ok=True, show_labels=False, show_boxes=False)

            # load predict image
            predict_image_path = predict_image[0].save_dir + "\\" + predict_image[0].path.split('\\')[-1]
            predict_image = Image.open(predict_image_path).resize(size=(self.W, self.H))

            # show image on window
            self.background_image = ImageTk.PhotoImage(predict_image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

    def load_shape_image(self):
        # open file
        file_path = filedialog.askopenfilename(title="Choose an image for the shape",
                                               filetypes=[("Image files", "*.jpg *.jpeg *.png *.gif")])
        if file_path:
            image = Image.open(file_path).resize(size=(30, 50))
            shape_image = ImageTk.PhotoImage(image)

            # Создаем фигуру на холсте
            shape_id = self.canvas.create_image(100, 100, anchor=tk.NW, image=shape_image)

            # Храним ссылку на изображение, чтобы оно не удалялось сборщиком мусора
            self.image_refs.append(shape_image)  # Сохраняем ссылку на изображение
            self.shapes.append(shape_id)  # Сохраняем ID фигуры
            self.make_movable(shape_id)

    def make_movable(self, shape_id):
        # Делаем фигуру перетаскиваемой
        self.canvas.tag_bind(shape_id, '<ButtonPress-1>', self.on_shape_press)
        self.canvas.tag_bind(shape_id, '<B1-Motion>', self.on_shape_drag)

    def on_shape_press(self, event):
        # Сохраняем ID фигуры и позицию курсора, когда нажата кнопка мыши
        self.drag_data = {'shape_id': self.canvas.find_closest(event.x, event.y)[0],
                          'x': event.x,
                          'y': event.y}

    def on_shape_drag(self, event):
        shape_id = self.drag_data['shape_id']
        dx = event.x - self.drag_data['x']
        dy = event.y - self.drag_data['y']

        # Перемещаем фигуру и линию
        self.canvas.move(shape_id, dx, dy)

        # Обновляем данные для следующего сдвига
        self.drag_data['x'] = event.x
        self.drag_data['y'] = event.y
        # print(self.drag_data)

    def draw_communication(self):
        """
        move line of commutation between 2 flag on the map
        :return: None
        """
        # print('----------------------')
        # print(self.shapes)
        # print('----------------------')
        # for i in self.shapes:
        #     print(f"id {i} --- coordinates {self.canvas.coords(i)}")
        x1 = self.canvas.coords(self.shapes[0])[0]
        y1 = self.canvas.coords(self.shapes[0])[1] + 50
        x2 = self.canvas.coords(self.shapes[1])[0]
        y2 = self.canvas.coords(self.shapes[1])[1] + 50

        line = self.canvas.create_line(
            x1, y1,     # x1, y1
            x2, y2,     # x2, y2
            width=2, fill="red")
        self.commutation_lines.append(line)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImagePlacer(root)
    root.mainloop()
