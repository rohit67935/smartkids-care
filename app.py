from flask import Flask, render_template, request, jsonify
from difflib import get_close_matches
import re
import os
app = Flask(__name__)

# ============================================
# QUIZ FEATURE — add this to your existing app.py
# ============================================

# Quiz questions data (aap yahan aur subjects/questions add kar sakte ho)
# ============================================
# COMPLETE QUIZ_DATA — Copy this entire block into app.py
# Replace your existing QUIZ_DATA dictionary with this one
# Contains: Junior subjects + Class 7+ Advanced subjects
# ============================================

QUIZ_DATA = {

    # ============ JUNIOR LEVEL ============

    "math": [
        {
            "question": "What is 5 + 3?",
            "options": ["6", "7", "8", "9"],
            "answer": "8",
            "solution": "5 + 3 = 8. Add both numbers together."
        },
        {
            "question": "What is 10 - 4?",
            "options": ["5", "6", "7", "8"],
            "answer": "6",
            "solution": "10 - 4 = 6. Subtract 4 from 10."
        },
        {
            "question": "What is 3 x 3?",
            "options": ["6", "9", "12", "3"],
            "answer": "9",
            "solution": "3 x 3 means 3 added 3 times: 3+3+3 = 9."
        },
        {
            "question": "What is 7 + 6?",
            "options": ["11", "12", "13", "14"],
            "answer": "13",
            "solution": "7 + 6 = 13. Add both numbers together."
        },
        {
            "question": "What is 9 - 5?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "solution": "9 - 5 = 4. Subtract 5 from 9."
        },
        {
            "question": "What is 4 x 5?",
            "options": ["16", "18", "20", "22"],
            "answer": "20",
            "solution": "4 x 5 means 4 added 5 times: 4+4+4+4+4 = 20."
        },
        {
            "question": "What is 12 / 3?",
            "options": ["3", "4", "5", "6"],
            "answer": "4",
            "solution": "12 divided by 3 means splitting 12 into 3 equal groups: each group has 4."
        },
        {
            "question": "How many sides does a triangle have?",
            "options": ["2", "3", "4", "5"],
            "answer": "3",
            "solution": "A triangle always has exactly 3 sides and 3 corners."
        },
    ],

    "english": [
        {
            "question": "Which word is a noun?",
            "options": ["Run", "Happy", "Dog", "Quickly"],
            "answer": "Dog",
            "solution": "A noun is the name of a person, place, animal, or thing. 'Dog' is an animal, so it's a noun."
        },
        {
            "question": "What is the past tense of 'go'?",
            "options": ["Goed", "Went", "Gone", "Going"],
            "answer": "Went",
            "solution": "'Go' is an irregular verb. Its past tense is 'went', not 'goed'."
        },
        {
            "question": "Which word is an adjective?",
            "options": ["Run", "Beautiful", "Table", "Quickly"],
            "answer": "Beautiful",
            "solution": "An adjective describes a noun. 'Beautiful' describes how something looks."
        },
        {
            "question": "What is the plural of 'cat'?",
            "options": ["Cates", "Cat", "Cats", "Caties"],
            "answer": "Cats",
            "solution": "To make most nouns plural, just add 's'. Cat becomes Cats."
        },
        {
            "question": "Which word means the opposite of 'big'?",
            "options": ["Large", "Huge", "Small", "Tall"],
            "answer": "Small",
            "solution": "'Small' is the opposite (antonym) of 'big'. Large and Huge both mean big."
        },
        {
            "question": "How many vowels are there in the English alphabet?",
            "options": ["3", "4", "5", "6"],
            "answer": "5",
            "solution": "The English vowels are: a, e, i, o, u — that's 5 vowels."
        },
    ],

    "health": [
        {
            "question": "How many hours of sleep should kids get daily?",
            "options": ["2-3 hours", "4-5 hours", "7-8 hours", "10+ hours"],
            "answer": "7-8 hours",
            "solution": "Kids need 7-8 hours of sleep daily to help their body and brain rest and grow properly."
        },
        {
            "question": "Which of these is a healthy food?",
            "options": ["Candy", "Fruit", "Chips", "Soda"],
            "answer": "Fruit",
            "solution": "Fruit is rich in vitamins and natural sugars, making it a healthy food choice."
        },
        {
            "question": "How many times a day should you brush your teeth?",
            "options": ["Once", "Twice", "Three times", "Never"],
            "answer": "Twice",
            "solution": "Dentists recommend brushing teeth twice a day — morning and night — to keep them clean and healthy."
        },
        {
            "question": "What should you do before eating food?",
            "options": ["Watch TV", "Wash your hands", "Sleep", "Run"],
            "answer": "Wash your hands",
            "solution": "Washing hands before eating removes germs and keeps you from getting sick."
        },
        {
            "question": "Which activity keeps your body fit?",
            "options": ["Watching TV all day", "Exercise", "Eating junk food", "Skipping meals"],
            "answer": "Exercise",
            "solution": "Regular exercise keeps your muscles, heart, and body strong and healthy."
        },
    ],

    "history": [
        {
            "question": "Who was the first Prime Minister of Pakistan?",
            "options": ["Liaquat Ali Khan", "Jinnah", "Ayub Khan", "Iskander Mirza"],
            "answer": "Liaquat Ali Khan",
            "solution": "Liaquat Ali Khan became Pakistan's first Prime Minister after independence in 1947."
        },
        {
            "question": "In which year did Pakistan get independence?",
            "options": ["1945", "1946", "1947", "1948"],
            "answer": "1947",
            "solution": "Pakistan became an independent country on August 14, 1947."
        },
        {
            "question": "Who is known as the founder of Pakistan?",
            "options": ["Allama Iqbal", "Quaid-e-Azam", "Liaquat Ali Khan", "Fatima Jinnah"],
            "answer": "Quaid-e-Azam",
            "solution": "Muhammad Ali Jinnah, known as Quaid-e-Azam, is recognized as the founder of Pakistan."
        },
        {
            "question": "Which ancient civilization was found in the Indus Valley?",
            "options": ["Egyptian", "Indus Valley Civilization", "Roman", "Greek"],
            "answer": "Indus Valley Civilization",
            "solution": "The Indus Valley Civilization was one of the world's earliest urban civilizations, found in present-day Pakistan and India."
        },
        {
            "question": "Which monument is known as a wonder of the world?",
            "options": ["Eiffel Tower", "Great Wall of China", "Taj Mahal", "All of these"],
            "answer": "All of these",
            "solution": "All these monuments are famous wonders recognized worldwide for their architecture and history."
        },
    ],

    # ============ ADVANCED LEVEL (Class 7+) ============
    
    "math> 4th class": [
    {
        "question": "What is 6 + 7?",
        "options": ["12", "13", "14", "15"],
        "answer": "13",
        "solution": "6 + 7 = 13. Add both numbers together."
    },
    {
        "question": "What is 15 - 8?",
        "options": ["5", "6", "7", "8"],
        "answer": "7",
        "solution": "15 - 8 = 7. Subtract 8 from 15."
    },
    {
        "question": "What is 6 x 4?",
        "options": ["20", "22", "24", "26"],
        "answer": "24",
        "solution": "6 x 4 means 6 added 4 times: 6+6+6+6 = 24."
    },
    {
        "question": "What is 20 / 5?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "solution": "20 divided by 5 means splitting 20 into 5 equal groups: each group has 4."
    },
    {
        "question": "How many minutes are there in 1 hour?",
        "options": ["30", "45", "60", "90"],
        "answer": "60",
        "solution": "1 hour always equals 60 minutes."
    },
    {
        "question": "What is the next number in the pattern: 2, 4, 6, 8, ___?",
        "options": ["9", "10", "12", "14"],
        "answer": "10",
        "solution": "This is a pattern of even numbers increasing by 2 each time: 8 + 2 = 10."
    },
    {
        "question": "What is 100 - 45?",
        "options": ["45", "55", "65", "75"],
        "answer": "55",
        "solution": "100 - 45 = 55."
    },
    {
        "question": "How many days are there in a week?",
        "options": ["5", "6", "7", "8"],
        "answer": "7",
        "solution": "A week always has 7 days: Sunday to Saturday."
    },
    {
        "question": "What is 8 x 8?",
        "options": ["56", "60", "64", "72"],
        "answer": "64",
        "solution": "8 x 8 = 64. This is a common multiplication fact."
    },
    {
        "question": "What is half of 50?",
        "options": ["20", "25", "30", "35"],
        "answer": "25",
        "solution": "Half of a number means dividing it by 2: 50 / 2 = 25."
    },
    {
        "question": "How many sides does a rectangle have?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "solution": "A rectangle always has 4 sides."
    },
    {
        "question": "What is 9 + 9?",
        "options": ["16", "17", "18", "19"],
        "answer": "18",
        "solution": "9 + 9 = 18. Add both numbers together."
    },
    {
        "question": "What is 3/6 simplified?",
        "options": ["1/2", "1/3", "2/3", "3/4"],
        "answer": "1/2",
        "solution": "Divide numerator and denominator by 3: 3/6 = 1/2."
    },
    {
        "question": "What number comes before 100?",
        "options": ["98", "99", "101", "97"],
        "answer": "99",
        "solution": "Counting backwards from 100, the previous number is 99."
    },
    {
        "question": "What is 7 x 6?",
        "options": ["36", "40", "42", "48"],
        "answer": "42",
        "solution": "7 x 6 means 7 added 6 times: 7+7+7+7+7+7 = 42."
    },
    {
        "question": "How many centimeters are there in 1 meter?",
        "options": ["10", "100", "1000", "10000"],
        "answer": "100",
        "solution": "1 meter equals 100 centimeters."
    },
    {
        "question": "What is 45 / 9?",
        "options": ["4", "5", "6", "7"],
        "answer": "5",
        "solution": "45 divided by 9 equals 5, because 9 x 5 = 45."
    },
    {
        "question": "What shape has 3 sides?",
        "options": ["Square", "Triangle", "Circle", "Rectangle"],
        "answer": "Triangle",
        "solution": "A triangle is a shape with exactly 3 sides and 3 angles."
    },
    {
        "question": "What is 25 + 35?",
        "options": ["50", "55", "60", "65"],
        "answer": "60",
        "solution": "25 + 35 = 60. Add both numbers together."
    },
    {
        "question": "What is the value of 5 tens and 3 ones?",
        "options": ["35", "53", "58", "85"],
        "answer": "53",
        "solution": "5 tens = 50, plus 3 ones = 3. So 50 + 3 = 53."
    },
    {
        "question": "What is 12 x 3?",
        "options": ["24", "30", "36", "42"],
        "answer": "36",
        "solution": "12 x 3 means 12 added 3 times: 12+12+12 = 36."
    },
    {
        "question": "How many months are there in a year?",
        "options": ["10", "11", "12", "13"],
        "answer": "12",
        "solution": "A year always has 12 months, from January to December."
    },
    {
        "question": "What is 90 - 30?",
        "options": ["50", "55", "60", "65"],
        "answer": "60",
        "solution": "90 - 30 = 60."
    },
    {
        "question": "What is double of 15?",
        "options": ["25", "28", "30", "35"],
        "answer": "30",
        "solution": "Double means multiplying by 2: 15 x 2 = 30."
    },
    {
        "question": "How many sides does a hexagon have?",
        "options": ["5", "6", "7", "8"],
        "answer": "6",
        "solution": "A hexagon always has 6 sides."
    },
    {
        "question": "What is 5 x 9?",
        "options": ["40", "42", "45", "48"],
        "answer": "45",
        "solution": "5 x 9 means 5 added 9 times, which equals 45."
    },
    {
        "question": "What is 1/4 of 20?",
        "options": ["4", "5", "6", "10"],
        "answer": "5",
        "solution": "1/4 of a number means dividing it by 4: 20 / 4 = 5."
    },
    {
        "question": "What is the smallest even number greater than 10?",
        "options": ["11", "12", "13", "14"],
        "answer": "12",
        "solution": "Even numbers after 10 are 12, 14, 16... The smallest one is 12."
    },
    {
        "question": "What is 60 + 25?",
        "options": ["75", "80", "85", "90"],
        "answer": "85",
        "solution": "60 + 25 = 85. Add both numbers together."
    },
    {
        "question": "How many hours are there in a day?",
        "options": ["12", "20", "24", "30"],
        "answer": "24",
        "solution": "A day always has 24 hours."
    },
    {
        "question": "What is 11 x 11?",
        "options": ["111", "121", "131", "141"],
        "answer": "121",
        "solution": "11 x 11 = 121. This is a common multiplication fact."
    },
    {
        "question": "What is 3/4 written as a decimal?",
        "options": ["0.25", "0.5", "0.75", "1.0"],
        "answer": "0.75",
        "solution": "3 divided by 4 equals 0.75."
    },
    {
        "question": "What number is 10 more than 45?",
        "options": ["50", "53", "55", "60"],
        "answer": "55",
        "solution": "45 + 10 = 55."
    },
    {
        "question": "What is 100 / 4?",
        "options": ["20", "25", "30", "35"],
        "answer": "25",
        "solution": "100 divided by 4 equals 25, because 4 x 25 = 100."
    },
    {
        "question": "How many corners does a cube have?",
        "options": ["6", "8", "10", "12"],
        "answer": "8",
        "solution": "A cube has 8 corners (vertices)."
    },
    {
        "question": "What is 30 - 12?",
        "options": ["16", "17", "18", "19"],
        "answer": "18",
        "solution": "30 - 12 = 18."
    },
    {
        "question": "What is the sum of 14 and 16?",
        "options": ["28", "29", "30", "31"],
        "answer": "30",
        "solution": "14 + 16 = 30. Add both numbers together."
    },
    {
        "question": "What comes next: 5, 10, 15, 20, ___?",
        "options": ["22", "24", "25", "30"],
        "answer": "25",
        "solution": "This pattern increases by 5 each time: 20 + 5 = 25."
    },
    {
        "question": "What is 9 x 7?",
        "options": ["56", "60", "63", "70"],
        "answer": "63",
        "solution": "9 x 7 = 63. This is a common multiplication fact."
    },
    {
        "question": "How many weeks are there in a month (approximately)?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "solution": "A month has approximately 4 weeks (28-31 days)."
    },
    {
        "question": "What is 500 - 250?",
        "options": ["200", "225", "250", "275"],
        "answer": "250",
        "solution": "500 - 250 = 250."
    },
    {
        "question": "What is the perimeter of a triangle with all sides 4 cm?",
        "options": ["8 cm", "10 cm", "12 cm", "16 cm"],
        "answer": "12 cm",
        "solution": "Perimeter = sum of all sides = 4 + 4 + 4 = 12 cm."
    },
    {
        "question": "What is 2/3 of 9?",
        "options": ["3", "6", "9", "12"],
        "answer": "6",
        "solution": "2/3 of 9 means (2/3) x 9 = 6."
    },
    {
        "question": "What is 70 + 30?",
        "options": ["90", "95", "100", "105"],
        "answer": "100",
        "solution": "70 + 30 = 100."
    },
    {
        "question": "How many sides does a pentagon have?",
        "options": ["4", "5", "6", "7"],
        "answer": "5",
        "solution": "A pentagon always has 5 sides."
    },

        {
            "question": "What is the value of 15% of 200?",
            "options": ["20", "25", "30", "35"],
            "answer": "30",
            "solution": "15% of 200 = (15/100) x 200 = 30."
        },
        {
            "question": "Solve: 7x = 42, what is x?",
            "options": ["5", "6", "7", "8"],
            "answer": "6",
            "solution": "Divide both sides by 7: x = 42/7 = 6."
        },
        {
            "question": "What is the square root of 144?",
            "options": ["10", "11", "12", "13"],
            "answer": "12",
            "solution": "12 x 12 = 144, so the square root of 144 is 12."
        },
        {
            "question": "What is the perimeter of a square with side 5 cm?",
            "options": ["15 cm", "20 cm", "25 cm", "30 cm"],
            "answer": "20 cm",
            "solution": "Perimeter of a square = 4 x side = 4 x 5 = 20 cm."
        },
        {
            "question": "What is 2 to the power of 5?",
            "options": ["16", "25", "32", "64"],
            "answer": "32",
            "solution": "2^5 = 2x2x2x2x2 = 32."
        },
        {
            "question": "What is the LCM of 4 and 6?",
            "options": ["10", "12", "18", "24"],
            "answer": "12",
            "solution": "Multiples of 4: 4,8,12... Multiples of 6: 6,12,18... The smallest common one is 12."
        },
        {
            "question": "Simplify: 3/4 + 1/4",
            "options": ["1/2", "3/4", "1", "5/4"],
            "answer": "1",
            "solution": "Same denominators, add numerators: 3/4 + 1/4 = 4/4 = 1."
        },
        {
            "question": "What is the area of a rectangle with length 8 cm and width 5 cm?",
            "options": ["13 cm²", "26 cm²", "40 cm²", "45 cm²"],
            "answer": "40 cm²",
            "solution": "Area of rectangle = length x width = 8 x 5 = 40 cm²."
        },
    ],

    "english> 4th class": [

    {
        "question": "Which word is a pronoun?",
        "options": ["Run", "He", "Table", "Blue"],
        "answer": "He",
        "solution": "A pronoun replaces a noun. 'He' is used instead of a person's name."
    },
    {
        "question": "What is the plural of 'box'?",
        "options": ["Boxs", "Boxes", "Boxies", "Box"],
        "answer": "Boxes",
        "solution": "Words ending in 'x' usually add 'es' to form the plural: box → boxes."
    },
    {
        "question": "Which word is a verb?",
        "options": ["Jump", "Happy", "Chair", "Slow"],
        "answer": "Jump",
        "solution": "A verb shows an action. 'Jump' is something you do."
    },
    {
        "question": "What is the opposite of 'hot'?",
        "options": ["Warm", "Cold", "Sunny", "Wet"],
        "answer": "Cold",
        "solution": "'Cold' is the antonym (opposite) of 'hot'."
    },
    {
        "question": "Choose the correct spelling.",
        "options": ["Recieve", "Receive", "Receeve", "Receve"],
        "answer": "Receive",
        "solution": "Remember the rule: 'i before e except after c' — 'Receive' is correct."
    },
    {
        "question": "Which sentence uses correct punctuation?",
        "options": ["What is your name", "What is your name?", "What is your name!", "what is your name?"],
        "answer": "What is your name?",
        "solution": "Questions must end with a question mark and start with a capital letter."
    },
    {
        "question": "What is the past tense of 'play'?",
        "options": ["Played", "Plays", "Playing", "Play"],
        "answer": "Played",
        "solution": "Regular verbs form the past tense by adding 'ed': play → played."
    },
    {
        "question": "Which word means the same as 'quick'?",
        "options": ["Slow", "Fast", "Lazy", "Late"],
        "answer": "Fast",
        "solution": "'Fast' is a synonym of 'quick' — both mean moving with speed."
    },
    {
        "question": "Identify the adjective: 'The tall boy ran.'",
        "options": ["The", "Tall", "Boy", "Ran"],
        "answer": "Tall",
        "solution": "'Tall' describes the boy, making it an adjective."
    },
    {
        "question": "Which is a proper noun?",
        "options": ["City", "London", "Boy", "River"],
        "answer": "London",
        "solution": "Proper nouns name specific places, people, or things and start with a capital letter. 'London' is a specific city."
    },
    {
        "question": "Which word is an adverb?",
        "options": ["Quickly", "Quick", "Quickness", "Quicken"],
        "answer": "Quickly",
        "solution": "Adverbs often end in '-ly' and describe how an action is done."
    },
    {
        "question": "What is the past tense of 'write'?",
        "options": ["Writed", "Wrote", "Written", "Writing"],
        "answer": "Wrote",
        "solution": "'Write' is irregular. Its simple past tense is 'wrote'."
    },
    {
        "question": "Choose the correctly capitalized sentence.",
        "options": ["my name is ali.", "My name is ali.", "My name is Ali.", "my Name is Ali."],
        "answer": "My name is Ali.",
        "solution": "Sentences start with a capital letter, and proper names like 'Ali' are always capitalized."
    },
    {
        "question": "What kind of word is 'and'?",
        "options": ["Noun", "Verb", "Conjunction", "Adjective"],
        "answer": "Conjunction",
        "solution": "'And' joins words or sentences together, making it a conjunction."
    },
    {
        "question": "Which word rhymes with 'cat'?",
        "options": ["Dog", "Hat", "Sun", "Big"],
        "answer": "Hat",
        "solution": "'Cat' and 'Hat' both end with the same '-at' sound, so they rhyme."
    },
    {
        "question": "What is the plural of 'mouse'?",
        "options": ["Mouses", "Mices", "Mice", "Mouse"],
        "answer": "Mice",
        "solution": "'Mouse' is irregular; its plural form is 'Mice'."
    },
    {
        "question": "Which sentence is a question?",
        "options": ["I like apples.", "Do you like apples?", "Apples are red.", "Eat the apple."],
        "answer": "Do you like apples?",
        "solution": "This sentence asks something and ends with a question mark, making it a question."
    },
    {
        "question": "What is the opposite of 'happy'?",
        "options": ["Joyful", "Sad", "Excited", "Glad"],
        "answer": "Sad",
        "solution": "'Sad' is the antonym of 'happy'."
    },
    {
        "question": "Which word is spelled correctly?",
        "options": ["Beautifull", "Beautiful", "Beutiful", "Beautifull"],
        "answer": "Beautiful",
        "solution": "The correct spelling has one 'l' at the end: Beautiful."
    },
    {
        "question": "What is the past tense of 'see'?",
        "options": ["Seed", "Seen", "Saw", "Sees"],
        "answer": "Saw",
        "solution": "'See' is irregular. Its simple past tense is 'saw' (e.g., 'I saw a bird')."
    },
    {
        "question": "Identify the subject: 'The cat sat on the mat.'",
        "options": ["Cat", "Sat", "Mat", "The"],
        "answer": "Cat",
        "solution": "The subject is who or what the sentence is about — here it's 'the cat'."
    },
    {
        "question": "Which word means 'very big'?",
        "options": ["Tiny", "Huge", "Small", "Short"],
        "answer": "Huge",
        "solution": "'Huge' means extremely large in size."
    },
    {
        "question": "What is the plural of 'leaf'?",
        "options": ["Leafs", "Leaves", "Leafes", "Leaf"],
        "answer": "Leaves",
        "solution": "Words ending in 'f' often change to 'ves' in plural form: leaf → leaves."
    },
    {
        "question": "Which is an exclamatory sentence?",
        "options": ["What time is it?", "Close the door.", "Wow, that's amazing!", "I am reading."],
        "answer": "Wow, that's amazing!",
        "solution": "Exclamatory sentences express strong emotion and end with an exclamation mark."
    },
    {
        "question": "What is the correct preposition: 'The cat is ___ the box.'",
        "options": ["in", "on", "at", "for"],
        "answer": "in",
        "solution": "'In' shows the cat is inside the box."
    },
    {
        "question": "Which word is a synonym for 'smart'?",
        "options": ["Dull", "Clever", "Slow", "Tired"],
        "answer": "Clever",
        "solution": "'Clever' has a similar meaning to 'smart' — both describe intelligence."
    },
    {
        "question": "What is the past tense of 'run'?",
        "options": ["Runned", "Ran", "Running", "Runs"],
        "answer": "Ran",
        "solution": "'Run' is irregular. Its simple past tense is 'ran'."
    },
    {
        "question": "Which sentence uses 'their' correctly?",
        "options": ["Their going home.", "They're going home.", "There going home.", "Their's going home."],
        "answer": "They're going home.",
        "solution": "'They're' is short for 'they are' and is correct here. 'Their' shows possession, not used correctly in this context."
    },
    {
        "question": "What is the opposite of 'open'?",
        "options": ["Close", "Wide", "Free", "New"],
        "answer": "Close",
        "solution": "'Close' means the opposite of 'open' — shutting something."
    },
    {
        "question": "Which word is a collective noun?",
        "options": ["Dog", "Herd", "Run", "Blue"],
        "answer": "Herd",
        "solution": "A collective noun names a group of things, like 'herd' for a group of animals."
    },
    {
        "question": "What is the plural of 'foot'?",
        "options": ["Foots", "Feets", "Feet", "Footes"],
        "answer": "Feet",
        "solution": "'Foot' is irregular; its plural form is 'Feet'."
    },
    {
        "question": "Which is a compound sentence?",
        "options": ["I like tea.", "I like tea and coffee.", "I like tea, but she likes coffee.", "Tea is hot."],
        "answer": "I like tea, but she likes coffee.",
        "solution": "A compound sentence joins two complete sentences using a conjunction like 'but'."
    },
    {
        "question": "What does the suffix '-less' mean in 'careless'?",
        "options": ["Full of", "Without", "Before", "After"],
        "answer": "Without",
        "solution": "The suffix '-less' means 'without'. 'Careless' means without care."
    },
    {
        "question": "Which word is an interjection?",
        "options": ["Run", "Wow!", "Blue", "Table"],
        "answer": "Wow!",
        "solution": "An interjection expresses sudden emotion, like 'Wow!'"
    },
    {
        "question": "What is the correct comparative form of 'big'?",
        "options": ["Biggest", "More big", "Bigger", "Bigly"],
        "answer": "Bigger",
        "solution": "For short adjectives, add '-er' to compare two things: big → bigger."
    },
    {
        "question": "Which word means the opposite of 'begin'?",
        "options": ["Start", "End", "Continue", "Open"],
        "answer": "End",
        "solution": "'End' is the antonym of 'begin' — one starts something, the other finishes it."
    },
    {
        "question": "What type of noun is 'happiness'?",
        "options": ["Common noun", "Proper noun", "Abstract noun", "Collective noun"],
        "answer": "Abstract noun",
        "solution": "Abstract nouns name feelings or ideas that can't be touched, like 'happiness'."
    },
    {
        "question": "Which sentence is in future tense?",
        "options": ["I eat rice.", "I ate rice.", "I will eat rice.", "I am eating rice."],
        "answer": "I will eat rice.",
        "solution": "'Will' shows an action that hasn't happened yet — future tense."
    },
    {
        "question": "What is the superlative form of 'good'?",
        "options": ["Gooder", "Best", "Better", "Goodest"],
        "answer": "Best",
        "solution": "'Good' is irregular. Its superlative form is 'best', not 'goodest'."
    },
    {
        "question": "Which word is spelled correctly?",
        "options": ["Definately", "Definitely", "Definitly", "Definetely"],
        "answer": "Definitely",
        "solution": "The correct spelling is 'Definitely' — a commonly misspelled word."
    },
    {
        "question": "What is the plural of 'city'?",
        "options": ["Citys", "Cities", "Cityes", "City"],
        "answer": "Cities",
        "solution": "Words ending in a consonant + 'y' change 'y' to 'ies': city → cities."
    },
    {
        "question": "Which word is a conjunction?",
        "options": ["Because", "Blue", "Jump", "Table"],
        "answer": "Because",
        "solution": "'Because' connects two clauses and gives a reason, making it a conjunction."
    },
    {
        "question": "What is the opposite of 'fast'?",
        "options": ["Quick", "Slow", "Speedy", "Rapid"],
        "answer": "Slow",
        "solution": "'Slow' is the antonym of 'fast' — moving with little speed."
    },
        {
            "question": "Choose the correct synonym for 'Happy'",
            "options": ["Sad", "Joyful", "Angry", "Tired"],
            "answer": "Joyful",
            "solution": "A synonym is a word with a similar meaning. 'Joyful' means the same as 'Happy'."
        },
        {
            "question": "Which sentence is grammatically correct?",
            "options": ["She go to school", "She goes to school", "She going to school", "She gone to school"],
            "answer": "She goes to school",
            "solution": "With 'She' (third person singular), the verb takes 's': 'goes', not 'go'."
        },
        {
            "question": "What is the antonym of 'Ancient'?",
            "options": ["Old", "Modern", "Historic", "Traditional"],
            "answer": "Modern",
            "solution": "An antonym is a word with the opposite meaning. 'Modern' is the opposite of 'Ancient'."
        },
        {
            "question": "Identify the verb in: 'The boy runs fast.'",
            "options": ["Boy", "Runs", "Fast", "The"],
            "answer": "Runs",
            "solution": "A verb shows action. 'Runs' is the action word in this sentence."
        },
        {
            "question": "Which of these is a compound word?",
            "options": ["Table", "Sunflower", "Happy", "Quick"],
            "answer": "Sunflower",
            "solution": "A compound word is made of two smaller words joined together: 'Sun' + 'flower' = 'Sunflower'."
        },
        {
            "question": "What type of sentence is: 'Please close the door.'",
            "options": ["Question", "Exclamation", "Imperative", "Statement"],
            "answer": "Imperative",
            "solution": "An imperative sentence gives a command or request, like 'Please close the door.'"
        },
        {
            "question": "Choose the correct preposition: 'The book is ___ the table.'",
            "options": ["in", "on", "at", "by"],
            "answer": "on",
            "solution": "'On' shows the book is resting on top of the table's surface."
        },
    ],

    "science> 4th class": [
    {
        "question": "What is the closest planet to the Sun?",
        "options": ["Venus", "Mercury", "Earth", "Mars"],
        "answer": "Mercury",
        "solution": "Mercury is the closest planet to the Sun in our solar system."
    },
    {
        "question": "What do plants need to make their own food?",
        "options": ["Water only", "Sunlight, water, and carbon dioxide", "Soil only", "Air only"],
        "answer": "Sunlight, water, and carbon dioxide",
        "solution": "Plants use sunlight, water, and carbon dioxide together in photosynthesis to make food."
    },
    {
        "question": "What is the largest organ in the human body?",
        "options": ["Heart", "Liver", "Skin", "Brain"],
        "answer": "Skin",
        "solution": "The skin covers the whole body and is the largest human organ."
    },
    {
        "question": "How many bones are there in an adult human body?",
        "options": ["186", "206", "226", "246"],
        "answer": "206",
        "solution": "An adult human body has 206 bones."
    },
    {
        "question": "What gas do humans breathe in to survive?",
        "options": ["Carbon Dioxide", "Nitrogen", "Oxygen", "Hydrogen"],
        "answer": "Oxygen",
        "solution": "Humans breathe in oxygen, which the body uses for energy production."
    },
    {
        "question": "What is the freezing point of water?",
        "options": ["0°C", "10°C", "32°C", "100°C"],
        "answer": "0°C",
        "solution": "Water freezes and turns to ice at 0°C."
    },
    {
        "question": "Which part of the plant absorbs water from the soil?",
        "options": ["Leaves", "Stem", "Roots", "Flowers"],
        "answer": "Roots",
        "solution": "Roots grow underground and absorb water and nutrients from the soil."
    },
    {
        "question": "What is the study of living things called?",
        "options": ["Physics", "Chemistry", "Biology", "Geology"],
        "answer": "Biology",
        "solution": "Biology is the science that studies living organisms."
    },
    {
        "question": "How many legs does a spider have?",
        "options": ["6", "8", "10", "12"],
        "answer": "8",
        "solution": "Spiders are arachnids and have 8 legs, unlike insects which have 6."
    },
    {
        "question": "What is the main source of energy for Earth?",
        "options": ["Moon", "Sun", "Wind", "Water"],
        "answer": "Sun",
        "solution": "The Sun provides light and heat energy that powers life on Earth."
    },
    {
        "question": "Which sense organ helps us to see?",
        "options": ["Ear", "Nose", "Eye", "Tongue"],
        "answer": "Eye",
        "solution": "The eyes are the sense organs responsible for vision."
    },
    {
        "question": "What state of matter is ice?",
        "options": ["Liquid", "Gas", "Solid", "Plasma"],
        "answer": "Solid",
        "solution": "Ice is water in its solid state, formed when water freezes."
    },
    {
        "question": "What do we call animals that eat only plants?",
        "options": ["Carnivores", "Herbivores", "Omnivores", "Predators"],
        "answer": "Herbivores",
        "solution": "Herbivores are animals that eat only plants, like cows and rabbits."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "options": ["Venus", "Jupiter", "Mars", "Saturn"],
        "answer": "Mars",
        "solution": "Mars appears red due to iron oxide (rust) on its surface, giving it the nickname 'Red Planet'."
    },
    {
        "question": "What do we call animals that eat both plants and meat?",
        "options": ["Herbivores", "Carnivores", "Omnivores", "Scavengers"],
        "answer": "Omnivores",
        "solution": "Omnivores eat both plants and meat, like humans and bears."
    },
    {
        "question": "Which organ helps us to breathe?",
        "options": ["Heart", "Lungs", "Liver", "Kidney"],
        "answer": "Lungs",
        "solution": "The lungs take in oxygen and remove carbon dioxide when we breathe."
    },
    {
        "question": "What is the process by which water turns into vapor called?",
        "options": ["Condensation", "Evaporation", "Freezing", "Melting"],
        "answer": "Evaporation",
        "solution": "Evaporation is when liquid water changes into water vapor due to heat."
    },
    {
        "question": "How many chambers does the human heart have?",
        "options": ["2", "3", "4", "5"],
        "answer": "4",
        "solution": "The human heart has 4 chambers: two atria and two ventricles."
    },
    {
        "question": "What is the hardest natural substance on Earth?",
        "options": ["Gold", "Iron", "Diamond", "Silver"],
        "answer": "Diamond",
        "solution": "Diamond is the hardest known natural material on Earth."
    },
    {
        "question": "Which gas do plants release during photosynthesis?",
        "options": ["Carbon Dioxide", "Oxygen", "Nitrogen", "Hydrogen"],
        "answer": "Oxygen",
        "solution": "During photosynthesis, plants take in carbon dioxide and release oxygen."
    },
    {
        "question": "What is the center of an atom called?",
        "options": ["Electron", "Proton", "Nucleus", "Neutron"],
        "answer": "Nucleus",
        "solution": "The nucleus is the central part of an atom, containing protons and neutrons."
    },
    {
        "question": "Which planet has rings around it?",
        "options": ["Earth", "Mars", "Saturn", "Mercury"],
        "answer": "Saturn",
        "solution": "Saturn is famous for its beautiful and prominent ring system made of ice and rock."
    },
    {
        "question": "What do we call baby frogs?",
        "options": ["Cubs", "Tadpoles", "Calves", "Kittens"],
        "answer": "Tadpoles",
        "solution": "Baby frogs are called tadpoles before they grow legs and become adult frogs."
    },
    {
        "question": "What is the natural satellite of Earth called?",
        "options": ["Sun", "Mars", "Moon", "Star"],
        "answer": "Moon",
        "solution": "The Moon is Earth's only natural satellite that orbits around it."
    },
    {
        "question": "Which blood cells help fight infections?",
        "options": ["Red blood cells", "White blood cells", "Platelets", "Plasma"],
        "answer": "White blood cells",
        "solution": "White blood cells are part of the immune system and help fight off infections."
    },
    {
        "question": "What causes day and night on Earth?",
        "options": ["Earth's revolution around the Sun", "Earth's rotation on its axis", "The Moon's orbit", "Clouds"],
        "answer": "Earth's rotation on its axis",
        "solution": "Earth spins on its axis once every 24 hours, causing day and night."
    },
    {
        "question": "What is the chemical formula for table salt?",
        "options": ["H2O", "NaCl", "CO2", "O2"],
        "answer": "NaCl",
        "solution": "Table salt is made of sodium (Na) and chlorine (Cl), forming NaCl."
    },
    {
        "question": "Which sense organ helps us to hear?",
        "options": ["Eye", "Ear", "Nose", "Skin"],
        "answer": "Ear",
        "solution": "The ears are responsible for detecting sound and helping us hear."
    },
    {
        "question": "What do we call animals without a backbone?",
        "options": ["Vertebrates", "Invertebrates", "Mammals", "Reptiles"],
        "answer": "Invertebrates",
        "solution": "Invertebrates are animals that do not have a backbone, like insects and worms."
    },
    {
        "question": "What is the process of a caterpillar turning into a butterfly called?",
        "options": ["Evolution", "Metamorphosis", "Reproduction", "Photosynthesis"],
        "answer": "Metamorphosis",
        "solution": "Metamorphosis is the process where an animal changes form completely, like caterpillar to butterfly."
    },
    {
        "question": "Which part of the body pumps blood?",
        "options": ["Lungs", "Brain", "Heart", "Stomach"],
        "answer": "Heart",
        "solution": "The heart is a muscular organ that pumps blood throughout the body."
    },
    {
        "question": "What is the main gas found in the air we breathe?",
        "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
        "answer": "Nitrogen",
        "solution": "Nitrogen makes up about 78% of the air, more than any other gas."
    },
    {
        "question": "What do we call the path a planet takes around the Sun?",
        "options": ["Rotation", "Orbit", "Axis", "Gravity"],
        "answer": "Orbit",
        "solution": "An orbit is the curved path a planet follows as it moves around the Sun."
    },
    {
        "question": "Which organ filters waste from the blood?",
        "options": ["Liver", "Kidney", "Lungs", "Heart"],
        "answer": "Kidney",
        "solution": "The kidneys filter waste products out of the blood and produce urine."
    },
    {
        "question": "What is the term for animals that are active at night?",
        "options": ["Diurnal", "Nocturnal", "Herbivore", "Carnivore"],
        "answer": "Nocturnal",
        "solution": "Nocturnal animals, like owls and bats, are active during the night and rest during the day."
    },
    {
        "question": "What is the smallest unit of life?",
        "options": ["Tissue", "Organ", "Cell", "Organism"],
        "answer": "Cell",
        "solution": "The cell is the basic building block and smallest unit of all living organisms."
    },
    {
        "question": "Which force keeps planets in orbit around the Sun?",
        "options": ["Magnetism", "Friction", "Gravity", "Electricity"],
        "answer": "Gravity",
        "solution": "Gravity is the force that pulls planets toward the Sun, keeping them in orbit."
    },
    {
        "question": "What is the process of water vapor turning back into liquid called?",
        "options": ["Evaporation", "Condensation", "Precipitation", "Sublimation"],
        "answer": "Condensation",
        "solution": "Condensation happens when water vapor cools and turns back into liquid water."
    },
    {
        "question": "Which vitamin do we get from sunlight?",
        "options": ["Vitamin A", "Vitamin B", "Vitamin C", "Vitamin D"],
        "answer": "Vitamin D",
        "solution": "Our skin produces Vitamin D when exposed to sunlight, which helps bones grow strong."
    },
    {
        "question": "What is the outer layer of the Earth called?",
        "options": ["Core", "Mantle", "Crust", "Atmosphere"],
        "answer": "Crust",
        "solution": "The crust is the thin outer layer of the Earth where we live."
    },
    {
        "question": "Which animal is known as the 'King of the Jungle'?",
        "options": ["Tiger", "Elephant", "Lion", "Bear"],
        "answer": "Lion",
        "solution": "The lion is commonly called the 'King of the Jungle' due to its strength and status as a top predator."
    },
    {
        "question": "What do bees collect from flowers?",
        "options": ["Water", "Nectar", "Leaves", "Seeds"],
        "answer": "Nectar",
        "solution": "Bees collect nectar from flowers, which they use to make honey."
    },
    {
        "question": "Which planet is the largest in our solar system?",
        "options": ["Earth", "Saturn", "Jupiter", "Neptune"],
        "answer": "Jupiter",
        "solution": "Jupiter is the largest planet in our solar system."
    },
    {
        "question": "What is the main function of the roots in a plant?",
        "options": ["Making food", "Absorbing water and nutrients", "Producing flowers", "Releasing oxygen"],
        "answer": "Absorbing water and nutrients",
        "solution": "Roots anchor the plant and absorb water and nutrients from the soil."
    },
    {
        "question": "What do we call a scientist who studies stars and planets?",
        "options": ["Biologist", "Chemist", "Astronomer", "Geologist"],
        "answer": "Astronomer",
        "solution": "An astronomer studies stars, planets, and other objects in space."
    },
        {
            "question": "What is the powerhouse of the cell?",
            "options": ["Nucleus", "Mitochondria", "Ribosome", "Cytoplasm"],
            "answer": "Mitochondria",
            "solution": "Mitochondria produce energy for the cell, which is why it's called the 'powerhouse of the cell'."
        },
        {
            "question": "What gas do plants absorb from the air for photosynthesis?",
            "options": ["Oxygen", "Nitrogen", "Carbon Dioxide", "Hydrogen"],
            "answer": "Carbon Dioxide",
            "solution": "Plants absorb carbon dioxide (CO2) and use sunlight to make food through photosynthesis."
        },
        {
            "question": "What is the chemical symbol for water?",
            "options": ["H2O", "O2", "CO2", "H2"],
            "answer": "H2O",
            "solution": "Water is made of 2 hydrogen atoms and 1 oxygen atom, written as H2O."
        },
        {
            "question": "How many planets are there in our solar system?",
            "options": ["7", "8", "9", "10"],
            "answer": "8",
            "solution": "There are 8 planets in our solar system since Pluto was reclassified as a dwarf planet."
        },
        {
            "question": "What force pulls objects toward the Earth?",
            "options": ["Magnetism", "Gravity", "Friction", "Tension"],
            "answer": "Gravity",
            "solution": "Gravity is the force that pulls objects toward the Earth's center."
        },
        {
            "question": "Which organ pumps blood in the human body?",
            "options": ["Lungs", "Liver", "Heart", "Kidney"],
            "answer": "Heart",
            "solution": "The heart pumps blood throughout the body, delivering oxygen and nutrients."
        },
        {
            "question": "What is the boiling point of water at sea level?",
            "options": ["90°C", "100°C", "110°C", "120°C"],
            "answer": "100°C",
            "solution": "Water boils at 100°C (212°F) at sea level under normal atmospheric pressure."
        },
    ],

    "history> 4th class": [
    {
        "question": "Who was the first Prime Minister of Pakistan?",
        "options": ["Liaquat Ali Khan", "Jinnah", "Ayub Khan", "Iskander Mirza"],
        "answer": "Liaquat Ali Khan",
        "solution": "Liaquat Ali Khan became Pakistan's first Prime Minister after independence in 1947."
    },
    {
        "question": "In which year did Pakistan get independence?",
        "options": ["1945", "1946", "1947", "1948"],
        "answer": "1947",
        "solution": "Pakistan became an independent country on August 14, 1947."
    },
    {
        "question": "Who is known as the founder of Pakistan?",
        "options": ["Allama Iqbal", "Quaid-e-Azam", "Liaquat Ali Khan", "Fatima Jinnah"],
        "answer": "Quaid-e-Azam",
        "solution": "Muhammad Ali Jinnah, known as Quaid-e-Azam, is recognized as the founder of Pakistan."
    },
    {
        "question": "Which ancient civilization was found in the Indus Valley?",
        "options": ["Egyptian", "Indus Valley Civilization", "Roman", "Greek"],
        "answer": "Indus Valley Civilization",
        "solution": "The Indus Valley Civilization was one of the world's earliest urban civilizations, found in present-day Pakistan and India."
    },
    {
        "question": "Which monument is known as a wonder of the world?",
        "options": ["Eiffel Tower", "Great Wall of China", "Taj Mahal", "All of these"],
        "answer": "All of these",
        "solution": "All these monuments are famous wonders recognized worldwide for their architecture and history."
    },
    {
        "question": "Which poet is known as the national poet of Pakistan?",
        "options": ["Allama Iqbal", "Faiz Ahmed Faiz", "Mirza Ghalib", "Ahmed Faraz"],
        "answer": "Allama Iqbal",
        "solution": "Allama Iqbal is called the national poet of Pakistan and inspired the idea of a separate Muslim state."
    },
    {
        "question": "Which city was the ancient capital of the Indus Valley Civilization?",
        "options": ["Lahore", "Mohenjo-daro", "Karachi", "Multan"],
        "answer": "Mohenjo-daro",
        "solution": "Mohenjo-daro was one of the largest and most well-preserved cities of the Indus Valley Civilization."
    },
    {
        "question": "In which year was the Lahore Resolution presented?",
        "options": ["1938", "1939", "1940", "1941"],
        "answer": "1940",
        "solution": "The Lahore Resolution, calling for a separate Muslim state, was presented in 1940."
    },
    {
        "question": "Who was the first President of Pakistan?",
        "options": ["Iskander Mirza", "Ayub Khan", "Yahya Khan", "Zulfikar Ali Bhutto"],
        "answer": "Iskander Mirza",
        "solution": "Iskander Mirza became the first President of Pakistan in 1956."
    },
    {
        "question": "Which ancient wonder was located in Egypt?",
        "options": ["Colosseum", "Great Pyramid of Giza", "Parthenon", "Stonehenge"],
        "answer": "Great Pyramid of Giza",
        "solution": "The Great Pyramid of Giza in Egypt is one of the Seven Wonders of the Ancient World."
    },
    {
        "question": "Who discovered America?",
        "options": ["Vasco da Gama", "Christopher Columbus", "Marco Polo", "Ferdinand Magellan"],
        "answer": "Christopher Columbus",
        "solution": "Christopher Columbus is credited with reaching the Americas in 1492."
    },
    {
        "question": "Which empire ruled over the Indian subcontinent before the British?",
        "options": ["Roman Empire", "Mughal Empire", "Ottoman Empire", "Persian Empire"],
        "answer": "Mughal Empire",
        "solution": "The Mughal Empire ruled large parts of the Indian subcontinent before British colonization."
    },
    {
        "question": "Who built the Taj Mahal?",
        "options": ["Akbar", "Shah Jahan", "Aurangzeb", "Babur"],
        "answer": "Shah Jahan",
        "solution": "Mughal Emperor Shah Jahan built the Taj Mahal in memory of his wife Mumtaz Mahal."
    },
    {
        "question": "Which country gifted the Statue of Liberty to the USA?",
        "options": ["Britain", "France", "Spain", "Germany"],
        "answer": "France",
        "solution": "France gifted the Statue of Liberty to the United States in 1886 as a symbol of friendship."
    },
    {
        "question": "Who was the founder of the Mughal Empire?",
        "options": ["Akbar", "Babur", "Humayun", "Shah Jahan"],
        "answer": "Babur",
        "solution": "Babur founded the Mughal Empire in 1526 after defeating the last Sultan of Delhi."
    },
    {
        "question": "Which ancient civilization built the pyramids?",
        "options": ["Romans", "Greeks", "Egyptians", "Persians"],
        "answer": "Egyptians",
        "solution": "The ancient Egyptians built the famous pyramids as tombs for their pharaohs."
    },
    {
        "question": "In which year did India and Pakistan gain independence from British rule?",
        "options": ["1945", "1946", "1947", "1950"],
        "answer": "1947",
        "solution": "Both India and Pakistan became independent from British rule in 1947."
    },
    {
        "question": "Which sea route did Vasco da Gama discover?",
        "options": ["Route to America", "Route to India", "Route to China", "Route to Australia"],
        "answer": "Route to India",
        "solution": "Vasco da Gama discovered the sea route from Europe to India in 1498."
    },
    {
        "question": "What was the ancient city of Rome the capital of?",
        "options": ["Greek Empire", "Roman Empire", "Persian Empire", "Ottoman Empire"],
        "answer": "Roman Empire",
        "solution": "Rome was the capital of the powerful Roman Empire."
    },
    {
        "question": "Who was the last Mughal Emperor of India?",
        "options": ["Akbar", "Bahadur Shah Zafar", "Shah Jahan", "Aurangzeb"],
        "answer": "Bahadur Shah Zafar",
        "solution": "Bahadur Shah Zafar was the last Mughal Emperor before the British took full control of India."
    },
    {
        "question": "Which country was ruled by the Pharaohs?",
        "options": ["Greece", "Rome", "Egypt", "Persia"],
        "answer": "Egypt",
        "solution": "Ancient Egypt was ruled by kings known as Pharaohs."
    },
    {
        "question": "Which war is known as the deadliest conflict in human history?",
        "options": ["World War I", "World War II", "Cold War", "Vietnam War"],
        "answer": "World War II",
        "solution": "World War II (1939-1945) is considered the deadliest and largest conflict in human history."
    },
    {
        "question": "Which explorer sailed around the world for the first time?",
        "options": ["Christopher Columbus", "Ferdinand Magellan", "Vasco da Gama", "Marco Polo"],
        "answer": "Ferdinand Magellan",
        "solution": "Ferdinand Magellan's expedition was the first to sail around (circumnavigate) the world."
    },
    {
        "question": "Which ancient Greek structure is dedicated to the goddess Athena?",
        "options": ["Colosseum", "Parthenon", "Pyramids", "Great Wall"],
        "answer": "Parthenon",
        "solution": "The Parthenon in Athens, Greece, was built as a temple dedicated to the goddess Athena."
    },
    {
        "question": "Who is known as the 'Iron Lady' and was the first female Prime Minister of Britain?",
        "options": ["Queen Elizabeth", "Margaret Thatcher", "Theresa May", "Angela Merkel"],
        "answer": "Margaret Thatcher",
        "solution": "Margaret Thatcher, nicknamed the 'Iron Lady', served as Britain's first female Prime Minister."
    },
    {
        "question": "Which river was important to the Indus Valley Civilization?",
        "options": ["Nile", "Indus", "Amazon", "Ganges"],
        "answer": "Indus",
        "solution": "The Indus River was central to the development of the Indus Valley Civilization."
    },
    {
        "question": "Who is Fatima Jinnah known as in Pakistan's history?",
        "options": ["Mother of Pakistan", "Madar-e-Millat", "Founder of Pakistan", "Iron Lady"],
        "answer": "Madar-e-Millat",
        "solution": "Fatima Jinnah is honored as 'Madar-e-Millat' (Mother of the Nation) for her role in Pakistan's independence movement."
    },
    {
        "question": "Which ancient wonder is located in China?",
        "options": ["Great Wall of China", "Colosseum", "Pyramids", "Stonehenge"],
        "answer": "Great Wall of China",
        "solution": "The Great Wall of China was built to protect Chinese states from invasions."
    },
    {
        "question": "Who was the first man to walk on the Moon?",
        "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "John Glenn"],
        "answer": "Neil Armstrong",
        "solution": "Neil Armstrong became the first man to walk on the Moon on July 20, 1969."
    },
    {
        "question": "Which country was formerly known as Persia?",
        "options": ["Iraq", "Iran", "Turkey", "Syria"],
        "answer": "Iran",
        "solution": "Iran was historically known as Persia until it officially changed its name in 1935."
    },
    {
        "question": "Which ancient civilization used hieroglyphics as writing?",
        "options": ["Romans", "Greeks", "Egyptians", "Mesopotamians"],
        "answer": "Egyptians",
        "solution": "Ancient Egyptians used hieroglyphics, a system of picture-based writing."
    },
    {
        "question": "Who invented the telephone?",
        "options": ["Thomas Edison", "Alexander Graham Bell", "Nikola Tesla", "Isaac Newton"],
        "answer": "Alexander Graham Bell",
        "solution": "Alexander Graham Bell is credited with inventing the first practical telephone in 1876."
    },
    {
        "question": "Which empire was ruled by Alexander the Great?",
        "options": ["Roman Empire", "Macedonian Empire", "Persian Empire", "Ottoman Empire"],
        "answer": "Macedonian Empire",
        "solution": "Alexander the Great expanded the Macedonian Empire across much of the known world."
    },
    {
        "question": "In which year was the United Nations founded?",
        "options": ["1943", "1945", "1947", "1950"],
        "answer": "1945",
        "solution": "The United Nations was founded in 1945 after World War II to promote peace among nations."
    },
    {
        "question": "Who was the leader of India's independence movement known for non-violence?",
        "options": ["Jawaharlal Nehru", "Mahatma Gandhi", "Subhas Chandra Bose", "Sardar Patel"],
        "answer": "Mahatma Gandhi",
        "solution": "Mahatma Gandhi led India's independence movement using non-violent methods."
    },
    {
        "question": "Which ancient city is famous for its hanging gardens?",
        "options": ["Rome", "Babylon", "Athens", "Cairo"],
        "answer": "Babylon",
        "solution": "The Hanging Gardens of Babylon were considered one of the Seven Wonders of the Ancient World."
    },
    {
        "question": "Which country built the ancient city of Machu Picchu?",
        "options": ["Aztec Empire", "Inca Empire", "Maya Empire", "Roman Empire"],
        "answer": "Inca Empire",
        "solution": "Machu Picchu in Peru was built by the Inca civilization."
    },
    {
        "question": "Who was Pakistan's national poet who inspired the idea of a separate homeland?",
        "options": ["Allama Iqbal", "Faiz Ahmed Faiz", "Josh Malihabadi", "Ahmed Faraz"],
        "answer": "Allama Iqbal",
        "solution": "Allama Iqbal's poetry and ideas inspired the demand for a separate Muslim homeland, later becoming Pakistan."
    },
    {
        "question": "Which war was fought between the North and South regions of the United States?",
        "options": ["World War I", "American Civil War", "Revolutionary War", "Cold War"],
        "answer": "American Civil War",
        "solution": "The American Civil War (1861-1865) was fought between the northern and southern United States."
    },
    {
        "question": "Which explorer is credited with reaching India by sea route first?",
        "options": ["Christopher Columbus", "Vasco da Gama", "Marco Polo", "Ferdinand Magellan"],
        "answer": "Vasco da Gama",
        "solution": "Vasco da Gama was the first European to reach India by sailing around Africa in 1498."
    },
    {
        "question": "Which country is home to the ancient city of Petra?",
        "options": ["Egypt", "Jordan", "Syria", "Iraq"],
        "answer": "Jordan",
        "solution": "Petra is an ancient city carved into rock, located in modern-day Jordan."
    },
    {
        "question": "Who was the first Governor-General of Pakistan?",
        "options": ["Liaquat Ali Khan", "Quaid-e-Azam", "Iskander Mirza", "Ayub Khan"],
        "answer": "Quaid-e-Azam",
        "solution": "Muhammad Ali Jinnah served as Pakistan's first Governor-General after independence in 1947."
    },
    {
        "question": "Which ancient civilization is credited with inventing the wheel?",
        "options": ["Egyptians", "Mesopotamians", "Greeks", "Romans"],
        "answer": "Mesopotamians",
        "solution": "The ancient Mesopotamians are credited with inventing the wheel around 3500 BCE."
    },
    {
        "question": "Who was the Chinese philosopher known for his teachings on ethics and respect?",
        "options": ["Buddha", "Confucius", "Lao Tzu", "Mencius"],
        "answer": "Confucius",
        "solution": "Confucius was an ancient Chinese philosopher whose teachings on ethics and respect greatly influenced Chinese culture."
    },
    {
        "question": "Which year did the Berlin Wall fall, symbolizing the end of the Cold War era?",
        "options": ["1985", "1987", "1989", "1991"],
        "answer": "1989",
        "solution": "The Berlin Wall fell in 1989, symbolizing the reunification of Germany and the end of Cold War divisions."
    },
        {
            "question": "In which year did World War II end?",
            "options": ["1943", "1944", "1945", "1946"],
            "answer": "1945",
            "solution": "World War II ended in 1945 after Japan's surrender in September that year."
        },
        {
            "question": "Who wrote the Pakistan Resolution (Lahore Resolution)?",
            "options": ["Allama Iqbal", "Quaid-e-Azam", "A.K. Fazlul Huq", "Liaquat Ali Khan"],
            "answer": "A.K. Fazlul Huq",
            "solution": "A.K. Fazlul Huq presented the Lahore Resolution in 1940, which laid the foundation for Pakistan."
        },
        {
            "question": "Which empire built the Great Wall of China?",
            "options": ["Roman Empire", "Chinese Empire", "Ottoman Empire", "British Empire"],
            "answer": "Chinese Empire",
            "solution": "The Great Wall was built by various Chinese dynasties over centuries to protect against invasions."
        },
        {
            "question": "Who was the first man to walk on the Moon?",
            "options": ["Buzz Aldrin", "Neil Armstrong", "Yuri Gagarin", "John Glenn"],
            "answer": "Neil Armstrong",
            "solution": "Neil Armstrong became the first man to walk on the Moon on July 20, 1969."
        },
        {
            "question": "The Indus Valley Civilization existed around which region?",
            "options": ["Egypt", "Mesopotamia", "Pakistan and India", "Greece"],
            "answer": "Pakistan and India",
            "solution": "The Indus Valley Civilization flourished in present-day Pakistan and northwest India."
        },
        {
            "question": "Which year did Pakistan become an independent country?",
            "options": ["1945", "1946", "1947", "1948"],
            "answer": "1947",
            "solution": "Pakistan gained independence from British rule on August 14, 1947."
        },
    ],

}





