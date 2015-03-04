import csv
import re
import os
from collections import Counter

class AudioFileParser:

    """
    Reads entries from the audio word file.
    the audio_list member contains an AudioList
    object that's constructed from parsing the file

    """
    def __init__(self, audio_file):
        self.word_file = audio_file
        self.entries = self.check_and_parse()

    def check_and_parse(self):
        """
        Runs checks on  audio entry file to make sure the
        input is uniformly laid out (fixed number of
        words (i.e. columns) per line)

        Constructs an AudioList object, which contains a list
        of AudioEntry objects

        @return: AudioList object containing entries from the file
        """
        entries = []

        with open(self.word_file, "r") as file:
            num_of_columns = len(file.readline().split())


            for line in file:
                replaced_line = line.replace("\"", "")
                split_line = replaced_line.split()
                #if len(split_line) != num_of_columns:
                #   raise Exception("input file %s is not uniform" % file)


                entry = split_line
                if len(entry) == 2: # we only have word and count
                    entries.append(AudioEntry(word=entry[0], count=entry[1]))
                else:
                    entries.append(AudioEntry(word=entry[0], count=int(entry[1]),
                                              coder=entry[2], child=entry[3], visit=int(entry[4])))


        return entries
        #return AudioList(entries)

class VideoFileParser:

    """
    Reads entries from the video word file.
    the video_list member contains an VideoList
    object that's constructed from parsing the file

    """
    def __init__(self, video_file):
        self.word_file = video_file
        self.entries = self.check_and_parse()

    def check_and_parse(self):
        """
        Runs checks on  video entry file to make sure the
        input is uniformly laid out (fixed number of
        words (i.e. columns) per line)

        Constructs a VideoList object, which contains a list
        of VideoEntry objects

        @return: VideoList object containing entries from the file
        """
        entries = []

        with open(self.word_file, "r") as file:
            num_of_columns = len(file.readline().split())

            #file.seek(0)
            for line in file:

                replaced_line = line.replace("\"", "")
                split_line = replaced_line.split()

                #if len(split_line) != num_of_columns:
                #    print split_line
                #    raise Exception("input file %s is not uniform" % file)


                entry = split_line
                if len(entry) == 2:   # we only have word and count
                    entries.append(VideoEntry(word=entry[0], count=entry[1]))
                else:
                    entries.append(VideoEntry(word=entry[0], count=int(entry[1]),
                                              child=entry[2], coder=entry[3], visit=int(entry[4])))
        return entries


class GeneralWordParser:

    def __init__(self, general_file):
        self.general_word_file = general_file
        self.words = self.check_and_parse()

    def check_and_parse(self):

        words = []

        with open(self.general_word_file, "rU") as file:
            file.readline()
            for line in file:
                # check to make sure there is only 1 word per line
                if len(line.split()) != 1:
                    raise Exception(" incorrect formatting of input file")

                words.append(line.strip())

        return words

class MonthSpecificParser:

    def __init__(self, specific_file):
        self.word_file = specific_file
        self.months = []
        self.words = self.check_and_parse()

    def check_and_parse(self):

        words = []

        with open(self.word_file, "rU") as file:
            file.readline()     # first line (header)
            for line in file:
                entry = line.split()
                if len(entry) != 2:
                    raise Exception("input file contains irregular formatting")
                # TODO check that entry[1] is an integer
                #if not self.months:  # initially list is empty. insert first element
                #    self.months.append(int(entry[1]))
                if int(entry[1]) not in self.months:
                    self.months.append(int(entry[1]))
                words.append((entry[0], int(entry[1])))
        return words


class RawAudioDataParser:

    def __init__(self, raw_file):
        self.raw_filepath = raw_file

        self.month = None
        self.coder = None
        self.child = None
        self.filename = self.parse_filename()

        self.counted_words = None
        self.raw_entries = None
        self.entries = self.parse_file(self.raw_filepath)





    def parse_file(self, file):

        # entries[] is a list of AudioEntries
        # raw_entries[] is a list of RawAudioEntries
        entries = []
        raw_entries = []

        # words[] is a temporary list of those words
        words = []

        with open(file, 'rU') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                print ', '.join(row)
                if row[6] == "NA":
                    continue
                raw_entries.append(RawAudioEntry(row[0], row[1],
                                                 row[2], row[3],
                                                 row[4], row[5],
                                                 row[6]))
                words.append(row[6])

        self.raw_entries = raw_entries
        self.counted_words = Counter(words)

        self.parse_filename()

        for word in self.counted_words:
            entries.append(AudioEntry(word=word, visit=self.month,
                                      count=self.counted_words[word],
                                      coder= self.coder, child=self.child))
        return entries


    def parse_filename(self):
        """
        (ignore for now)
        Returns:
            the month number parsed from the filename
        """

        (filepath, filename) = os.path.split(self.raw_filepath)

        print filename

        filename_split = filename.split("_")
        self.child = int(filename_split[0])
        self.month = int(filename_split[1])
        coder_string = re.search("coder[A-Z]+", filename)
        if coder_string:  # make sure there's a match
            self.coder = coder_string.group().split("coder")[1]
        else:
            print "This file has no \"coder\" tag embeded in the filename"
        print self.coder
        print filename_split

        return filename



        #return visit


