"""django_graphene_data_loaders_demo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from graphene_django.views import GraphQLView
from django_graphene_data_loaders_demo.schema import schema
from django.views.decorators.csrf import csrf_exempt
from polls.dataloaders import QuestionLoader
from django.utils.functional import cached_property

class GQLContext:
    def __init__(self, request):
        self.request = request
    # TODO: add users and auth
    @cached_property
    def user(self):
        return self.request.user
    @cached_property
    def question_loader(self):
        return QuestionLoader()
class GraphQL(GraphQLView):
    def get_context(self, request):
        return GQLContext(request)

urlpatterns = [
    path("graphql", csrf_exempt(GraphQL.as_view(graphiql=True, schema=schema))),
    path('admin/', admin.site.urls),
]