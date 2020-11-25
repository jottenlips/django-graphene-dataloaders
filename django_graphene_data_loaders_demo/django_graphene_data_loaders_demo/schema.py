import graphene

from polls.schema import PollsQuery, PollsMutation
from graphene_django.debug import DjangoDebug
from graphql import GraphQLError


class Query(PollsMutation, PollsQuery, graphene.ObjectType):
    debug = graphene.Field(DjangoDebug, name='_debug')
    pass

class Mutation(PollsMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query,mutation=Mutation)
