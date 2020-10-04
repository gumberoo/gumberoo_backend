# Gumberoo Backend
Click [here](https://gumberoo-backend.herokuapp.com/) to view Gumberoo's deployed API

Gumberoo is a website for elementary school educators inspired by the education learning experience during the pandemic of 2020. As schools have gone remote, there has never been a more crucial period/threat to our children's education. Gumberoo's API is built on Python and Django. Teachers can create students and check for understanding "quizzes" after each lesson. The statistic endpoints help teachers gain an overview of how well they taught the lesson and how much of the material their student's are comphrehending.

When a student has completed the lesson check for understanding, they have the opportunity to write a reflection on how they felt during the lesson. Their comment is then analyzed by the IMB WATSON TONE ANALYZER to return an overall mood. Teachers can use this analysis to gain an overview of the student's mental well being. The mood analyzer was implemented to give introverted students a chance to communicate with their teachers.

**Contributers**

[Derek Borski](https://github.com/dborski)

[Max Mitrani](https://github.com/Lithnotep)

[Melanie Tran](https://github.com/melatran)

## Table of Contents

* [Software Requirements](#software-requirements)
* [IBM Watson Tone Analyzer API](#ibm-watson-tone-analyzer-api)
* [Getting Started](#getting-started)
* [Test Suite](#running-the-test-suite)
* [End Points](#end-points)
    * [Teacher Endpoints](#teacher-endpoints)
    * [Teacher Students Endpoints](#teacher-students-endpoints)
    * [Teacher Lesson Endpoints](#teacher-lesson-endpoints)
    * [Statistics Endpoints](#statistics-endpoints)

## Software Requirements
<img width="764" alt="Screen Shot 2020-09-13 at 12 39 02 PM" src="https://user-images.githubusercontent.com/59414750/93025782-2dd8dd80-f5be-11ea-8800-11f7d0ee4f07.png">

- [Python 3.8.5](https://www.python.org/download/releases/3.0/)
- [Django 3.1.1](https://www.djangoproject.com/)
- [Pip 20.1.1](https://pip.pypa.io/en/stable/)
- [TravisCI](https://travis-ci.org/)
- [PostgreSQL](https://www.postgresql.org/docs/9.3/app-psql.html)

## IBM Watson Tone Analyzer API
The Gumberoo backend incorporates the [IBM Watson Tone Analyzer API](https://cloud.ibm.com/docs/tone-analyzer?topic=tone-analyzer-gettingStarted) to improve a teacher's relationship with their students and track their progress and growth with each lesson. After completing a "Check for Understanding", students are given the chance to write their mood/feelings/thoughts about the lesson. The Watson Tone Analyzer is then used to analyze a student's response and return an overall mood for that student. If the student's overall response is negative, the teacher is aware of the students they have to checkin with.

## Getting Started

1. Fork this repository and clone it down
2. Setup a virtualenv

    a. `python3 -m venv myenv`
    
    b. `source myenv/bin/activate`
    
3. Run `pip install -r requirements.txt` to install libraries
4. Create data in PosgreSQL

    a. `$ psql`
    
    b. `$ CREATE DATABASE gumberoo;`
    
    c. `$ \q`
5. Run Migrations

    a. Run `python manage.py makemigrations`
    
    b. Run `python manage.py migrate`

## Running the Test Suite
To check if tests are passing, run `python ./manage.py test`

## End Points

### Teacher Endpoints

**GET** `/api/v1/teachers`  (Get a list of all teachers)

*Response*
```
[
    {
        "id": 1,
        "first_name": "Sevrus",
        "last_name": "Snape"
    },
    {
        "id": 2,
        "first_name": "Minerva",
        "last_name": "McGonagall"
    },
    {
        "id": 3,
        "first_name": "Albus",
        "last_name": "Dumbledore"
    }
]
```

**POST** `/api/v1/teachers` (Create a new teacher)

*Body*
```
{
    "first_name": "Remus",
    "last_name": "Lupin"
}
```

*Response*
```
{
  "id": 4,
  "first_name": "Remus",
  "last_name": "Lupin"
}
```

**GET** `/api/v1/teachers/:teacher_id` (Get information about a teacher by teacher_id)

*Response*
```
{
    "id": 1,
    "first_name": "Sevrus",
    "last_name": "Snape"
}
```

### Teacher Students Endpoints

**POST** `/api/v1/teachers/:teacher_id/students` (Create students for a teacher)

*Body*  

```{      
      'students': [   
        {   
        'first_name': 'newStudent1First',  
        'last_name': 'newStudent1Last'
        },   
        {   
        'first_name': 'newStudent2First',  
        'last_name': 'newStudent2Last'
        }   
      ]   
    }
```

*Response*   
```
[   
    {   
        "teacher": 1,   
        "id": 7,   
        "first_name": "newStudent1First",   
        "last_name": "newStudent1Last"
    },   
    {   
        "teacher": 1,   
        "id": 8,   
        "first_name": "newStudent2First",   
        "last_name": "newStudent2Last"
    }   
]
```
    
**GET** `/api/v1/teachers/:teacher_id/students` (Get all students for a teacher)    

*Response* 
```
 [   
    {   
        "teacher": 1,   
        "id": 1,   
        "first_name": "newStudent1First",   
        "last_name": "newStudent1Last",
        "class_rank": 1
    },   
    {   
        "teacher": 1,   
        "id": 2,   
        "first_name": "newStudent2First",   
        "last_name": "newStudent2Last",
        "class_rank": 2
    }   
  ]     
 ```
 **POST** `/api/v1/students/:student_id` (Create a lesson for a student when they take the checkpoint for a lesson)
 
 *Body*
 ```
 {
    "lesson": 2,
    "score": 1,
    "mood": "I'm going to cry but I'm happy it's over"
 }
 ```
 
 *Response*
 ```
 {
    "student": 3,
    "lesson": 2,
    "score": 1,
    "mood": "I'm going to cry but I'm happy it's over"
    "mood_analysis": "Sadness"
 }
 ```
 ### Teacher Lesson Endpoints
 
 **GET** `/api/v1/lessons/:lesson_id`  (Get a specific lesson)  

 *Response*

```
{
  'id': 1,
  'name': 'Lesson 1',
  'questions': [
    {
      'id': 1,
      'question': 'Question 1',
      'reading': 'Reading 1',
      'answers': [
        {
          'id': 1,
          'answer': 'Answer 1 Text',
          'correct': false
        },
        {
          'id': 2,
          'answer': 'Answer 2 Text',
          'correct': true
        }
      ]
    },
    {
      'id': 2,
      'question': 'Question 2',
      'reading': 'Reading 2',
      'answers': [
        {
          'id': 3,
          'answer': 'Answer 3 Text',
          'correct': true
        },
        {
          'id': 4,
          'answer': 'Answer 4 Text',
          'correct': false
        }
      ]
    }
  ],
  'teacher': {
    'id': 1,
    'first_name': 'teacher1First',
    'last_name': 'teacher1Last'
  }
}
```
**GET** `/api/v1/teachers/:teacher_id/lessons/`  (Get all lessons for a specific teacher)

*Response* 
```
[
    {
        "id": 1,
        "name": "Lesson 1",
        "questions": [],
        "teacher": {
            "id": 1,
            "first_name": "Harry",
            "last_name": "Potter",
            "created_at": "2020-09-10T15:30:53Z",
            "updated_at": "2020-09-10T15:30:56Z"
        }
    },
    {
        "id": 2,
        "name": "lesson 2",
        "questions": [
            {
                "id": 1,
                "question": "Question 1",
                "reading": "Question 1 Reading",
                "answers": [
                    {
                        "id": 1,
                        "answer": "Answer 1",
                        "correct": false
                    },
                    {
                        "id": 2,
                        "answer": "Answer 2",
                        "correct": true
                    }
                ]
            },
            {
                "id": 2,
                "question": "Question 2",
                "reading": "Question 2 Reading",
                "answers": [
                    {
                        "id": 3,
                        "answer": "Answer 3 Description",
                        "correct": true
                    },
                    {
                        "id": 4,
                        "answer": "Answer 4 Description",
                        "correct": false
                    }
                ]
            }
        ],
        "teacher": {
            "id": 1,
            "first_name": "Harry",
            "last_name": "Potter",
            "created_at": "2020-09-10T15:30:53Z",
            "updated_at": "2020-09-10T15:30:56Z"
        }
    },
    {
        "id": 3,
        "name": "lessonName1",
        "questions": [
            {
                "id": 3,
                "question": "question1 description",
                "reading": "question1 reading",
                "answers": [
                    {
                        "id": 5,
                        "answer": "answer1 description",
                        "correct": false
                    },
                    {
                        "id": 6,
                        "answer": "answer2 description",
                        "correct": false
                    },
                    {
                        "id": 7,
                        "answer": "answer3 description",
                        "correct": true
                    },
                    {
                        "id": 8,
                        "answer": "answer4 description",
                        "correct": false
                    }
                ]
            }
        ],
        "teacher": {
            "id": 1,
            "first_name": "Harry",
            "last_name": "Potter",
            "created_at": "2020-09-10T15:30:53Z",
            "updated_at": "2020-09-10T15:30:56Z"
        }
    },
    {
        "id": 4,
        "name": "New Lesson",
        "questions": [
            {
                "id": 4,
                "question": "question1 description",
                "reading": "question1 reading",
                "answers": [
                    {
                        "id": 9,
                        "answer": "answer1 description",
                        "correct": false
                    },
                    {
                        "id": 10,
                        "answer": "answer2 description",
                        "correct": false
                    },
                    {
                        "id": 11,
                        "answer": "answer3 description",
                        "correct": true
                    },
                    {
                        "id": 12,
                        "answer": "answer4 description",
                        "correct": false
                    }
                ]
            }
        ],
        "teacher": {
            "id": 1,
            "first_name": "Harry",
            "last_name": "Potter",
            "created_at": "2020-09-10T15:30:53Z",
            "updated_at": "2020-09-10T15:30:56Z"
        }
    }
]
```

**POST** `/api/v1/teachers/:teacher_id/lessons/`  (Create a new lesson for a specific teacher)  


 *Request body*
 ```
{
  'lesson': {
    'name': 'lessonName1',
    'questions': [
        {
          'question': 'question1 description',
          'reading': 'question1 reading',
          'answers': [
              {
                'answer': 'answer1 description',
                'correct': 'false'
              },
              {
                'answer': 'answer2 description',
                'correct': 'false'
              },
              {
                'answer': 'answer3 description',
                'correct': 'false'
              },
              {
                'answer': 'answer4 description',
                'correct': 'false'
              }
            ]
        },
        {
          'question': 'question2 description',
          'reading': 'question2 reading',
          'answers': [
              {
                'answer': 'answer1 description',
                'correct': 'false'
              },
              {
                'answer': 'answer2 description',
                'correct': 'false'
              },
              {
                'answer': 'answer3 description',
                'correct': 'false'
              },
              {
                'answer': 'answer4 description',
                'correct': 'false'
              }
            ]
          }   
      ]
  }
 }
 ```

 *Response*
 
```
{
  'id': 1,
  'name': 'lessonName1',
  'questions': [
    {
      'id': 1,
      'question': 'question1 description',
      'reading': 'question1 reading',
      'answers': [
        {
          'id': 1,
          'answer': 'answer1 description',
          'correct': false
        },
        {
          'id': 2,
          'answer': 'answer2 description',
          'correct': true
        },
        {
          'id': 3,
          'answer': 'answer3 description',
          'correct': false
        },
        {
          'id': 4,
          'answer': 'answer4 description',
          'correct': false
        }
      ]
    },
    {
      'id': 2,
      'question': 'question2 description',
      'reading': 'question2 reading',
      'answers': [
        {
          'id': 3,
          'answer': 'answer1 description',
          'correct': true
        },
        {
          'id': 4,
          'answer': 'answer2 description',
          'correct': false
        },
        {
          'id': 5,
          'answer': 'answer3 description',
          'correct': true
        },
        {
          'id': 6,
          'answer': 'answer4 description',
          'correct': false
        }
      ]
    }
  ],
  'teacher': {
    'id': 1,
    'first_name': 'teacher1First',
    'last_name': 'teacher1Last'
  }
}
```
**GET** `api/v1/lessons/:lesson_id/students/:student_id/` get score specific score and moood for a student from a lesson.  

 *Response*

 ```
 {
   'lesson': 2
   'student: 3
   'score': 6
   'mood': "Mad"
 }
 ```  

**GET** `api/v1/lessonstudents/:lesson_id/` Get all students scores and moods from a given lesson.  

*Response*
```
{[
  {
   'lesson': 2
   'student: 3
   'score': 6
   'mood': "Mad"
 },
 {
   'lesson': 2
   'student: 4
   'score': 2
   'mood': "Happy"
 },
 {
   'lesson': 2
   'student: 5
   'score': 8
   'mood': "Sad"
 }
]}
```
### Statistics Endpoints

**GET** `api/v1/lessons/:lesson_id/zscores/` Get calculated z-scores for every student's score on a specific lesson

*Response*
```
{
    "student_id": 1,
    "zscore": 1.4078871326090967
}
```

**GET** `api/v1/students/:student_id/average_score/` Get aggregated average score on all lessons taken by a single student

*Response*
```
{
    "student_id": 1,
    "average_score": 65
}
```

**GET** `api/v1/lessons/:lesson_id/average_score/` Get aggregated average score for all student's scores on a single lesson

*Response*
```
{
    "lesson_id": 1,
    "average_score": 88
}
```

