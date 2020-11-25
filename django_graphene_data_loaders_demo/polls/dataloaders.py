from promise import Promise
from promise.dataloader import DataLoader
from polls.models import Question, Choice

class QuestionLoader(DataLoader):
    def batch_load_fn(self, keys):
        questions = {question.id: question for question in Question.objects.filter(id__in=keys)}
        return Promise.resolve([questions.get(question_id) for question_id in keys])