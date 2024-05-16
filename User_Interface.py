# Import necessary libraries 
import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import csv
import numpy as np

class Statistics_Tracker(tk.Tk):
    """
    Loads the user interface for the statistcs tracker app
    with buttons to add/delete round as well as buttons that
    print the graphs related to the statistics.
    """
    def __init__(self):
        """
        Function that initializes the class and the user interface.
        """
        super().__init__()
        self.title("Golf Statistics Tracker")
        self.geometry("1350x750")
        self.scores = []
        self.setup_user_interface()

    def setup_user_interface(self):
        """
        Function that creates the entries for club name, date, score,
        GIR, FIR % Putts. A frame were all the inputs will go, and 
        all the buttons to add/delete/save the stats. ALso the buttons
        to print the score, putts and GIR & FIR graphs.
        """
        #Create Title label at the top screen
        self.tag = tk.Label(
            self, text = "Golf Statistics Tracker", 
            font = ("Arial", 35, "bold"))
        self.tag.pack(pady=(15,2))

        #Create label design to be the same for all buttons
        self.input_design = tk.Frame(self)
        self.input_design.pack(pady=7)

        #Create label for club name.
        self.club_tag = tk.Label(
            self.input_design, text = "Golf club name:", 
            font = ("Arial", 15))
        self.club_tag.grid(row=0, column=0, padx=15, pady=7)
        #Create input space to enter club name. 
        self.club_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.club_input.grid(row=0, column=1, padx=15, pady=7)

        #Create label for date played.
        self.date_tag = tk.Label(
            self.input_design, text = "Date of round:", 
            font = ("Arial", 15))
        self.date_tag.grid(row=1, column=0, padx=15, pady=7)
        #Create input space to enter date played. 
        self.date_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.date_input.grid(row=1, column=1, padx=15, pady=7)

        #Create label for score.
        self.score_tag = tk.Label(
            self.input_design, text = "Score:", 
            font = ("Arial", 15))
        self.score_tag.grid(row=2, column=0, padx=15, pady=7)
        #Create input space to enter score.
        self.score_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.score_input.grid(row=2, column=1, padx=15, pady=7)

        #Create label for green in regulation percentage.
        self.gir_tag = tk.Label(
            self.input_design, text = "GIR %:", 
            font = ("Arial", 15))
        self.gir_tag.grid(row=3, column=0, padx=15, pady=7)
        #Create input space for green in regulation percentage.
        self.gir_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.gir_input.grid(row=3, column=1, padx=15, pady=7)

        #Create label for fairway in regulation percentage.
        self.fir_tag = tk.Label(
            self.input_design, text = "FIR %:", 
            font = ("Arial", 15))
        self.fir_tag.grid(row=4, column=0, padx=15, pady=7)
        #Create input space for fairway in regulation percentage.
        self.fir_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.fir_input.grid(row=4, column=1, padx=15, pady=7)

        #Create label for number of putts.
        self.putts_tag = tk.Label(
            self.input_design, text = "Number of putts:", 
            font = ("Arial", 15))
        self.putts_tag.grid(row=5, column=0, padx=15, pady=7)
        #Create input space for number of putts.
        self.putts_input = tk.Entry(
            self.input_design, font = ("Arial", 15), width=15)
        self.putts_input.grid(row=5, column=1, padx=15, pady=7)
        

        #Create button to add a new round to input frame.
        self.new_round_button = tk.Button( 
                self.input_design,                     
                text = "Add New Round", 
                background='white', fg='green',
                command = self.add_new_round)
        self.new_round_button.grid(row=1, column=5, padx=15, pady=7)  

        #Create button to delete round from input frame.
        self.delete_button = tk.Button(
            self.input_design,
            text = "Delete Round", 
            background='white', fg='red',
            command = self.delete_round)
        self.delete_button.grid(row=2, column=5, padx=15, pady=7)

        #Create button to save rounds to a csv document.
        self.save_button = tk.Button(
            self.input_design, 
            text = "Upload Rounds", 
            background='white', fg='blue',
            command = self.save_statistics)
        self.save_button.grid(row=3, column=5, padx=15, pady=7) 


        #Create a frame for input list.
        self.stats_list = tk.Frame(self)
        self.stats_list.pack(pady=10, padx=10)
        self.scrollbar = tk.Scrollbar(self.stats_list)
        self.scrollbar.pack(side ="right", fill = "y")
        self.scores_list = tk.Listbox(
            self.stats_list,
            font = ("Arial", 18),
            height = 7,
            width = 60,
            yscrollcommand = self.scrollbar.set)
        self.scores_list.pack(pady=10)
        self.scrollbar.config(command = self.scores_list.yview)


        #Create button that prints score per round trend graph.
        self.show_charts = tk.Button(
            self, 
            text = "Show Score Trends", 
            command = self.print_score_stats)
        self.show_charts.pack(pady=6)

        #Create a button that prints putts per round trend graph.
        self.show_charts = tk.Button(
            self, text = "Show Putting Trends", 
            command = self.print_putting_stats)
        self.show_charts.pack(pady=6)

        #Create a button that prints GIR & FIR percentages per round graph.
        self.show_charts = tk.Button(
            self, text = "Show GIR & FIR Graphs", 
            command = self.prints_GIR_FIR_stats)
        self.show_charts.pack(pady=6)


    def add_new_round(self):    
        """
        Function that adds input of the user to the frame list 
        and deletes the inputs so the user can input again.
        Checks if inputs are full and if the values are integers.
        """
        name = self.club_input.get()
        date = self.date_input.get()
        score = self.score_input.get()
        gir = self.gir_input.get() 
        fir = self.fir_input.get() 
        putt = self.putts_input.get()
        if name and date and score and gir and fir and putt:    # Checks if inputs are completed
            try:                                                # Checks if inputs are integers
                int(score)
                int(gir)
                int(fir)
                int(putt)
                self.scores.append((name, date, score, gir, fir, putt))
                self.scores_list.insert('end',
                    f"{name} , {date} , {score} , {gir} , {fir} , {putt}")
                self.club_input.delete(0, 'end')
                self.date_input.delete(0, 'end')
                self.score_input.delete(0, 'end')
                self.gir_input.delete(0, 'end')
                self.fir_input.delete(0, 'end')
                self.putts_input.delete(0, 'end')
            except:                                             # if not integers, error
                messagebox.showerror("Warning","Please enter a number")
        else:                                                   # if not full, error
            messagebox.showerror("Warning","Please complete all the fields")


    def delete_round(self):
        """
        Function that deletes all inputs from the frame.
        """
        choose_round = self.scores_list.curselection()
        if choose_round:
            choose_round = choose_round[0]
            del self.scores[choose_round]
            self.scores_list.delete(choose_round)


    def save_statistics(self):
        """
        Function that saves the statistics in the frame to a 
        csv file called golf-statistics.csv.
        Creates a document if not already existent. 
        """
        with open("Golf-Statistics.csv", "w", newline="") as csvfile:
            write = csv.writer(csvfile)
            headers = ["Golf Club Name", "Date of round",
                       "Score", "Green in Regulation as %",
                       "Fairway in Regulation as %",
                       "Number of putts per round"]
            write.writerow(headers)
            for s in self.scores:
                write.writerow(s)

            # Print message telling user the slides have been saved 
            # to the csv document.
            messagebox.showinfo("Info", "Stats saved to CSV document")


    def print_score_stats(self):   
        """
        Function that prints the graph of score per round trends
        with the average score per round from the csv file.
        """
        x = []
        y = []
        with open("golf-statistics.csv", "r") as csvfile:
            df = csv.reader(csvfile)     
            next(df)
            for row in df:
                x.append(row[0])
                y.append(int(row[2]))

        avg_sco = np.mean(y)                # Calculates average score
        plt.plot(x, y, color ='b', marker = 'o')
        plt.xlabel("Name of Club")
        plt.ylabel("Result")
        plt.title("Average Score per round (Avg: {:.2f})".format(avg_sco), fontsize=15)
        plt.grid()
        plt.axhline(
            y=np.nanmean(y),
            color='b',
            linestyle='--')
        plt.xticks(rotation=30, ha='right')
        plt.show()


    def print_putting_stats(self): 
        """
        Function that prints the graph of putting per round trends
        with the average per round number of putts from the csv file.
        """   
        x = []
        u = []
        with open("golf-statistics.csv", "r") as csvfile:
            df = csv.reader(csvfile)     
            next(df)
            for row in df:
                x.append(row[0])
                u.append(int(row[5]))

        avg_pu = np.mean(u)                         # Calculates average putts
        plt.plot(x, u, color ='g', marker = 'o')
        plt.xlabel("Name of Club")
        plt.ylabel("Putts")
        plt.title("Average Putts per round (Avg: {:.2f})".format(avg_pu), fontsize=15)
        plt.grid()
        plt.axhline(
            y=np.nanmean(u),
            color='g',
            linestyle='--')
        plt.xticks(rotation=30, ha='right')
        plt.show()

   
    def prints_GIR_FIR_stats(self):    
        """
        Function that prints the graph of GIR & FIR % per round trends
        from the csv file.
        """
        x = []
        q = []
        w = []
        with open("golf-statistics.csv", "r") as csvfile:
            df = csv.reader(csvfile)     
            next(df)
            for row in df:
                x.append(row[0])
                q.append(int(row[3]))
                w.append(int(row[4]))

        plt.plot(x, q, color ='m', marker = 'o', label = 'GIR')
        plt.plot(x, w, color ='y', marker = 'o', label = 'FIR')
        plt.xlabel("Name of Club")
        plt.ylabel("%")
        plt.title("Number of GIR and FIR % per round", fontsize=15)
        plt.legend()
        plt.grid()
        plt.xticks(rotation=30, ha='right')
        plt.show()
       