# 6.0001/6.00 Problem Set 5 - RSS Feed Filter
# Name:
# Collaborators:
# Time:

import feedparser
import string
import time
import threading
from project_util import translate_html
from mtTkinter import *
from datetime import datetime
import pytz
#import datetime
import copy

#-----------------------------------------------------------------------

#======================
# Code for retrieving and parsing
# Google and Yahoo News feeds
# Do not change this code
#======================

def process(url):
    """
    Fetches news items from the rss url and parses them.
    Returns a list of NewsStory-s.
    """
    feed = feedparser.parse(url)
    entries = feed.entries
    ret = []
    for entry in entries:
        guid = entry.guid
        title = translate_html(entry.title)
        link = entry.link
        description = translate_html(entry.description)
        pubdate = translate_html(entry.published)

        try:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %Z")
            pubdate.replace(tzinfo=pytz.timezone("GMT"))
          #  pubdate = pubdate.astimezone(pytz.timezone('EST'))
          #  pubdate.replace(tzinfo=None)
        except ValueError:
            pubdate = datetime.strptime(pubdate, "%a, %d %b %Y %H:%M:%S %z")

        newsStory = NewsStory(guid, title, description, link, pubdate)
        ret.append(newsStory)
    return ret

#======================
# Data structure design
#======================

# Problem 1

# TODO: NewsStory

#define a class called news story. 
class NewsStory(object):
    # this will take a guid, title, description, link, pubDate, and category
    def __init__(self, guid, title, description, link, pubDate):
        self.guid = guid
        self.title = title
        self.description = description
        self.link = link
        self.pubDate = pubDate

    # create getter methods for each of the arguments
    def get_guid(self):
        return(self.guid)
    def get_title(self):
        return(self.title)
    def get_description(self):
        return(self.description)
    def get_link(self):
        return(self.link)
    def get_pubdate(self):
        return(self.pubDate)

    # create a str method that pronts everything sequentially.
    def __str__(self):
        return('GUID: '+ self.get_guid()+ '\n'+ 'title: '+ self.get_title()+ '\n'+ 'description: '+ self.get_description()+ '\n'+ 'link: '+ self.get_link()+ '\n'+ 'publish date: '+ str(self.get_pubdate()))


#======================
# Triggers
#======================

class Trigger(object):
    def evaluate(self, story):
        """
        Returns True if an alert should be generated
        for the given news item, or False otherwise.
        """
        # DO NOT CHANGE THIS!
        raise NotImplementedError

# PHRASE TRIGGERS

# Problem 2
# TODO: PhraseTrigger

# first, define a class called phase trigger
class PhraseTrigger(Trigger):

    # this will take a string, phrase.
    def __init__(self, trigger):
        self.trigger = trigger
    # define getter methods
    def get_trigger(self):
        return(self.trigger)
    # define the is_phrase_in method, which takes a string trigger
    def is_phrase_in(self, text):
        text_simple = text.lower()
        for c in text_simple:
            if c in string.punctuation:
                text_simple = text_simple.replace(c, ' ')
        text_simple = ' '.join(text_simple.split())
            
        # check to see if trigger is in phrase, ignoring capitalisation and punctuation
        trigger = self.get_trigger().lower()
        return(' '+trigger+' ' in ' '+text_simple+' ')
# Problem 3

