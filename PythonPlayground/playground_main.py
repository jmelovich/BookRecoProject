# at the moment this script is just giving an example usage of tkinter for creating a window and simple UI
# i also demonstrate how to import a function from another file, which is useful for organizational purposes
# for example, we can create seperate py files for each type of approach or complicated operation and then run them from here

# in this case, I import the add_numbers function from the functions.py file, which defines that method from a C function 
# defined in functions/add_numbers.cpp

import tkinter as tk
from ttkwidgets.autocomplete import AutocompleteEntry
from playground_functions import add_numbers

def button_click():
    label_greybox = tk.Label(root,  background="#909090", width=50, height=50)
    label_results = tk.Label(root, background="#909090", font="Poppins")
    label_greybox.place(x=700, y=500)
    if genre_entry.get() == "":
        genre_results = "N/A"
    else:
        genre_results = genre_entry.get()
    if entry_minprice.get() == "":
        minprice_results = "N/A"
    else:
        minprice_results = entry_minprice.get()
    if entry_maxprice.get() == "":
        maxprice_results = "N/A"
    else:
        maxprice_results = entry_maxprice.get()
    label_results.config(text=f"Genre: {genre_results}\n"
                              f"Min Price: {minprice_results}\n"
                              f"Max Price: {maxprice_results}")
    label_results.place(x=700, y=500)

# Create the main window
root = tk.Tk()
root.title("Amazon Popular Books Filter Program")
root.geometry("1000x800")
root['background'] = '#909090'