@app.route('/quiz')
def quiz_home():
    # Shows list of quiz subjects to choose from
    return render_template('quiz_home.html', subjects=QUIZ_DATA.keys())


@app.route('/quiz/<subject>')
def quiz(subject):
    if subject not in QUIZ_DATA:
        return "Quiz not found", 404
    questions = QUIZ_DATA[subject]
    return render_template('quiz.html', subject=subject, questions=questions)



@app.route('/quiz/<subject>/submit', methods=['POST'])
def quiz_submit(subject):
    if subject not in QUIZ_DATA:
        return "Quiz not found", 404

    questions = QUIZ_DATA[subject]
    score = 0
    total = len(questions)
    results = []

    for i, q in enumerate(questions):
        user_answer = request.form.get(f'q{i}')
        is_correct = (user_answer == q['answer'])
        if is_correct:
            score += 1
        results.append({
            "question": q['question'],
            "user_answer": user_answer,
            "correct_answer": q['answer'],
            "is_correct": is_correct,
            "solution": q.get('solution', 'hi.')
        })

    return render_template('quiz_result.html', subject=subject, score=score, total=total, results=results)

def analyze(text):
    text = text.lower().strip()

    try:
        if re.match(r'^[0-9+\-*/().^ ]+$', text):
            text = text.replace("^", "**")
            return f"🧮 Answer = {eval(text)}"
    except:
        pass

    qa = {
    "what is computer": "A computer is an electronic machine that helps us learn, work, and play.",
    "what is laptop": "A laptop is a portable computer that you can carry anywhere.",
    "what is keyboard": "A keyboard is used to type letters, numbers, and symbols.",
    "what is mouse": "A mouse is used to point, click, and select items on a computer.",
    "what is monitor": "A monitor is the screen that shows pictures and text.",
    "what is cpu": "The CPU is the brain of the computer.",
    "what is internet": "The internet connects computers around the world.",
    "what is website": "A website is a collection of web pages on the internet.",
    "what is browser": "A browser is a program used to visit websites.",
    "what is email": "Email is a way to send messages online.",

    "what is science": "Science helps us understand the world around us.",
    "what is matter": "Matter is anything that has mass and takes up space.",
    "what is water": "Water is a liquid that all living things need.",
    "what is air": "Air is a mixture of gases that we breathe.",
    "what is sun": "The Sun is a star that gives us light and heat.",
    "what is moon": "The Moon is Earth's natural satellite.",
    "what is earth": "Earth is the planet where we live.",
    "what is planet": "A planet is a large object that moves around a star.",
    "what is star": "A star is a huge ball of hot glowing gas.",
    "what is gravity": "Gravity is the force that pulls objects toward Earth.",

    "what is plant": "A plant is a living thing that grows from the soil.",
    "what is tree": "A tree is a tall plant with a trunk and branches.",
    "what is flower": "A flower is the colorful part of many plants.",
    "what is seed": "A seed grows into a new plant.",
    "what is animal": "An animal is a living creature that can move and grow.",
    "what is bird": "A bird is an animal with feathers and wings.",
    "what is fish": "A fish is an animal that lives in water.",
    "what is mammal": "A mammal is an animal that feeds milk to its babies.",
    "what is insect": "An insect is a small animal with six legs.",
    "what is butterfly": "A butterfly is a colorful flying insect.",

    "what is body": "Your body helps you move, think, and live.",
    "what is heart": "The heart pumps blood throughout the body.",
    "what is brain": "The brain controls your thoughts and body.",
    "what is eye": "Eyes help us see.",
    "what is ear": "Ears help us hear sounds.",
    "what is nose": "The nose helps us smell and breathe.",
    "what is mouth": "The mouth helps us eat and speak.",
    "what is hand": "Hands help us hold and touch things.",
    "what is leg": "Legs help us walk and run.",
    "what is bone": "Bones support and protect our body.",

    "what is math": "Math is the study of numbers and shapes.",
    "what is addition": "Addition means putting numbers together.",
    "what is subtraction": "Subtraction means taking away.",
    "what is multiplication": "Multiplication is repeated addition.",
    "what is division": "Division means sharing equally.",
    "what is number": "A number is used for counting and measuring.",
    "what is zero": "Zero means nothing or no quantity.",
    "what is fraction": "A fraction shows equal parts of a whole.",
    "what is shape": "A shape is the form of an object.",
    "what is circle": "A circle is a round shape.",

    "what is square": "A square has four equal sides.",
    "what is rectangle": "A rectangle has four sides with opposite sides equal.",
    "what is triangle": "A triangle has three sides.",
    "what is angle": "An angle is made where two lines meet.",
    "what is line": "A line is a straight path connecting points.",
    "what is centimeter": "A centimeter is a unit of length.",
    "what is kilogram": "A kilogram is a unit of weight.",
    "what is clock": "A clock tells the time.",
    "what is calendar": "A calendar shows days, weeks, and months.",
    "what is money": "Money is used to buy things.",

    "what is english": "English is a language spoken in many countries.",
    "what is alphabet": "The alphabet is a set of letters from A to Z.",
    "what is letter": "A letter is one symbol in the alphabet.",
    "what is word": "A word is made of letters and has a meaning.",
    "what is sentence": "A sentence is a group of words with complete meaning.",
    "what is noun": "A noun names a person, place, animal, or thing.",
    "what is verb": "A verb is an action word.",
    "what is adjective": "An adjective describes a noun.",
    "what is pronoun": "A pronoun replaces a noun.",
    "what is punctuation": "Punctuation marks help make writing clear.",

    "what is book": "A book contains stories or information.",
    "what is library": "A library is a place where books are kept.",
    "what is school": "A school is where children learn.",
    "what is teacher": "A teacher helps students learn.",
    "what is student": "A student is a person who learns.",
    "what is homework": "Homework is schoolwork done at home.",
    "what is exam": "An exam tests what you have learned.",
    "what is classroom": "A classroom is where lessons take place.",
    "what is lesson": "A lesson is something you learn.",
    "what is education": "Education is the process of learning.",

    "what is food": "Food gives us energy and helps us grow.",
    "what is fruit": "Fruit is healthy food that grows on plants.",
    "what is vegetable": "Vegetables are healthy foods rich in nutrients.",
    "what is milk": "Milk helps build strong bones and teeth.",
    "what is exercise": "Exercise keeps our body healthy and strong.",
    "what is sleep": "Sleep helps the body and brain rest.",
    "what is hygiene": "Hygiene means keeping yourself clean.",
    "what is toothbrush": "A toothbrush is used to clean your teeth.",
    "what is soap": "Soap helps remove dirt and germs.",
    "what is doctor": "A doctor helps people stay healthy.",

    "what is family": "A family is a group of people who love and care for each other.",
    "what is friend": "A friend is someone you like and trust.",
    "what is kindness": "Kindness means being caring and helpful.",
    "what is honesty": "Honesty means telling the truth.",
    "what is respect": "Respect means treating others politely.",
    "what is sharing": "Sharing means letting others use what you have.",
    "what is teamwork": "Teamwork means working together.",
    "what is safety": "Safety means staying protected from harm.",
    "what is happiness": "Happiness is the feeling of joy.",
    "what is love": "Love means caring deeply for others."
}

    if text in qa:
        return qa[text]
    
    match = get_close_matches(text, qa.keys(), n=1, cutoff=0.6)

    if match:
        return qa[match[0]]

    elif "noun" in text:
        return "A noun is the name of a person, place, animal, or thing."
    
    elif "Letures" in text or "Lectures" in text or "Lecture" in text or "Lectur" in text or "lecture" in text:
        return "1,Go to home after 2,click Relax & Music, 3,after you see different audios"



    elif "song" in text or "Song" in text or "songs" in text or "Songs" in text:
        return "1,Go to home after: 2,click Relax & Music,:  3,after you see different audios"
    
    elif "Music" in text or "musics" in text or "Musics" in text:
        return "1,Go to home after: 2,click Relax & Music,:  3,after you see different audios"
    

    elif "entertanments" in text or "Entertainment" in text or "Funny videos" in text or "Video" in text:
        return "1,Go to home after: 2,click Relax & Music,:  3,after you see different audios"

    elif "verb" in text:
        return "A verb is an action word, such as run, eat, or play."

    elif "adjective" in text:
        return "An adjective describes a noun."

    elif "what is matter" in text:
        return "Matter is anything that has mass and occupies space."

    elif "what is water" in text:
        return "Water is a liquid essential for life."

    elif "what is sun" in text:
        return "The Sun is a star that provides light and heat."

    elif "height" in text:
        return "Eat milk, eggs, fruits. Do exercise + get sunlight daily."
    elif "stress" in text or "sad" in text:
        return "Listen calm music, sleep well, talk to friends."
    elif "coding" in text:
        return "You can become Software Engineer or AI Developer."
    elif "drawing" in text:
        return "You can become Graphic Designer or Animator."
    elif "weak" in text or "tired" in text:
        return "Eat healthy food, drink water, sleep 7-8 hours."
    elif "Routine" in text or "routine" in text or "rotine" in text:
        return "Get up Early, Get Sun Light, Or Walking, night Sleep=7-8 hours, Reduce Screen Time"
 

    elif "hello" in text or "hi" in text:
        return "Hello! How can I help you today?"

    else:
        return "Stay healthy, follow routine, explore your interests."


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_response', methods=['POST'])
def get_response():
    data = request.get_json()
    message = data.get("message", "")
    answer = analyze(message)
    return jsonify({"reply": answer})

@app.route('/ask')
def ask():
    return render_template('ask.html')


@app.route('/result', methods=['POST'])
def result():
    user_input = request.form.get('problem', '')
    answer = analyze(user_input)
    return render_template('result.html', input=user_input, answer=answer)


@app.route('/health')
def health():
    return render_template('health.html')


@app.route('/music')
def music():
    return render_template('music.html')


@app.route('/chat')
def chat():
    return render_template('chat.html')


@app.route('/career')
def career():
    return render_template('career.html')


@app.route('/routine')
def routine():
    return render_template('routine.html')


@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/entertainment')
def entertainment():
    return render_template('entertainment.html')


@app.route('/songs')
def songs():
    return render_template('songs.html')


@app.route('/study')
def study():
    return render_template('study.html')


@app.route('/movies')
def movies():
    return render_template('movies.html')


@app.route('/community')
def community():
    return render_template('community.html')
    








if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=False)
