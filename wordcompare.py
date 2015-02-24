from Tkinter import *
import tkFileDialog
from collections import Counter
import operator
import parser

from parser import *


class MainWindow:

    def __init__(self, master):

        # general session variables:

        self.general_parser = None      # general words
        self.general_file = None        # general word file (string representing absolute path)

        self.specific_parser = None     # month specific words
        self.specific_file = None       # month specific word file (string representing absolute path)

        self.general_words = None
        self.specific_month_words = None    # words from selected month

        self.audio_parser = None        # parser for audio file
        self.audio_data_parser = None   # parser for raw word list
        self.audio_file = None          # audio file (string representing absolute path)

        self.video_parser = None        # parser for audio file
        self.video_data_parser = None   # parser for raw word list
        self.video_file = None          # video file (string representing absolute path)

        self.audio_entries = None
        self.video_entries = None


        self.root = master                  # main GUI context
        self.root.title("Word Compare")     # title of window
        self.root.geometry("1100x660")      # size of GUI window
        self.main_frame = Frame(root)       # main frame into which all the Gui components will be placed
        self.main_frame.pack()              # pack() basically sets up/inserts the element (turns it on)


        self.month_selected = None          # number indicating what month the user selected

        self.top_unique_audio_num = None    # N for audio words
        self.top_unique_video_num = None    # N for video words

        self.top_unique_audio = None        # list of top N unique audio words
        self.top_unique_video = None        # list of top N unique video words

        self.unique_audio_found = False     # make sure unique audio is found before exporting
        self.unique_video_found = False     # make sure unique video is found before exporting

        # declare the basic buttons:

        # general
        self.load_general_button = Button(self.main_frame,
                                          text= "Load General Words",
                                          command=self.load_general)
        self.clear_general_button = Button(self.main_frame,
                                           text= "Clear",
                                           command=self.clear_general)

        # month specific
        self.load_specific_button = Button(self.main_frame,
                                           text= "Load Month Specific",
                                           command=self.load_specific)
        self.clear_specific_button = Button(self.main_frame,
                                            text= "Clear",
                                            command=self.clear_specific)

        # audio
        self.load_audio_button = Button(self.main_frame,
                                        text= "Load Audio Words",
                                        command=self.load_audio)
        self.clear_audio_button = Button(self.main_frame,
                                         text= "Clear",
                                         command=self.clear_audio)


        self.load_raw_audio_button = Button(self.main_frame,
                                     text= "Load Raw Data",
                                     command=self.load_audio_data)

        self.export_audio_counts_button = Button(self.main_frame,
                                                 text = "Export Counts",
                                                 command = self.export_audio_counts)


        # video
        self.load_video_button = Button(self.main_frame,
                                        text= "Load Video Words",
                                        command=self.load_video)
        self.clear_video_button = Button(self.main_frame,
                                         text= "Clear",
                                         command=self.clear_video)

        self.load_raw_video_button = Button(self.main_frame,
                                            text= "Load Raw Data",
                                            command=self.load_video_data)

        self.export_video_counts_button = Button(self.main_frame,
                                                 text = "Export Counts",
                                                 command = self.export_video_counts)

        # find top N unique
        self.find_top_audio_button = Button(self.main_frame,
                                            text="Find",
                                            command=self.load_top_audio)

        self.find_top_video_button = Button(self.main_frame,
                                            text="Find",
                                            command=self.load_top_video)

        # clear unique
        self.clear_unique_audio_button = Button(self.main_frame,
                                                text = "Clear",
                                                command = self.clear_unique_audio)

        self.clear_unique_video_button = Button(self.main_frame,
                                                text = "Clear",
                                                command = self.clear_unique_video)

        # clear all
        self.clear_button = Button(self.main_frame,
                                   text="Clear All",
                                   command=self.clear_all)

        self.export_button = Button(self.main_frame,
                                    text="Export",
                                    command=self.export)

        # exit program
        self.quit_button = Button(self.main_frame,
                                  text="Quit",
                                  command=quit)

        # pack() the buttons at the bottom of the screen
        self.load_general_button.grid(row = 10, column = 0)
        self.clear_general_button.grid(row = 11, column = 0)

        self.load_specific_button.grid(row = 10, column = 1)
        self.clear_specific_button.grid(row = 11, column = 1)

        self.load_audio_button.grid(row = 10, column = 2)
        self.clear_audio_button.grid(row = 11, column = 2)
        self.load_raw_audio_button.grid(row = 12, column = 2)
        self.export_audio_counts_button.grid(row=13, column=2)

        self.load_video_button.grid(row = 10, column = 3)
        self.clear_video_button.grid(row = 11, column = 3)
        self.load_raw_video_button.grid(row = 12, column = 3)
        self.export_video_counts_button.grid(row=13, column=3)

        self.find_top_audio_button.grid(row = 11, column = 4)
        self.find_top_video_button.grid(row = 11, column = 5)

        self.clear_unique_audio_button.grid(row=12, column = 4)
        self.clear_unique_video_button.grid(row=12, column = 5)


        self.export_button.grid(row = 10, column = 6)
        self.clear_button.grid(row = 11, column = 6)


        # set up General Box
        self.general_box_label = Label(self.main_frame, text = "General Words")
        self.general_box_label.grid(columnspan=1, row = 2, column = 0)
        self.general_box = Listbox(self.main_frame, width=15, height = 27)
        self.general_box.grid(columnspan=1, row = 3, column = 0, padx=0, pady=0)

        #set up Month Specific Box
        self.specific_box_label = Label(self.main_frame, text = "Month Specific")
        self.specific_box_label.grid(columnspan=1, row = 2, column = 1)
        self.specific_box = Listbox(self.main_frame, width=15, height = 27)
        self.specific_box.grid(columnspan=1, row = 3, column = 1, padx=10, pady=0)

        #set up Audio Word Box
        self.audio_box_label = Label(self.main_frame, text = "Audio Words")
        self.audio_box_label.grid(columnspan=1, row = 2, column = 2)
        self.audio_box = Listbox(self.main_frame, width=15, height = 27)
        self.audio_box.grid(columnspan=1, row = 3, column = 2, padx=10, pady=0)

        # set up Video Word Box
        self.video_box_label = Label(self.main_frame, text = "Video Words")
        self.video_box_label.grid(columnspan=1, row = 2, column = 3)
        self.video_box = Listbox(self.main_frame, width=15, height = 27)
        self.video_box.grid(columnspan=1, row = 3, column = 3, padx=10, pady=0)

        # text entry box for entering top N for audio words
        self.top_unique_audio_entry = Entry(self.main_frame, width=10)
        self.top_unique_audio_entry.grid(row = 10, column = 4)

        # text entry box for entering top N for video words
        self.top_unique_video_entry = Entry(self.main_frame, width=10)
        self.top_unique_video_entry.grid(row = 10, column = 5)

        # title and box for unique audio words
        self.top_unique_audio_label = Label(self.main_frame, text = "Top N Unique Audio")
        self.top_unique_audio_label.grid(columnspan=1, row = 2, column = 4)
        self.top_unique_audio_box = Listbox(self.main_frame, width=17, height = 27)
        self.top_unique_audio_box.grid(columnspan=1, row = 3, column = 4, padx=10, pady=0)

        # title and box for unique video words
        self.top_unique_video_label = Label(self.main_frame, text = "Top N Unique Video")
        self.top_unique_video_label.grid(columnspan=1, row = 2, column = 5)
        self.top_unique_video_box = Listbox(self.main_frame, width=17, height = 27)
        self.top_unique_video_box.grid(columnspan=1, row = 3, column = 5, padx=10, pady=0)

        # warning when trying to perform operation that requires files that are missing
        self.missing_files_label = Label(self.main_frame,
                                         fg="red",
                                         text="You need to load\nappropriate files")

        # warning text if no month selected
        self.no_month_selected_label = Label(self.main_frame,
                                             fg="red",
                                             text = "You need to select\na month")

        # warning text if entered N is greater than the number of unique words in the list.
        # It isn't initialized here because we don't know what N is until the user calls
        # the
        self.top_n_too_large_label = None

        self.cant_export_label = Label(self.main_frame, fg="red",
                                       text="Can't export: \nMake sure\nessential files\nand variables\nare set")

    # general words
    def load_general(self):

        self.general_file = tkFileDialog.askopenfilename()
        self.general_parser = GeneralWordParser(self.general_file)

        for index, word in enumerate(self.general_parser.words):
            self.general_box.insert(index, word)

    def clear_general(self):
        self.general_file = None
        self.general_parser = None

        self.general_box.delete(0, END)

    # load month specific word file
    def load_specific(self):

        self.specific_file = tkFileDialog.askopenfilename()
        self.specific_parser = MonthSpecificParser(self.specific_file)

        for index, (word, month) in enumerate(self.specific_parser.words):
            self.specific_box.insert(index, word + " - " + str(month))

        select_month = Menubutton(self.main_frame, text="Month #: ")

        month_menu = Menu(select_month)
        select_month.config(menu=month_menu)


        for month in self.specific_parser.months:
            if month == 6:
                continue
            month_menu.add_command(label=str(month), command=lambda month=month: self.load_specific_month(month))

        select_month.grid(row = 12, column = 1)


    def load_specific_month(self, month_selected):
        """
        Takes an integer as month selected.
        Sets that number as the global variable self.month_selected.
        Clear the specific word box if it's already filled with something.
        Iterate through the specific_parser's "words" member. It is
        a list of tuples (word, month). If month = month_selected, toss
        that corresponding word into the specific_month_words list.
        Then iterate through those specific_month_words and insert them
        into the GUI box for specific words
        """
        if month_selected == 6:
            raise Exception("month 6 is not available for selection")
        self.month_selected = month_selected
        self.specific_box.delete(0, END)

        self.specific_month_words = []

        for (word, month) in self.specific_parser.words:
            if month == month_selected:
                self.specific_month_words.append(word)

        for index, word in enumerate(self.specific_month_words):
            self.specific_box.insert(index, word + " - " + str(self.month_selected))

    def clear_specific(self):
        """
        Clear entry for specific_file path,
        clear the accompanying parser,
        and erase the specific word GUI box
        """
        self.specific_file = None
        self.specific_parser = None

        self.specific_box.delete(0, END)

    # audio word list
    def load_audio(self):
        """
        Prompt the user for the audio word file.
        Save the selected file's absolute path and
        construct an AudioFileParser with it.
        Fill the audio words GUI box with the words
        returned in the parser's "entries" member
        """

        self.audio_file = tkFileDialog.askopenfilename()
        self.audio_parser = AudioFileParser(self.audio_file)

        self.audio_entries = self.audio_parser.entries

        for index, entry in enumerate(self.audio_parser.entries):
            self.audio_box.insert(index, entry.word)

    def clear_audio(self):
        """
        Clear entry for audio_file path,
        clear the accompanying parser,
        and erase the audio word GUI box
        """
        self.audio_file = None
        self.audio_parser = None

        self.audio_box.delete(0, END)

    def load_audio_data(self):
        """
        Builds the audio word list from raw word collection data
        in the form of .csv files
        """

        self.audio_data = tkFileDialog.askopenfilename()
        self.audio_data_parser = RawAudioDataParser(self.audio_data)

        self.audio_entries = sorted(self.audio_data_parser.entries, key=self.get_count, reverse=True)

        for index, entry in enumerate(self.audio_entries):
            self.audio_box.insert(index, entry.word)


    # video word list
    def load_video(self):
        """
        Prompt the user for the video word file.
        Save the selected file's absolute path and
        construct an VideoFileParser with it.
        Fill the video words GUI box with the words
        returned in the parser's "entries" member
        """
        self.video_file = tkFileDialog.askopenfilename()
        self.video_parser = VideoFileParser(self.video_file)

        self.video_entries = self.video_parser.entries

        for index, entry in enumerate(self.video_entries):
            self.video_box.insert(index, entry.word)

    def clear_video(self):
        """
        Clear entry for video_file path,
        clear the accompanying parser,
        and erase the video word GUI box
        """
        self.video_file = None
        self.video_parser = None

        self.video_box.delete(0, END)

    def load_video_data(self):

        self.video_data = tkFileDialog.askopenfilename()
        self.video_data_parser = RawVideoDataParser(self.video_data)

        self.video_entries = sorted(self.video_data_parser.entries, key=self.get_count, reverse=True)

        for index, entry in enumerate(self.video_entries):
            self.video_box.insert(index, entry.word)


    def load_top_audio(self):
        """
        Check to make sure general, specific, and audio
        parsers have been initialized.
        Display warning if no month selected.
        Call find_top_unique(), using the top_unique_audio_entry box's
        value as the argument for N.
        Delete existing entries in the top unique audio GUI box.
        Load the new entries into the GUI box
        """

        if self.general_parser is None or \
           self.specific_parser is None or \
                ((self.audio_parser is None) and (self.audio_data_parser is None)):
            self.missing_files_label.grid(row=13, column=4)
            raise Exception("you need to load the general, month-specific, and audio words first")
        else:
            self.missing_files_label.grid_remove()


        if self.month_selected is None:
            self.no_month_selected_label.grid(row=13, column=4, columnspan=1)
        else:
            self.no_month_selected_label.grid_remove()

        self.top_unique_audio = self.find_top_unique(self.audio_entries,
                                                     int(self.top_unique_audio_entry.get()))

        self.top_unique_audio_box.delete(0, END)

        box_count = 0
        for rank, words in enumerate(self.top_unique_audio):
            for index, word in enumerate(words):
                self.top_unique_audio_box.insert(box_count,
                                                 str(word.rank)+ ". " +
                                                 word.word +
                                                 " - " + str(word.count))
                box_count = box_count + 1

        self.unique_audio_found = True

    def clear_unique_audio(self):
        """
        Clear text in top_unique_audio_entry and GUI box,
        """
        self.top_unique_audio_entry.delete(0, END)
        self.top_unique_audio_box.delete(0, END)
        self.unique_audio_found = False
        self.missing_files_label.grid_remove()

    def load_top_video(self):
        """
        Check to make sure general, specific, and video
        parsers have been initialized.
        Display warning if no month selected.
        Call find_top_unique(), using the top_unique_audio_entry box's
        value as the argument for N.
        Delete existing entries in the top unique audio GUI box.
        Load the new entries into the GUI box
        """

        if self.general_parser is None or \
           self.specific_parser is None or \
                ((self.video_parser is None) and (self.video_data_parser is None)):
            self.missing_files_label.grid(row=13, column=5)
            raise Exception("you need to load the general, month-specific, and video words first")
        else:
            self.missing_files_label.grid_remove()


        if self.month_selected is None:
            self.no_month_selected_label.grid(row=14, column=5, columnspan=1)
        else:
            self.no_month_selected_label.grid_remove()

        self.top_unique_video = self.find_top_unique(self.video_entries,
                                                     int(self.top_unique_video_entry.get()))

        self.top_unique_video_box.delete(0, END)

        box_count = 0
        for rank, words in enumerate(self.top_unique_video):
            for index, word in enumerate(words):
                self.top_unique_video_box.insert(box_count,
                                                 str(word.rank)+ ". " +
                                                 word.word +
                                                 " - " + str(word.count))
                box_count = box_count + 1

        self.unique_video_found = True

    def clear_unique_video(self):
        """
        Clear text in top_unique_audio_entry and GUI box,
        """
        self.top_unique_video_entry.delete(0, END)
        self.top_unique_video_box.delete(0, END)
        self.unique_video_found = False
        self.missing_files_label.grid_remove()

    def find_top_unique(self, list_of_entries, top_n):
        """
        If N is greater than the number of unique words,
        raise exception and display warning on the GUI (and
        check which box to write GUI warning under based on
        the type of the elements in the list_of_entries).

        Sort the list_of_entries by descending count. This is
        done by passing the get_count() function as the value
        to the key= parameter in the sorted() function.

        Loop through the sorted list, checking:
            1. if word is in general list:
                    set that entry's "in_general" field to True, else it's false
            2. if word is not in month specific list:
                    add that entry to the back of the unique_entries[] list

                    use the present size of the unique_entries[] list to represent
                    the rank of the word relative to the other unique words

        Finally, return a slice of the unique_entries[] list, from index 0-N

        """


        if len(list_of_entries) < top_n:
            self.top_n_too_large_label = Label(self.main_frame,
                                               fg="red",
                                               text="Max N = %s" % len(list_of_entries))
            if type(list_of_entries[0]) is AudioEntry:
                self.top_n_too_large_label.grid(row=13, column=4)
            if type(list_of_entries[0]) is VideoEntry:
                self.top_n_too_large_label.grid(row=13, column=5)
            raise Exception("N is larger than the total number of words")

        if self.top_n_too_large_label is not None:
            self.top_n_too_large_label.grid_remove()

        sorted_by_count = sorted(list_of_entries, key=self.get_count, reverse=True)
        #self.top_n_too_large_label = Label(self.main_frame, fg="red", text="Max N = %s" % len(list_of_entries))
        unique_entries = [[] for i in range(top_n)]

        curr_rank = 0
        prev_count = 0
        curr_count = 0

        for entry in sorted_by_count:

            if entry.word in self.general_parser.words:
                entry.in_general = True
            else:
                entry.in_general = False

            if curr_count == 0:
                unique_entries[curr_rank].append(entry)
                prev_count = entry.count
                entry.rank = 1
                curr_count = 5 # random number, just to get past this if statement
                continue


            curr_count = entry.count



            if curr_rank >= top_n:
                break



            if entry.word not in self.specific_month_words:
                # increment rank if current entry has a different count
                # (the last set of entries having this count are all filled
                #  into the unique_entries[])
                if curr_count != prev_count:
                    curr_rank = curr_rank + 1
                    if curr_rank >= top_n:
                        break
                    unique_entries[curr_rank].append(entry)
                    prev_count = entry.count
                    entry.rank = curr_rank + 1
                    continue
                unique_entries[curr_rank].append(entry)
                entry.rank = curr_rank + 1



        return unique_entries[0:curr_rank + 1]


    def get_count(self, entry):
        """
        Special function used solely for passing to the sorted()
        function when sorting lists. Designates the count as the
        key by which to sort the values by
        """
        return entry.count



    def get_count_from_rank(self, rank_list):
        return rank_list[0].count


    def set_top_unique_num(self, number):
        """
        Sets "number" as the value entered by the user for top N
        """
        self.top_unique_num = number


    def export_audio_counts(self):

        export_file = tkFileDialog.asksaveasfilename()

        with open(export_file, "w") as file:

            file.write("\"basic_level\"   \"freq\"   \"coder\"   \"child\"   \"visit\"\n")

            for entry in self.audio_entries:
                visit = entry.visit
                if visit == 9999:
                    visit = ""
                file.write(entry.word + "   " + str(entry.count) + "    " +
                           entry.coder + "    " + str(entry.child) + "    " +
                           str(visit) + "\n")

    def export_video_counts(self):

        export_file = tkFileDialog.asksaveasfilename()

        with open(export_file, "w") as file:

            file.write("\"basic_level\"   \"freq\"   \"coder\"   \"child\"   \"visit\"\n")


            for entry in self.video_entries:
                visit = entry.visit
                if visit == 9999:
                    visit = ""
                file.write(entry.word + "   " + str(entry.count) + "    " +
                           entry.coder + "    " + str(entry.child) + "    " +
                           str(visit) + "\n")

    def export(self):
        """
        Checks to make sure the session state is exportable,
        prints warning on GUI and throws exception if not,
        then prompts user to select output file for exporting.
        It then concatenates the two unique words lists (audio + video)
        into a single list, then sorts that combined list by descending count.

        It first prints the header (describing each column). Then it
        iterates over the combined/sorted list and handles printing the
        entry to file based on whether the type of the entry is either
        AudioEntry or VideoEntry. This produces a final output where the
        entries are interleaved.
        """
        # check that session state is exportable
        if self.general_parser is None or \
           self.specific_parser is None or \
                ((self.audio_parser is None) and (self.audio_data_parser is None)) or \
                ((self.video_parser is None) and (self.video_data_parser is None)) or \
           self.month_selected is None or \
           self.unique_audio_found is False or \
           self.unique_video_found is False:

            self.cant_export_label.grid(row=13, column=6, columnspan=1, rowspan=5)
            raise Exception("you need to load the general, "
                            "month-specific, "
                            "audio and video words first")

        self.cant_export_label.grid_remove()
        export_file = tkFileDialog.asksaveasfilename() # ask for output file

        unique_words = self.top_unique_audio + self.top_unique_video # concatenate
        unique_words = sorted(unique_words, key=self.get_count_from_rank, reverse=True) # sort

        with open(export_file, "w") as file:
            file.write("rank   source   word      in_general  count\n") # print header
            for rank in unique_words:

                for entry in rank:

                    if type(entry) is AudioEntry: # if entry is AudioEntry, print it as such
                        file.write(str(entry.rank) + "      audio   " +
                                   entry.word + "      " +
                                   str(entry.in_general) + "  " +
                                   str(entry.count) + "\n")
                    else: # if entry is VideoEntry, print it as such
                        file.write(str(entry.rank) + "      video   " +
                                   entry.word + "      " +
                                   str(entry.in_general) + "  " +
                                   str(entry.count) + "\n")


    def clear_all(self):
        """
        Sets all the files, parsers, and session specific
        variables to 0. Also clears all the GUI boxes and warnings
        """

        self.general_file = None
        self.general_parser = None

        self.specific_file = None
        self.specific_parser = None

        self.audio_file = None
        self.audio_parser = None

        self.video_file = None
        self.video_parser = None


        self.top_unique_num = None

        self.general_box.delete(0, END)
        self.specific_box.delete(0, END)
        self.audio_box.delete(0, END)
        self.video_box.delete(0, END)
        self.top_unique_audio_box.delete(0, END)
        self.top_unique_video_box.delete(0, END)

        self.top_unique_audio_entry.delete(0, END)
        self.top_unique_video_entry.delete(0, END)

        if self.missing_files_label is not None:
            self.missing_files_label.grid_remove()
        if self.no_month_selected_label is not None:
            self.no_month_selected_label.grid_remove()
        if self.top_n_too_large_label is not None:
            self.top_n_too_large_label.grid_remove()
        if self.cant_export_label is not None:
            self.cant_export_label.grid_remove()

if __name__ == "__main__":

    root = Tk()
    MainWindow(root)
    root.mainloop()