# Create Genre Search Bar
Genres = ["1800s", "1900s", "20th Century", "Action & Adventure","Activities, Crafts & Games", "Actors & Entertainers",
"Administration & Medicine Economics", "Adventure", "Afghan & Iraq Wars", "Afghan War", "African American Studies",
"African Descent & Black", "Aging", "Alternative Medicine", "Amateur Sleuths", "American Civil War",
"American Revolution", "Americas", "Analysis & Strategy", "Ancient", "Animals", "Anthologies", "Antiques & Collectibles",
"Applied", "Applied Psychology", "Art, Music & Photography", "Arts & Literature", "Arts & Photography",
"Arts, Music & Photography", "Asia", "Astronomy & Space Science", "Atlases & Maps", "Authors", "Authorship",
"Baking", "Beginner Readers", "Behavioral Sciences", "Bible", "Bible Study & Reference", "Bibles", "Biographical",
"Biographies", "Biographies & Memoirs", "Biological Sciences", "Black & African American", "Black & African Americans",
"Books", "Boys & Men", "British & Irish", "Broadway & Musicals", "Buddhism", "Budgeting & Money Management",
"Business", "Business & Money", "Business Culture", "Calendars", "Canada", "Canadian", "Canning & Preserving",
"Chapter Books & Readers", "Chemistry", "Children's Books", "Christian", "Christian Books & Bibles", "Christian Living",
"Christianity", "Churches & Church Leadership", "City Life", "Civil Rights & Liberties", "Civilization & Culture",
"Classics", "Cleaning, Caretaking & Relocating", "Cognitive Psychology", "Comics & Graphic Novels", "Coming of Age",
"Community & Culture", "Computers & Technology", "Conservatism & Liberalism", "Contemporary", "Conventional",
"Cookbooks, Food & Wine", "Cooking Education & Reference", "Cooking Methods", "Cooking by Ingredient",
"Corporate Finance", "Cozy", "Crafts & Hobbies", "Crafts, Hobbies & Home", "Creativity", "Crime",
"Crime & Criminal Biographies", "Cultural Heritage", "Dark Fantasy", "Dating & Sex", "Death & Dying", "Death & Grief",
"Decision-Making & Problem Solving", "Democracy", "Detoxes & Cleanses", "Diets & Weight Loss", "Direction & Production",
"Discrimination & Racism", "Diseases", "Diseases & Physical Ailments", "Diseases & Physical Illness", "Divination",
"Dogs", "Domestic", "Dramas & Plays", "Drawing", "Dystopian", "Early Learning", "Econometrics & Statistics", "Economics",
"Education & Reference", "Education & Teaching", "Education & Training","Electronic Learning Toys",
"Encyclopedias & Subject Guides", "Endocrinology & Metabolism", "Engineering", "Engineering & Transportation", "Epic",
"Erotica", "Espionage","Ethics & Morality", "Ethnic Studies", "Europe", "European", "Executive Branch",
"Exercise & Fitness", "Fairy Tales & Folklore", "Fairy Tales, Folk Tales & Myths", "Family", "Family Life",
"Family Relationships", "Family Saga", "Fantasy", "Fantasy & Magic", "Finance", "Fortune Telling", "France",
"Friendship", "Friendship, Social Skills & School Life", "General", "Genre Fiction", "Geography & Cultures", "Ghosts",
"Gothic", "Graphic Design", "Graphic Novels", "Great Britain","Greek & Roman", "Grief & Bereavement",
"Growing Up & Facts of Life", "Guides", "Happiness", "Hard Science Fiction", "Health", "Health Care Delivery",
"Health, Fitness & Dieting", "Historical", "Historical Fiction", "History", "History & Criticism", "History & Theory",
"Holidays", "Holidays & Celebrations", "Holocaust", "Home Improvement & Design", "Horror", "How-to & Home Improvements",
"Humor", "Humor & Entertainment", "Humor & Satire", "Humorous", "Ideologies & Doctrines", "Indigenous",
"Individual Sports", "Industries", "Intelligence & Espionage", "Internal Medicine", "International Mystery & Crime",
"Introduction", "Investing", "Iraq War", "Jewish", "Job Hunting & Careers", "Judicial Branch", "Kitchen Appliances",
"LGBTQ+", "LGBTQ+ Books", "Leaders & Notable People", "Leadership & Motivation", "Learning & Education", "Legal",
"Literary", "Literature & Fiction", "Longevity", "Love & Romance", "Main Courses & Side Dishes", "Management",
"Management & Leadership", "Manga", "Marriage & Divorce", "Mathematics", "Medical", "Medical Books", "Medicine",
"Medicine & Health Sciences", "Meditation", "Mental & Spiritual Healing", "Mental Health", "Metaphysical & Visionary",
"Military", "Motivation & Self-Improvement", "Motivational", "Movies", "Music", "Musical Genres", "Mystery",
"Mystery & Thriller", "Mystery, Thriller & Suspense", "Mythology", "Mythology & Folk Tales", "Myths & Legends",
"National", "Native American", "Negotiating", "Neurology", "Neuroscience", "New Adult & College",
"New Age & Spirituality", "New Thought", "New, Used & Rental Textbooks", "Nursing", "Occult", "Occult & Paranormal",
"Operating Systems", "Orphans & Foster Homes", "Other Diets", "Paranormal", "Paranormal & Urban",
"Parenting & Relationships","Parents", "Patents & Inventions", "Pathology", "Peer Pressure", "Performing Arts",
"Personal Finance", "Personal Transformation", "Personality", "Pets & Animal Care", "Philosophy", "Photography & Video",
"Poetry", "Police Procedurals", "Political", "Political Science", "Politics & Government", "Politics & Social Sciences",
"Popular", "Poverty", "Pregnancy & Childbirth", "Prejudice & Racism", "Presidents & Heads of State",
"Privacy & Surveillance", "Private Investigators", "Probability & Statistics", "Professionals & Academics", "Psoriasis",
"Psychological", "Psychological Thrillers", "Psychology", "Psychology & Counseling", "Public Health",
"Publishing & Books", "Puzzles & Games", "Quick & Easy", "Race Relations", "Reference", "Regional & Cultural",
"Regional & International", "Reincarnation", "Relationships", "Religion & Spirituality", "Religions", "Religious",
"Religious Fiction", "Rich & Famous", "Rituals & Practice", "Romance", "Romantic", "Romantic Comedy", "Satire",
"Schools & Teaching", "Science & Math", "Science Fiction", "Science Fiction & Fantasy", "Science, Nature & How It Works",
"Scotland", "Scottish", "Sea Stories", "Self-Help", "Serial Killers", "Short Stories & Anthologies", "Siblings",
"Sleep Disorders", "Small Town & Rural", "Social & Family Issues", "Social Issues", "Social Sciences",
"Social Scientists & Psychologists", "Social Skills", "Social Theory", "Sociology", "Space Opera", "Special Diet",
"Specific Topics", "Spies & Politics", "Sports", "Sports & Outdoors", "State & Local", "Statistics", "Stocks",
"Stories", "Strategy", "Supernatural", "Survival Stories", "Suspense", "TV, Movie, Video Game Adaptations",
"Teen & Young Adult", "Theater", "Thriller & Suspense", "Thrillers & Suspense", "Time Travel", "Toys & Games",
"Traditional Detectives", "Travel", "Trivia & Fun Facts", "True Crime", "U.S. Presidents", "United States", "Urban",
"Urban Life", "Values & Virtues", "Vampires", "Venture Capital", "Video", "Vigilante Justice", "Viral",
"Wealth Management", "Weapons & Warfare", "Weddings", "Weight Training", "Wicca", "Wicca, Witchcraft & Paganism",
"Witchcraft", "Women", "Women Sleuths", "Women's Fiction", "Women's Health", "Workplace Culture", "World",
"World Literature", "World War II", "Worship & Devotion", "Writing"]

genre_entry = AutocompleteEntry(completevalues= Genres, width=20)
genre_entry.place(x=100, y=105)

label = tk.Label(root, text="Genre: ", font="Poppins", background='#909090')
label.place(x=10, y=100)

#Create min price entry field
entry_minprice = tk.Entry(root, width=20)
entry_minprice.place(x=200, y=175)
label = tk.Label(root, text="Min Price Point: ", font="Poppins", background='#909090')
label.place(x=10, y=170)

#Create max price entry field
entry_maxprice = tk.Entry(root, width=20)
entry_maxprice.place(x=200, y=225)
label = tk.Label(root, text="Max Price Point: ", font="Poppins", background='#909090')
label.place(x=10, y=220)

# Create a button
button = tk.Button(root, text="Print Results", font="Poppins", command=button_click, width=10, height=3)
button.place(x=450, y=500)

# # Create input fields
# entry1 = tk.Entry(root)
# entry1.place(x=100, y=200)
#
# entry2 = tk.Entry(root)
# entry2.pack(pady=5)
#
# # Create a button
# button = tk.Button(root, text="Add Numbers", command=button_click)
# button.pack(pady=10)
#


# Start the GUI event loop
root.mainloop()