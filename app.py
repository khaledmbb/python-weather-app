from pathlib import Path
from tkinter import *  # type:ignore
from tkinter import font
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import PhotoImage
from ttkbootstrap.dialogs import Messagebox
import requests
from requests.exceptions import HTTPError
import datetime

PATH = Path(__file__).parent / "assets"

# 89a2bcbc12354f8bae9143824231607


class Weather_app:
    def __init__(self):
        self.root = ttk.Window(
            title="Weather App",
            themename="yeti",
            size=(1200, 800),
            minsize=(1200, 800),
        )
        self.root.iconbitmap("./IMGS/weather.ico")
        self.bg = "#e0f8fc"
        self.font = ("jetbrains mono", 12)
        self.root.config(bg=self.bg)
        self.root.option_add("*Font", self.font)

        self.root.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # type:ignore
        self.root.rowconfigure([0, 1, 2, 3], weight=0)  # type:ignore
        self.root.config(padx=20, pady=20)

        self.create_gui()
        self.fetch_data()

    def create_gui(self):
        # Frame 1
        style = ttk.Style()
        style.configure("frm1.TFrame", background=self.bg)
        style.configure("font.TButton", font=self.font)
        frm1 = ttk.Frame(self.root, style="frm1.TFrame")
        frm1.grid(row=0, column=0, columnspan=6, sticky="nsew")
        frm1.grid_columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # type:ignore

        title = ttk.Label(
            frm1,
            text="Tkinter Weather",
            bootstyle="info",
            background=self.bg,
            font=(self.font[0], 20, "bold"),
        )
        title.grid(row=0, column=0, sticky="ew")

        self.search_bar = ttk.Entry(frm1, bootstyle="info")
        self.search_bar.insert(0, "alaska")
        self.search_bar.grid(
            row=1, column=0, sticky="ew", pady=20, columnspan=5, ipady=5
        )

        self.sub_btn = ttk.Button(
            frm1,
            text="Submit",
            bootstyle="info",
            style="font.TButton",
            command=self.fetch_data,
        )
        self.sub_btn.grid(row=1, column=5, sticky="ew", ipady=5, padx=(15, 0))

        # Frame 2
        frm2 = ttk.Frame(self.root, padding=(25, 20))
        frm2.grid(row=1, column=0, columnspan=6, sticky="nsew")
        frm2.grid_columnconfigure([0, 1, 2], weight=1)  # type:ignore
        frm2.grid_rowconfigure([0, 1, 2, 3, 4], weight=1)  # type:ignore

        lb1 = ttk.Label(frm2, text="Current weather", bootstyle="secondary")
        lb1.grid(row=0, column=0, sticky="w")

        def place_curr_data(
            city_name,
            ico,
            txt_condition,
            temp_c,
            feelslike_c,
            max_tem,
            min_tem,
            hum,
            wind,
            pressure,
        ):
            city_lb = ttk.Label(
                frm2, text=city_name, bootstyle="info", font=(*self.font, "bold")
            )
            city_lb.grid(row=1, column=0, sticky="w", pady=(15, 0))

            img_path = Path(__file__).parent / ico
            self.img = ttk.PhotoImage(file=img_path)
            self.image = self.img.zoom(3)
            self.img_lb = ttk.Label(frm2, image=self.image)
            self.img_lb.grid(row=2, column=0, sticky="w", rowspan=3)

            condition_lb = ttk.Label(
                frm2, text=txt_condition, bootstyle="info", font=(*self.font, "bold")
            )
            condition_lb.grid(row=4, column=0, sticky="nsew")

            temp = ttk.Label(
                frm2,
                text=temp_c,
                font=(self.font[0], 55, "normal"),
                bootstyle="info",
            )
            temp.grid(row=2, column=1, sticky="nsw", rowspan=3)

            feelslike = ttk.Label(
                frm2,
                text=feelslike_c,
                font=(*self.font, "bold"),
                bootstyle="info",
            )
            feelslike.grid(row=1, column=2, sticky="w")

            maxmintemp_frm = ttk.Frame(frm2)
            maxmintemp_frm.grid(row=2, column=2, sticky="nsw", pady=(0, 10))

            max_img_path = Path(__file__).parent / "./IMGS/up.png"
            self.max_img = ttk.PhotoImage(file=max_img_path)
            self.max_image = self.max_img.subsample(2, 2)
            self.max_img_lb = ttk.Label(maxmintemp_frm, image=self.max_image)
            self.max_img_lb.grid(row=0, column=0, sticky="w")

            up_lb = ttk.Label(
                maxmintemp_frm,
                text=max_tem,
                bootstyle="info",
                font=(*self.font, "bold"),
            )
            up_lb.grid(row=0, column=1)

            em_lb = ttk.Label(maxmintemp_frm, padding=(10, 0))
            em_lb.grid(row=0, column=2)

            min_img_path = Path(__file__).parent / "./IMGS/down.png"
            self.min_img = ttk.PhotoImage(file=min_img_path)
            self.min_image = self.min_img.subsample(2, 2)
            self.min_img_lb = ttk.Label(maxmintemp_frm, image=self.min_image)
            self.min_img_lb.grid(row=0, column=3, sticky="w")

            down_lb = ttk.Label(
                maxmintemp_frm,
                text=min_tem,
                bootstyle="info",
                font=(*self.font, "bold"),
            )
            down_lb.grid(row=0, column=4)

            info_frm = ttk.Frame(frm2)
            info_frm.grid(row=3, column=2, sticky="nsw")

            humidity_img_path = Path(__file__).parent / "./IMGS/humidity.png"
            self.humidity_img = ttk.PhotoImage(file=humidity_img_path)
            self.humidity_image = self.humidity_img.subsample(3, 3)
            self.humidity_img_lb = ttk.Label(
                info_frm, image=self.humidity_image, padding=(10, 10)
            )
            self.humidity_img_lb.grid(row=0, column=0, sticky="w")

            humidity_lb = ttk.Label(
                info_frm, text="humidity", bootstyle="secondary", padding=(15, 0)
            )
            humidity_lb.grid(row=0, column=1, sticky=W)

            humidity_per_lb = ttk.Label(
                info_frm, text=hum, bootstyle="info", font=(*self.font, "bold")
            )
            humidity_per_lb.grid(row=0, column=2, sticky=W)

            wind_img_path = Path(__file__).parent / "./IMGS/wind.png"
            self.wind_img = ttk.PhotoImage(file=wind_img_path)
            self.wind_image = self.wind_img.subsample(3, 3)
            self.wind_img_lb = ttk.Label(
                info_frm, image=self.wind_image, padding=(10, 10)
            )
            self.wind_img_lb.grid(row=1, column=0, sticky="w")

            wind_lb = ttk.Label(
                info_frm, text="wind", bootstyle="secondary", padding=(15, 0)
            )
            wind_lb.grid(row=1, column=1, sticky=W)

            wind_per_lb = ttk.Label(
                info_frm, text=wind, bootstyle="info", font=(*self.font, "bold")
            )
            wind_per_lb.grid(row=1, column=2, sticky=W)

            pressure_img_path = Path(__file__).parent / "./IMGS/pressure.png"
            self.pressure_img = ttk.PhotoImage(file=pressure_img_path)
            self.pressure_image = self.pressure_img.subsample(3, 3)
            self.pressure_img_lb = ttk.Label(
                info_frm, image=self.pressure_image, padding=(10, 10)
            )
            self.pressure_img_lb.grid(row=2, column=0, sticky="w")

            pressure_lb = ttk.Label(
                info_frm, text="pressure", bootstyle="secondary", padding=(15, 0)
            )
            pressure_lb.grid(row=2, column=1, sticky=W)

            pressure_per_lb = ttk.Label(
                info_frm, text=pressure, bootstyle="info", font=(*self.font, "bold")
            )
            pressure_per_lb.grid(row=2, column=2, sticky=W)

        self.place_curr_data = place_curr_data

        # frame 3
        frm3 = ttk.Frame(self.root, padding=(25, 20))
        frm3.grid(row=2, column=0, columnspan=6, sticky="nsew", pady=(25, 0))
        frm3.grid_columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # type:ignore
        frm3.grid_rowconfigure([0, 1], weight=1)  # type:ignore

        lb2 = ttk.Label(frm3, text="Extended forecast", bootstyle="secondary")
        lb2.grid(row=0, column=0, sticky="w", pady=(0, 20))

        days_holder = ttk.Frame(frm3)
        days_holder.grid(row=1, column=0, columnspan=6, sticky="nsew")

        days_holder.columnconfigure([0, 1, 2, 3, 4, 5], weight=1)  # type:ignore

        def place_days(days, icons, days_status, tem):
            for num in range(0, 7):
                day_holder = ttk.Frame(days_holder)
                day_holder.grid(
                    row=0,
                    column=num,
                    sticky="nsew",
                )

                day = ttk.Label(
                    day_holder,
                    text=days[num],
                    bootstyle="info",
                    font=(*self.font, "bold"),
                )
                day.grid(row=0, column=0)

                if num == 0:
                    day_img_path_0 = Path(__file__).parent / icons[num]
                    self.day_img_0 = ttk.PhotoImage(file=day_img_path_0)
                    self.day_img_lb_0 = ttk.Label(day_holder, image=self.day_img_0)
                    self.day_img_lb_0.grid(row=1, column=0)
                elif num == 1:
                    day_img_path_1 = Path(__file__).parent / icons[num]
                    self.day_img_1 = ttk.PhotoImage(file=day_img_path_1)
                    self.day_img_lb_1 = ttk.Label(day_holder, image=self.day_img_1)
                    self.day_img_lb_1.grid(row=1, column=0)
                elif num == 2:
                    day_img_path_2 = Path(__file__).parent / icons[num]
                    self.day_img_2 = ttk.PhotoImage(file=day_img_path_2)
                    self.day_img_lb_2 = ttk.Label(day_holder, image=self.day_img_2)
                    self.day_img_lb_2.grid(row=1, column=0)
                elif num == 3:
                    day_img_path_3 = Path(__file__).parent / icons[num]
                    self.day_img_3 = ttk.PhotoImage(file=day_img_path_3)
                    self.day_img_lb_3 = ttk.Label(day_holder, image=self.day_img_3)
                    self.day_img_lb_3.grid(
                        row=1,
                        column=0,
                    )
                elif num == 4:
                    day_img_path_4 = Path(__file__).parent / icons[num]
                    self.day_img_4 = ttk.PhotoImage(file=day_img_path_4)
                    self.day_img_lb_4 = ttk.Label(day_holder, image=self.day_img_4)
                    self.day_img_lb_4.grid(row=1, column=0)
                elif num == 5:
                    day_img_path_5 = Path(__file__).parent / icons[num]
                    self.day_img_5 = ttk.PhotoImage(file=day_img_path_5)
                    self.day_img_lb_5 = ttk.Label(day_holder, image=self.day_img_5)
                    self.day_img_lb_5.grid(row=1, column=0)
                elif num == 6:
                    day_img_path_6 = Path(__file__).parent / icons[num]
                    self.day_img_6 = ttk.PhotoImage(file=day_img_path_6)
                    self.day_img_lb_6 = ttk.Label(day_holder, image=self.day_img_6)
                    self.day_img_lb_6.grid(row=1, column=0)
                else:
                    day_img_path_7 = Path(__file__).parent / icons[num]
                    self.day_img_7 = ttk.PhotoImage(file=day_img_path_7)
                    self.day_img_lb_7 = ttk.Label(day_holder, image=self.day_img_7)
                    self.day_img_lb_7.grid(row=1, column=0)

                def handle_phrase(phrase):
                    phrase_len = len(phrase.split())
                    sentence = phrase.split()
                    if phrase_len == 3:
                        return f"{sentence[0]} {sentence[1]}\n {sentence[2]}"
                    if phrase_len == 4:
                        return f"{sentence[0]} {sentence[1]}\n {sentence[2]} {sentence[3]}\n"
                    if phrase_len == 5:
                        return f"{sentence[0]} {sentence[1]}\n {sentence[2]} {sentence[3]}\n {sentence[4]}"
                    else:
                        return phrase

                day_status = ttk.Label(
                    day_holder,
                    text=handle_phrase(days_status[num]),
                    bootstyle="info",
                    font=(*self.font, "bold"),
                    justify="center",
                )
                day_status.grid(row=2, column=0, pady=5)

                day_temp = ttk.Label(day_holder, text=tem[num], bootstyle="info")
                day_temp.grid(row=3, column=0, pady=5)

        my_name = ttk.Label(
            self.root,
            text="Developed by khaled mabrouki",
            bootstyle="info",
            background=self.bg,
            font=(*self.font, "bold"),
        )
        my_name.grid(row=3, column=3, sticky="ew", pady=10)

        self.place_days = place_days

    def fetch_data(self):
        city = self.search_bar.get()
        url = f"http://api.weatherapi.com/v1/forecast.json?key=89a2bcbc12354f8bae9143824231607&q={city}&days=7&aqi=no&alerts=no"

        if not city:
            Messagebox.show_error(
                "Please, Enter a valid city name", "Invalid city name"
            )
        else:
            try:
                self.sub_btn.config(state=DISABLED)

                self.response = requests.get(url)
                self.response.raise_for_status()

            except HTTPError as e:
                if self.response.status_code == 401:
                    Messagebox.show_error("Sorry, an error in the app", "App Error")
                elif self.response.status_code == 400:
                    Messagebox.show_error(
                        "Please, Enter a valid city name ", "Invalid city name"
                    )
                else:
                    Messagebox.show_error("An error occurred ", "An error")
            else:
                now_time = datetime.datetime.now().hour

                city_name = self.response.json()["location"]["name"]
                ico = "./IMGS/" + "/".join(
                    self.response.json()["current"]["condition"]["icon"].split("/")[-4:]
                )
                txt_condition = self.response.json()["current"]["condition"]["text"]
                temp = str(int(self.response.json()["current"]["temp_c"])) + "°c"
                feelslike = (
                    "feels like "
                    + str(int(self.response.json()["current"]["feelslike_c"]))
                    + "°c"
                )
                max_tem = (
                    str(
                        int(
                            self.response.json()["forecast"]["forecastday"][0]["day"][
                                "maxtemp_c"
                            ]
                        )
                    )
                    + "°c"
                )
                min_tem = (
                    str(
                        int(
                            self.response.json()["forecast"]["forecastday"][0]["day"][
                                "mintemp_c"
                            ]
                        )
                    )
                    + "°c"
                )

                humidity = (
                    str(
                        self.response.json()["forecast"]["forecastday"][0]["hour"][
                            now_time
                        ]["humidity"]
                    )
                    + " %"
                )

                wind = (
                    str(
                        int(
                            self.response.json()["forecast"]["forecastday"][0]["hour"][
                                now_time
                            ]["wind_kph"]
                        )
                    )
                    + " kph"
                )

                pressure = (
                    str(
                        int(
                            self.response.json()["forecast"]["forecastday"][0]["hour"][
                                now_time
                            ]["pressure_mb"]
                        )
                    )
                    + " hpa"
                )

                self.place_curr_data(
                    city_name,
                    ico,
                    txt_condition,
                    temp,
                    feelslike,
                    max_tem,
                    min_tem,
                    humidity,
                    wind,
                    pressure,
                )

                days = []
                icons = []
                days_status = []
                tem = []
                for day_num in range(0, 7):
                    year = int(
                        self.response.json()["forecast"]["forecastday"][day_num][
                            "date"
                        ].split("-")[0]
                    )

                    month = int(
                        self.response.json()["forecast"]["forecastday"][day_num][
                            "date"
                        ].split("-")[1]
                    )

                    day = int(
                        self.response.json()["forecast"]["forecastday"][day_num][
                            "date"
                        ].split("-")[2]
                    )

                    icon = "./IMGS/" + "/".join(
                        self.response.json()["forecast"]["forecastday"][day_num][
                            "hour"
                        ][now_time]["condition"]["icon"].split("/")[-4:]
                    )

                    day_status = self.response.json()["forecast"]["forecastday"][
                        day_num
                    ]["hour"][now_time]["condition"]["text"]

                    temps = (
                        str(
                            int(
                                self.response.json()["forecast"]["forecastday"][
                                    day_num
                                ]["hour"][now_time]["temp_c"]
                            )
                        )
                        + "°/"
                        + str(
                            int(
                                self.response.json()["forecast"]["forecastday"][
                                    day_num
                                ]["hour"][now_time]["feelslike_c"]
                            )
                        )
                        + "°"
                    )

                    days.append(datetime.datetime(year, month, day).strftime("%a"))
                    icons.append(icon)
                    days_status.append(day_status)
                    tem.append(temps)
                self.place_days(days, icons, days_status, tem)

            finally:
                self.sub_btn.config(state=NORMAL)

    def run_app(self):
        self.root.mainloop()


app = Weather_app()
app.run_app()