class RawVideoDataParser:

    def __init__(self, raw_file):
        self.raw_filepath = raw_file

        self.month = None
        self.coder = None
        self.child = None
        self.filename = self.parse_filename()

        self.counted_words = None
        self.raw_entries = None
        self.entries = self.parse_file(self.raw_filepath)




    def parse_file(self, file):

        # entries[] is a list of AudioEntries
        # raw_entries[] is a list of RawAudioEntries
        entries = []
        raw_entries = []

        # words[] is a temporary list of those words
        words = []

        with open(file, 'rU') as file:
            reader = csv.reader(file, delimiter=',')
            for row in reader:
                print ', '.join(row)
                if row[7] == "NA":
                    continue
                raw_entries.append(RawVideoEntry(row[0], row[1],
                                             row[2], row[3],
                                             row[4], row[5],
                                             row[6], row[7]))
                words.append(row[7])

        self.raw_entries = raw_entries
        self.counted_words = Counter(words)

        for word in self.counted_words:
            entries.append(VideoEntry(word=word, visit=self.month,
                                      count=self.counted_words[word],
                                      coder= self.coder, child=self.child))
        return entries

    def parse_filename(self):
        """
        (ignore for now)
        Returns:
            the month number parsed from the filename
        """

        (filepath, filename) = os.path.split(self.raw_filepath)

        print filename

        filename_split = filename.split("_")
        self.child = int(filename_split[0])
        self.month = int(filename_split[1])
        coder_string = re.search("coder[A-Z]+", filename)
        if coder_string:  # make sure there's a match
            self.coder = coder_string.group().split("coder")[1]
        else:
            print "This file has no \"coder\" tag embeded in the filename"
        print self.coder
        print filename_split

        return filename




class VideoList:

    def __init__(self, entry_list):
        self.entries = entry_list

class AudioList:

    def __init__(self, entry_list):
        self.entries = entry_list




class VideoEntry(object):

    def __init__(self, word, count, child="", coder="", visit=0):
        self.word = word
        self.count = count
        self.child = child
        self.coder = coder
        self.visit = visit
        self.in_general = None
        self.rank = None

    def __repr__(self):
        return "{}: {} {} {} {}".format(self.word,
                                        self.count,
                                        self.child,
                                        self.coder,
                                        self.visit)
    def __cmp__(self, other):
        if hasattr(other, 'count'):
            return self.count.__cmp__(other.count)

class AudioEntry(object):

    def __init__(self, word, count, child="", coder="", visit=0):
        self.word = word
        self.count = count
        self.child = child
        self.coder = coder
        self.visit = visit
        self.in_general = None
        self.rank = None

    def __repr__(self):
        return "{}: {} {} {} {}".format(self.word,
                                        self.count,
                                        self.child,
                                        self.coder,
                                        self.visit)
    def __cmp__(self, other):
        if hasattr(other, 'count'):
            return self.count.__cmp__(other.count)


#############
# Raw Entries are those taken from the csv files
#####
class RawAudioEntry:

    def __init__(self, tier, word, utterance, object_present, speaker, time, basic_level):
        self.tier = tier
        self.word = word
        self.utterance = utterance
        self.object_present = object_present
        self.speaker = speaker
        self.time = time
        self.basic_level = basic_level

class RawVideoEntry:

    def __init__(self, ordinal, onset, offset,
                 object, utterance, object_present,
                 speaker, basic_level):
        self.ordinal = ordinal
        self.onset = onset
        self.offset = offset
        self.object = object
        self.utterance = utterance
        self.object_present = object_present
        self.speaker = speaker
        self.basic_level = basic_level



