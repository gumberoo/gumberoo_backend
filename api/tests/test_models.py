from django.test import TestCase
from api.models import Teacher, Student, Lesson, Question, Answer, LessonStudent

from .factories import TeacherFactory, StudentFactory

class TeacherModelTest(TestCase):
  def setUp(self):
    teacher = TeacherFactory(first_name='teacher1First')

  def test_string_representation(self):
    teacher = Teacher.objects.get(first_name='teacher1First')
    self.assertEqual(str(teacher), teacher.full_name())

  def test_full_name(self):
    teacher = Teacher.objects.get(first_name='teacher1First')
    self.assertEqual(str(teacher.full_name()), str(f'{teacher.first_name} {teacher.last_name}'))

class StudentModelTest(TestCase):
  def setUp(self):
    # Both a student and a teacher are created here because an association is setup
    # in the factories. student.teacher can still be called
    student = StudentFactory(first_name='student1First')

  def test_string_representations(self):
    student = Student.objects.get(first_name='student1First')
    self.assertEqual(str(student), student.full_name())

  def test_full_name(self):
    student = Student.objects.get(first_name='student1First')
    self.assertEqual(str(student.full_name()), str(f'{student.first_name} {student.last_name}'))

class LessonModelTest(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory()
    self.teacher1.lesson_set.create(name='lesson1', description='lesson1 Description')

  def test_string_representation(self):
    lesson = Lesson.objects.get(name='lesson1')
    self.assertEqual(str(lesson), lesson.name)

class QuestionModelTest(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory()
    lesson = self.teacher1.lesson_set.create(name='lesson2', description='lesson2 Description')
    lesson.question_set.create(question='question1', reading='question1 Reading')

  def test_string_representation(self):
    question = Question.objects.get(question='question1')
    self.assertEqual(str(question), question.question)

class AnswerModelTest(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory()
    lesson = self.teacher1.lesson_set.create(name='lesson3', description='lesson3 Description')
    question = lesson.question_set.create(question='question2', reading='question2 Reading')
    question.answer_set.create(answer='answer1', correct=False)
  
  def test_string_representation(self):
    answer = Answer.objects.get(answer='answer1')
    self.assertEqual(str(answer), answer.answer)

class LessonStudentModelTest(TestCase):
  def setUp(self):
    self.teacher1 = TeacherFactory(first_name='teacher1First', last_name='teacher1Last')

    self.lesson1 = self.teacher1.lesson_set.create(name='name1', description='description1')

    self.question1 = self.lesson1.question_set.create(question='question1', reading='reading1')
    self.answer1 = self.question1.answer_set.create(answer='answer1', correct=False)
    self.answer2 = self.question1.answer_set.create(answer='answer2', correct=True)

    self.question2 = self.lesson1.question_set.create(question='question2', reading='reading2')
    self.answer3 = self.question2.answer_set.create(answer='answer3', correct=True)
    self.answer4 = self.question2.answer_set.create(answer='answer4', correct=False)

    self.lesson2 = self.teacher1.lesson_set.create(name='name2', description='description2')

    self.question3 = self.lesson2.question_set.create(question='question1', reading='reading1')
    self.answer5 = self.question3.answer_set.create(answer='answer1', correct=False)
    self.answer6 = self.question3.answer_set.create(answer='answer2', correct=True)

    self.question4 = self.lesson2.question_set.create(question='question2', reading='reading2')
    self.answer7 = self.question4.answer_set.create(answer='answer3', correct=True)
    self.answer8 = self.question4.answer_set.create(answer='answer4', correct=False)

    self.student1 = StudentFactory()
    self.student2 = StudentFactory()

    self.lessonStudent1 = self.student1.lessonstudent_set.create(lesson_id=self.lesson1.id, mood='cranky', score=90)
    self.lessonStudent2 = self.student1.lessonstudent_set.create(lesson_id=self.lesson2.id, mood='cranky', score=96)

    self.lessonStudent4 = self.student2.lessonstudent_set.create(lesson_id=self.lesson1.id, mood='cranky', score=62)
    self.lessonStudent5 = self.student2.lessonstudent_set.create(lesson_id=self.lesson2.id, mood='cranky', score=22)
  
  def test_student_average_score(self):
    score = LessonStudent.student_average_score(self.student2.id)['score__avg']

    self.assertEqual(score, 42.0)

  def test_lesson_average_score(self):
    score = LessonStudent.lesson_average_score(self.lesson1.id)['score__avg']

    self.assertEqual(score, 76.0)

  def test_student_average_score(self):
    students = Student.ranked_by_average_score(self.teacher1.id)

    expected_students = ["<Student: %s %s>" % (self.student1.first_name, self.student1.last_name), "<Student: %s %s>" % (self.student2.first_name, self.student2.last_name)]

    self.assertQuerysetEqual(students, expected_students)


