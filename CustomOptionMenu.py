import customtkinter


class CustomOptionMenu(customtkinter.CTkButton):

    def __init__(
            self,
            master,

            # Настройка основного элемента - кнопки
            button_width=160,
            button_height=40,
            button_corner_radius=5,
            button_fg_color="#397DA9",
            button_hover_color="#306A8F",
            button_image=None,
            button_font=("Roboto", 12),
            button_text="Option Menu",
            button_text_color="#FAFAFA",

            # Настройка выпадающего списка
            dropdown_width=160,
            dropdown_height=160,
            dropdown_corner_radius=5,
            dropdown_fg_color="#397DA9",
            dropdown_values=None,
            dropdown_font=("Roboto", 12),
            dropdown_text_color="#FAFAFA",
            dropdown_value_hover_color="#306A8F",

            # Настройка полосы прокрутки в выпадающем списке
            dropdown_scrollbar_width=12,
            dropdown_scrollbar_button_color="#163142",
            dropdown_scrollbar_hover_color="#1F445C",
            dropdown_scrollbar_padding=4,

            # Настройка положения выпадающего списка
            dropdown_gap=5,
            dropdown_above=False
    ):
        # Передача аргументов, поступивших извне от пользователя класса
        # внутрь родительского класса данного виджета CTkButton
        super().__init__(
            master=master,
            width=button_width,
            height=button_height,
            corner_radius=button_corner_radius,
            fg_color=button_fg_color,
            hover_color=button_hover_color,
            image=button_image,
            font=button_font,
            text=button_text,
            text_color=button_text_color,
            command=self._toggle_dropdown
        )

        # Если значения для выпадающего списка не были переданы
        if dropdown_values is None:
            dropdown_values = []

        self.current_value = button_text
        self.dropdown_values = dropdown_values

        self.arrow_closed = "▾"
        self.arrow_opened = "▴"

        self.dropdown_width = dropdown_width
        self.dropdown_height = dropdown_height
        self.dropdown_corner_radius = dropdown_corner_radius
        self.dropdown_fg_color = dropdown_fg_color
        self.dropdown_font = dropdown_font
        self.dropdown_text_color = dropdown_text_color
        self.dropdown_value_hover_color = dropdown_value_hover_color

        self.dropdown_scrollbar_width = dropdown_scrollbar_width
        self.dropdown_scrollbar_button_color = dropdown_scrollbar_button_color
        self.dropdown_scrollbar_hover_color = dropdown_scrollbar_hover_color
        self.dropdown_scrollbar_padding = dropdown_scrollbar_padding

        self.dropdown_gap = dropdown_gap
        self.dropdown_above = dropdown_above

        self.dropdown_opened = False
        self.dropdown = None

        self.configure(text=f"{self.current_value} {self.arrow_closed}")

    def _toggle_dropdown(self):

        # Если выпадающий список уже открыт
        if self.dropdown_opened:
            self._hide_dropdown()

        # Если выпадающий список скрыт
        else:
            self._show_dropdown()

    def _show_dropdown(self):

        if self.dropdown is not None:
            self._hide_dropdown()

        self.configure(text=f"{self.current_value} {self.arrow_opened}")

        self.dropdown = customtkinter.CTkScrollableFrame(
            master=self.master,
            width=self.dropdown_width,
            height=self.dropdown_height,
            corner_radius=self.dropdown_corner_radius,
            fg_color=self.dropdown_fg_color,
            scrollbar_button_color=self.dropdown_scrollbar_button_color,
            scrollbar_button_hover_color=self.dropdown_scrollbar_hover_color,
        )

        self.dropdown._scrollbar.configure(width=self.dropdown_scrollbar_width)
        self.dropdown._scrollbar.grid_configure(padx=(0, self.dropdown_scrollbar_padding))

        # Получение текущих координат кнопки
        x = self.winfo_x()
        y = self.winfo_y()

        # Размещение списка над кнопкой
        if self.dropdown_above:
            self.dropdown.place(
                x=x,
                y=y - self.dropdown_height - self.dropdown_gap
            )

        # Размещение списка под кнопкой
        else:
            self.dropdown.place(
                x=x,
                y=y + self.winfo_height() + self.dropdown_gap
            )

        # Создание кнопок внутри выпадающего списка
        for value in self.dropdown_values:
            value_button = customtkinter.CTkButton(
                master=self.dropdown,
                text=value,
                fg_color="transparent",
                hover_color=self.dropdown_value_hover_color,
                text_color=self.dropdown_text_color,
                font=self.dropdown_font,
                anchor="w",
                command=lambda selected=value: self._select_value(selected)
            )

            value_button.pack(fill="x", padx=2, pady=2)

        self.dropdown.lift()
        self.dropdown_opened = True

    def _hide_dropdown(self):

        if self.dropdown is not None:
            self.dropdown.place_forget()
            self.dropdown.destroy()
            self.dropdown = None

        self.dropdown_opened = False

        self.configure(text=f"{self.current_value} {self.arrow_closed}")

    def _select_value(self, value):

        self.current_value = value

        # Изменение текста основной кнопки
        self.configure(text=f"{self.current_value} {self.arrow_closed}")

        # Сокрытие выпадающего списка после выбора значения
        self._hide_dropdown()

    def get(self):

        return self.current_value

    def set(self, value):

        self.current_value = value
        self.configure(text=f"{self.current_value} {self.arrow_closed}")