# first, define a class called title trigger that inherits the phrase trigger class and takes a news story object as an argument
class TitleTrigger(PhraseTrigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    # getter methods
    def get_trigger(self):
        return(self.trigger)
        
    
    # use the is phrase in method to see if the trigger is in the title
    def evaluate(self, news_story):
        title = news_story.get_title()
        return(self.is_phrase_in(title))
    

# Problem 4

# this is identical to the title trigger class except it checks the description

class DescriptionTrigger(PhraseTrigger):
    def __init__(self, trigger):
        self.trigger = trigger
    
    # getter methods
    def get_trigger(self):
        return(self.trigger)
        
    
    # use the is phrase in method to see if the trigger is in the description
    def evaluate(self, news_story):
        description = news_story.get_description()
        return(self.is_phrase_in(description))
    

# TIME TRIGGERS

# Problem 5
# TODO: TimeTrigger
# Constructor:
#        Input: Time has to be in EST and in the format of "%d %b %Y %H:%M:%S".
#        Convert time from string to a datetime before saving it as an attribute.

    # define a class called TimeTrigger that takes a string "time_string"
class TimeTrigger(Trigger):
    def __init__(self, time_string):
        self.time_string = time_string
    
    # getter methods
    def get_time_string(self):
        return(self.time_string)
    
    # convert the string into a datetime with the datetime.strptime method
    def convert_time(self):
        time_string = self.get_time_string()
        time_datetime = datetime.strptime(time_string, '%d %b %Y %H:%M:%S')
    
    # set the datetime as an attribute
        self.time_datetime = time_datetime
        return(time_datetime)
# Problem 6
# TODO: BeforeTrigger and AfterTrigger

 # define a class called before trigger that takes a trigger datetime  
class BeforeTrigger(TimeTrigger):
    def __init__(self, time_string):
            self.time_string = time_string
    
    # getter methods
    def get_time_string(self):
        return(self.time_string)
    
    # make a method which takes a news_story, and returns wetehr or not the pubdate is before the datetime
    def evaluate(self, news_story):
        return(news_story.get_pubdate() < self.convert_time())
    

# after trigger is identical to before trigger, but with the > changed to a <

class AfterTrigger(TimeTrigger):
    def __init__(self, time_string):
            self.time_string = time_string
    
    # getter methods
    def get_time_string(self):
        return(self.time_string)
    
    # make a method which takes a news_story, and returns wetehr or not the pubdate is before the datetime
    def evaluate(self, news_story):
        return(news_story.get_pubdate() > self.convert_time())
    

# COMPOSITE TRIGGERS

# Problem 7
# TODO: NotTrigger

# define a class called not trigger which takes one argument, called class_trigger'
class NotTrigger(Trigger):
    def __init__(self, class_trigger):
        self.class_trigger = class_trigger

    # getter methods    
    def get_class_trigger(self):
        return(self.class_trigger)

    # run the evaluate function on class trigger and return the opposite of what it returns
    def evaluate(self, news_story):
        class_trigger = self.get_class_trigger()
        return(not class_trigger.evaluate(news_story))

# Problem 8
# TODO: AndTrigger

# define a class and trigger which takes 2 arguments, trigger1 and 2
class AndTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    # getter methods
    def get_trigger1(self):
        return(self.trigger1)
    def get_trigger2(self):
        return(self.trigger2)
        
    # run the evaluate function on both triggers and return them with an and operator
    def evaluate(self, news_story):
        trigger1 = self.get_trigger1()
        trigger2 = self.get_trigger2()
        return(trigger1.evaluate(news_story) and trigger2.evaluate(news_story))

# Problem 9
# TODO: OrTrigger

# same as and but with or

class OrTrigger(Trigger):
    def __init__(self, trigger1, trigger2):
        self.trigger1 = trigger1
        self.trigger2 = trigger2

    # getter methods
    def get_trigger1(self):
        return(self.trigger1)
    def get_trigger2(self):
        return(self.trigger2)
        
    # run the evaluate function on both triggers and return them with an and operator
    def evaluate(self, news_story):
        trigger1 = self.trigger1
        trigger2 = self.trigger2
        return(trigger1.evaluate(news_story) or trigger2.evaluate(news_story))


#======================
# Filtering
#======================

# Problem 10
def filter_stories(stories, triggerlist):
    """
    Takes in a list of NewsStory instances.

    Returns: a list of only the stories for which a trigger in triggerlist fires.
    """
    # TODO: Problem 10
    # This is a placeholder
    # (we're just returning all the stories, with no filtering)

    # make a for loop over all the triggers
    filtered_stories = []
    for t in triggerlist:
        
        # make another for loop which checks each of the stories to see if it fits the current trigger
        for s in stories:
            if t.evaluate(s) and s not in filtered_stories:

        # if it does, add it to a new list of filtered storues
                filtered_stories.append(s)
        
    # return filtered stories
    return(filtered_stories)
#======================
# User-Specified Triggers
#======================
# Problem 11
def read_trigger_config(filename):
    """
    filename: the name of a trigger configuration file

    Returns: a list of trigger objects specified by the trigger configuration
        file.
    """
    # We give you the code to read in the file and eliminate blank lines and
    # comments. You don't need to know how it works for now!
    trigger_file = open(filename, 'r')
    lines = []
    for line in trigger_file:
        line = line.rstrip()
        if not (len(line) == 0 or line.startswith('//')):
            lines.append(line)

    # TODO: Problem 11
    # line is the list of lines that you need to parse and for which you need
    # to build triggers

    # print(lines) # for now, print it so you see what it contains!
    
    # create an empty dictionary trigger dict which will hold the first elemnt of the trigger as a key and a list of all other elements
    trigger_dict = {}
    
    # add all the elemts to the dict
    for l in lines:
        l_list = l.split(',')
        trigger_dict[l_list[0]] = l_list[1:]
    # loop over the first element of the lists in trigger dict to get the type of class beign called. ignore it if the key is ADD
    trigger_list = []
    for k in trigger_dict:
        if trigger_dict[k][0] == 'TITLE':
            trigger_dict[k] = TitleTrigger(trigger_dict[k][1])
        elif trigger_dict[k][0] == 'DESCRIPTION':
            trigger_dict[k] = DescriptionTrigger(trigger_dict[k][1])
        elif trigger_dict[k][0] == 'AFTER':
            trigger_dict[k] = AfterTrigger(trigger_dict[k][1])
        elif trigger_dict[k][0] == 'BEFORE':
            trigger_dict[k] = BeforeTrigger(trigger_dict[k][1])
        elif trigger_dict[k][0] == 'NOT':
            trigger_dict[k] = NotTrigger(trigger_dict[trigger_dict[k][1]], trigger_dict[k][2])
        elif trigger_dict[k][0] == 'AND':
            trigger_dict[k] = AndTrigger(trigger_dict[trigger_dict[k][1]], trigger_dict[k][2])
        elif trigger_dict[k][0] == 'OR':
            trigger_dict[k] = OrTrigger(trigger_dict[trigger_dict[k][1]], trigger_dict[k][2])
    print(trigger_dict)
        # check to see the key called ADD. add all its elements to a list trigger list
    for k in trigger_dict:
        if k == 'ADD':
            for l in trigger_dict[k]:
                trigger_list.append(trigger_dict[l])
        
    # return trigger list
    return(trigger_list)

SLEEPTIME = 120 #seconds -- how often we poll

def main_thread(master):
    # A sample trigger list - you might need to change the phrases to correspond
    # to what is currently in the news
    try:
        t1 = TitleTrigger("election")
        t2 = DescriptionTrigger("Trump")
        t3 = DescriptionTrigger("Clinton")
        t4 = AndTrigger(t2, t3)
        triggerlist = [t1, t4]

        # Problem 11
        # TODO: After implementing read_trigger_config, uncomment this line 
        triggerlist = read_trigger_config('triggers.txt')
        
        # HELPER CODE - you don't need to understand this!
        # Draws the popup window that displays the filtered stories
        # Retrieves and filters the stories from the RSS feeds
        frame = Frame(master)
        frame.pack(side=BOTTOM)
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT,fill=Y)

        t = "Google & Yahoo Top News"
        title = StringVar()
        title.set(t)
        ttl = Label(master, textvariable=title, font=("Helvetica", 18))
        ttl.pack(side=TOP)
        cont = Text(master, font=("Helvetica",14), yscrollcommand=scrollbar.set)
        cont.pack(side=BOTTOM)
        cont.tag_config("title", justify='center')
        button = Button(frame, text="Exit", command=root.destroy)
        button.pack(side=BOTTOM)
        guidShown = []
        def get_cont(newstory):
            if newstory.get_guid() not in guidShown:
                cont.insert(END, newstory.get_title()+"\n", "title")
                cont.insert(END, "\n---------------------------------------------------------------\n", "title")
                cont.insert(END, newstory.get_description())
                cont.insert(END, "\n*********************************************************************\n", "title")
                guidShown.append(newstory.get_guid())

        while True:

            print("Polling . . .", end=' ')
            # Get stories from Google's Top Stories RSS news feed
            stories = process("http://news.google.com/news?output=rss")

            # Get stories from Yahoo's Top Stories RSS news feed
            stories.extend(process("http://news.yahoo.com/rss/topstories"))

            stories = filter_stories(stories, triggerlist)

            list(map(get_cont, stories))
            scrollbar.config(command=cont.yview)


            print("Sleeping...")
            time.sleep(SLEEPTIME)

    except Exception as e:
        print(e)


# if __name__ == '__main__':
#     root = Tk()
#     root.title("Some RSS parser")
#     t = threading.Thread(target=main_thread, args=(root,))
#     t.start()
#     root.mainloop()

