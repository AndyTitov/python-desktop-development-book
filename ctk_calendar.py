from __future__ import annotations

import calendar
import datetime
from typing import Literal

import customtkinter


class CTkCalendar(customtkinter.CTkFrame):
    def __init__(
        self,
        master,
        width: int = 280,
        height: int = 270,
        selection_mode: Literal["single", "range"] = "range",
        fg_color=("#F9FAFB", "#1F1F1F"),
        border_color="#3B8ED0",
        border_width: int = 1,
        corner_radius: int = 10,
        header_text_color=("#1F2937", "#F9FAFB"),
        weekday_text_color="#3B8ED0",
        day_fg_color=("#FFFFFF", "#2B2B2B"),
        day_text_color=("#1F2937", "#F9FAFB"),
        day_border_color="#3B8ED0",
        day_hover_color=("#DCEEFF", "#1F6AA5"),
        selected_fg_color="#3B8ED0",
        selected_text_color="#FFFFFF",
        today_fg_color=("#DCEEFF", "#263A4F"),
        today_text_color="#3B8ED0",
        nav_button_fg_color="#3B8ED0",
        nav_button_hover_color="#36719F",
        nav_button_text_color="#FFFFFF",
        font=("Arial", 14, "bold"),
        weekday_font=("Arial", 13, "bold"),
        day_font=("Arial", 13),
        months: list[str] | None = None,
        weekdays: list[str] | None = None,
        start_date: datetime.date | None = None,
        command=None,
    ):
        super().__init__(
            master=master,
            width=width,
            height=height,
            fg_color=fg_color,
            border_color=border_color,
            border_width=border_width,
            corner_radius=corner_radius,
        )

        if selection_mode not in ("single", "range"):
            raise ValueError("selection_mode must be 'single' or 'range'")

        self.width = width
        self.height = height
        self.selection_mode = selection_mode
        self.command = command

        self._colors = {
            "fg_color": fg_color,
            "border_color": border_color,
            "header_text_color": header_text_color,
            "weekday_text_color": weekday_text_color,
            "day_fg_color": day_fg_color,
            "day_text_color": day_text_color,
            "day_border_color": day_border_color,
            "day_hover_color": day_hover_color,
            "selected_fg_color": selected_fg_color,
            "selected_text_color": selected_text_color,
            "today_fg_color": today_fg_color,
            "today_text_color": today_text_color,
            "nav_button_fg_color": nav_button_fg_color,
            "nav_button_hover_color": nav_button_hover_color,
            "nav_button_text_color": nav_button_text_color,
        }

        self._fonts = {
            "header": font,
            "weekday": weekday_font,
            "day": day_font,
        }

        self.months = months or [
            "Январь", "Февраль", "Март", "Апрель", "Май", "Июнь",
            "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"
        ]
        self.weekdays = weekdays or ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]

        base_date = start_date or datetime.date.today()
        self.current_year = base_date.year
        self.current_month = base_date.month

        self._anchors: list[datetime.date] = []
        self.day_buttons: list[customtkinter.CTkButton] = []
        self._button_dates: list[datetime.date | None] = [None] * 42
        self._weekday_labels: list[customtkinter.CTkLabel] = []

        self.grid_propagate(False)
        self.pack_propagate(False)

        self._build_layout()
        self.render_calendar()

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

        self._header_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self._header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 4))

        self._header_frame.grid_columnconfigure(0, weight=0)
        self._header_frame.grid_columnconfigure(1, weight=0)
        self._header_frame.grid_columnconfigure(2, weight=1)
        self._header_frame.grid_columnconfigure(3, weight=0)
        self._header_frame.grid_columnconfigure(4, weight=0)

        self.double_left_arrow = customtkinter.CTkButton(
            master=self._header_frame,
            width=28,
            height=28,
            text="«",
            fg_color=self._colors["nav_button_fg_color"],
            hover_color=self._colors["nav_button_hover_color"],
            text_color=self._colors["nav_button_text_color"],
            corner_radius=6,
            command=self.prev_year,
        )
        self.double_left_arrow.grid(row=0, column=0, sticky="w", padx=(0, 4))

        self.left_arrow = customtkinter.CTkButton(
            master=self._header_frame,
            width=28,
            height=28,
            text="‹",
            fg_color=self._colors["nav_button_fg_color"],
            hover_color=self._colors["nav_button_hover_color"],
            text_color=self._colors["nav_button_text_color"],
            corner_radius=6,
            command=self.prev_month,
        )
        self.left_arrow.grid(row=0, column=1, sticky="w", padx=(0, 8))

        self.month_and_year = customtkinter.CTkLabel(
            master=self._header_frame,
            text="",
            text_color=self._colors["header_text_color"],
            font=self._fonts["header"],
        )
        self.month_and_year.grid(row=0, column=2, sticky="ew", padx=4)

        self.right_arrow = customtkinter.CTkButton(
            master=self._header_frame,
            width=28,
            height=28,
            text="›",
            fg_color=self._colors["nav_button_fg_color"],
            hover_color=self._colors["nav_button_hover_color"],
            text_color=self._colors["nav_button_text_color"],
            corner_radius=6,
            command=self.next_month,
        )
        self.right_arrow.grid(row=0, column=3, sticky="e", padx=(8, 4))

        self.double_right_arrow = customtkinter.CTkButton(
            master=self._header_frame,
            width=28,
            height=28,
            text="»",
            fg_color=self._colors["nav_button_fg_color"],
            hover_color=self._colors["nav_button_hover_color"],
            text_color=self._colors["nav_button_text_color"],
            corner_radius=6,
            command=self.next_year,
        )
        self.double_right_arrow.grid(row=0, column=4, sticky="e")

        self._weekdays_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self._weekdays_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 4))

        for column in range(7):
            self._weekdays_frame.grid_columnconfigure(column, weight=1, uniform="weekday")

        for column, weekday in enumerate(self.weekdays):
            label = customtkinter.CTkLabel(
                master=self._weekdays_frame,
                text=weekday,
                text_color=self._colors["weekday_text_color"],
                font=self._fonts["weekday"],
            )
            label.grid(row=0, column=column, sticky="nsew", padx=2, pady=2)
            self._weekday_labels.append(label)

        self._days_frame = customtkinter.CTkFrame(master=self, fg_color="transparent")
        self._days_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=(0, 10))

        for column in range(7):
            self._days_frame.grid_columnconfigure(column, weight=1, uniform="day")

        for row in range(6):
            self._days_frame.grid_rowconfigure(row, weight=1, uniform="day")

        self._create_day_buttons()

    def _create_day_buttons(self):
        for index in range(42):
            row = index // 7
            column = index % 7

            button = customtkinter.CTkButton(
                master=self._days_frame,
                text="",
                text_color=self._colors["day_text_color"],
                fg_color=self._colors["day_fg_color"],
                border_color=self._colors["day_border_color"],
                border_width=1,
                font=self._fonts["day"],
                hover_color=self._colors["day_hover_color"],
                corner_radius=6,
                command=lambda button_index=index: self._on_button_click(button_index),
            )
            button.grid(row=row, column=column, sticky="nsew", padx=2, pady=2)
            self.day_buttons.append(button)

    def place_left_of(self, target, gap=12, align="center", y_offset=-120):
        self.update_idletasks()
        target.update_idletasks()

        calendar_width = self.winfo_width()
        calendar_height = self.winfo_height()

        target_x = target.winfo_rootx()
        target_y = target.winfo_rooty()
        target_height = target.winfo_height()

        root = self.master
        root_x = root.winfo_rootx()
        root_y = root.winfo_rooty()

        x = target_x - gap - calendar_width

        if align == "top":
            y = target_y + y_offset
        elif align == "bottom":
            y = target_y + target_height - calendar_height + y_offset
        else:
            y = target_y + (target_height - calendar_height) // 2 + y_offset

        self.place(x=x - root_x, y=y - root_y, anchor="nw")

    def _date_for_day(self, day: int) -> datetime.date:
        return datetime.date(self.current_year, self.current_month, day)

    def _is_selected(self, date_value: datetime.date) -> bool:
        if self.selection_mode == "single":
            return len(self._anchors) == 1 and date_value == self._anchors[0]

        if len(self._anchors) == 2:
            start, end = sorted(self._anchors)
            return start <= date_value <= end

        if len(self._anchors) == 1:
            return date_value == self._anchors[0]

        return False

    def render_calendar(self):
        self.month_and_year.configure(
            text=f"{self.months[self.current_month - 1]}, {self.current_year}"
        )

        self._button_dates = [None] * 42

        for button in self.day_buttons:
            button.grid_remove()

        first_weekday, number_of_days = calendar.monthrange(self.current_year, self.current_month)

        for day in range(1, number_of_days + 1):
            index = first_weekday + day - 1
            date_value = self._date_for_day(day)
            button = self.day_buttons[index]

            self._button_dates[index] = date_value
            button.configure(text=str(day), state="normal")
            button.grid()

        self._repaint()

    def _repaint(self):
        today = datetime.date.today()

        for index, button in enumerate(self.day_buttons):
            date_value = self._button_dates[index]

            if date_value is None:
                continue

            if self._is_selected(date_value):
                button.configure(
                    fg_color=self._colors["selected_fg_color"],
                    text_color=self._colors["selected_text_color"],
                    border_color=self._colors["day_border_color"],
                    hover_color=self._colors["day_hover_color"],
                )
            elif date_value == today:
                button.configure(
                    fg_color=self._colors["today_fg_color"],
                    text_color=self._colors["today_text_color"],
                    border_color=self._colors["day_border_color"],
                    hover_color=self._colors["day_hover_color"],
                )
            else:
                button.configure(
                    fg_color=self._colors["day_fg_color"],
                    text_color=self._colors["day_text_color"],
                    border_color=self._colors["day_border_color"],
                    hover_color=self._colors["day_hover_color"],
                )

    def _on_button_click(self, button_index: int):
        selected_date = self._button_dates[button_index]

        if selected_date is None:
            return

        if self.selection_mode == "single":
            self._anchors = [selected_date]
            self._repaint()
            self._run_command()
            return

        if selected_date in self._anchors:
            self._anchors.remove(selected_date)
        elif len(self._anchors) < 2:
            self._anchors.append(selected_date)
        else:
            self._anchors = [selected_date]

        self._repaint()
        self._run_command()

    def on_day_click(self, day: int):
        selected_date = self._date_for_day(day)

        if self.selection_mode == "single":
            self._anchors = [selected_date]
            self._repaint()
            self._run_command()
            return

        if selected_date in self._anchors:
            self._anchors.remove(selected_date)
        elif len(self._anchors) < 2:
            self._anchors.append(selected_date)
        else:
            self._anchors = [selected_date]

        self._repaint()
        self._run_command()

    def _run_command(self):
        if self.command is None:
            return

        try:
            self.command(self)
        except TypeError:
            self.command()

    def get_selected_date(self) -> datetime.date | None:
        if not self._anchors:
            return None

        return self._anchors[0]

    def get_selected_range(self) -> tuple[datetime.date | None, datetime.date | None]:
        if not self._anchors:
            return None, None

        if len(self._anchors) == 1:
            return self._anchors[0], self._anchors[0]

        start, end = sorted(self._anchors)
        return start, end

    def clear_selection(self):
        self._anchors.clear()
        self._repaint()

    def set_selected_date(self, date_value: datetime.date | None):
        if date_value is None:
            self.clear_selection()
            return

        self.current_year = date_value.year
        self.current_month = date_value.month
        self._anchors = [date_value]
        self.render_calendar()

    def set_selected_range(self, start: datetime.date | None, end: datetime.date | None = None):
        if start is None:
            self.clear_selection()
            return

        if end is None:
            end = start

        self.current_year = start.year
        self.current_month = start.month
        self._anchors = sorted([start, end])
        self.render_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1

        self.render_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1

        self.render_calendar()

    def prev_year(self):
        self.current_year -= 1
        self.render_calendar()

    def next_year(self):
        self.current_year += 1
        self.render_calendar()

    @staticmethod
    def remove_zero(obj: str) -> int:
        return int(obj[1]) if obj and obj[0] == "0" else int(obj)
