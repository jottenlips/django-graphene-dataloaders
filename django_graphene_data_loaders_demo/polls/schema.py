import graphene
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField
from polls.models import Question, Choice
from graphql_relay.node.node import from_global_id
from graphql import GraphQLError

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        filter_fields = ['id']
        interfaces = (graphene.relay.Node,)

class ChoiceType(DjangoObjectType):
    class Meta:
      model = Choice
      filter_fields = ['id']
      interfaces = (graphene.relay.Node,)
    
    question = graphene.Field(QuestionType)

    def resolve_question(root, info):
      return info.context.question_loader.load(root.question.id)

      

class VoteMutation(graphene.Mutation):
    class Arguments:
        question_global_id = graphene.ID()
        choice_global_id = graphene.ID()

    question = graphene.Field(QuestionType)

    @staticmethod
    def mutate(root, info, question_global_id=None, choice_global_id=None):
      question_id = from_global_id(question_global_id)[1]
      choice_id = from_global_id(choice_global_id)[1]
      question = Question.objects.get(id=question_id)
      try:
        selected_choice = question.choice_set.get(pk=choice_id)
      except (KeyError, Choice.DoesNotExist):
          # Redisplay the question voting form.
        raise GraphQLError('No Choice selected')
      else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return VoteMutation(question=question)
      return None
    
class PollsMutation(object):
  vote = VoteMutation.Field();
  
class PollsQuery(graphene.ObjectType):
    questions = DjangoFilterConnectionField(QuestionType)
    choices = DjangoFilterConnectionField(ChoiceType)
    # me = graphene.Field(UserType)

    def resolve_me(self, info):
        if not hasattr(info.context.user, 'is_authenticated'):
            return None
        if not info.context.user.is_authenticated:
            return None
        else:
            return info.context.user