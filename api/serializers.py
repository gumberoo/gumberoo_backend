from rest_framework import serializers
from api.models import Teacher, Lesson, Question, Answer, LessonStudent, Student
from api.popos import LessonScore, StudentScore


class TeacherSerializer(serializers.ModelSerializer):
  class Meta:
    model = Teacher
    fields = (
      'id', 'first_name', 'last_name'
    )

class StudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = Student
    fields = (
        'teacher', 'id', 'first_name', 'last_name'
    )

class StudentRankSerializer(serializers.ModelSerializer):
  class_rank = serializers.SerializerMethodField()
  class Meta:
    model = Student
    fields = (
        'teacher', 'id', 'first_name', 'last_name', 'class_rank'
    )

  def get_class_rank(self, obj):
    return obj.class_rank


class AnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    fields = (
      'id', 'answer', 'correct'
    )
    depth = 0

class QuestionSerializer(serializers.ModelSerializer):
  answers = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
  class Meta:
    model = Question
    fields = (
      'id', 'question', 'reading', 'answers'
    )
    read_only_fields = (
      'answers'
    )

class QuestionAnswerSerializer(serializers.ModelSerializer):
  class Meta:
    model = Answer
    depth = 1
    fields = ('id', 'answer', 'correct')

class LessonQuestionSerializer(serializers.ModelSerializer):
  answers = QuestionAnswerSerializer(source='answer_set', many=True, read_only=True)
  class Meta:
    model = Question
    depth = 1
    fields = ('id', 'question', 'reading', 'answers')

class LessonSerializer(serializers.ModelSerializer):
  questions = LessonQuestionSerializer(source='question_set', many=True, read_only=True)
  class Meta:
    model = Lesson
    fields = (
      'id', 'name', 'questions', 'teacher'
    )
    read_only_fields = ['questions']
    depth = 1

class LessonStudentSerializer(serializers.ModelSerializer):
  class Meta:
    model = LessonStudent
    fields = (
      "student", "lesson", "score", "mood", "mood_analyzer"
    )

class StudentScoreSerializer(serializers.Serializer):
  student_id = serializers.IntegerField()
  average_score = serializers.IntegerField()


class LessonScoreSerializer(serializers.Serializer):
  lesson_id = serializers.IntegerField()
  average_score = serializers.IntegerField()

class ZScoreSerializer(serializers.Serializer):
  student_id = serializers.IntegerField()
  zscore = serializers.FloatField()
