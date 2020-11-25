# Django GraphQL API with dataloaders ⚡️

This is a Django GraphQL App based on the Django Polls tutorial.
I made this to experiment 🧪 with dataloaders and the relay pattern.

## Run locally

Install Pipenv

https://pypi.org/project/pipenv/

`pipenv install`

`cd django_graphene_data_loaders_demo`

`pipenv run python manage.py migrate`

`pipenv run python manage.py createsuperuser`

Go to the Django admin, login, and add your questions and choices. `localhost:8000/admin`

`pipenv run python manage.py runserver`

## Query

Resolve question uses a dataloader for efficient querying.

```
{
  choices {
    edges {
      node {
        id
        choiceText
        votes
      	question {
          id
          questionText
        }
      }
    }
  }
}

```

## Mutation

```
mutation Vote($question: ID, $choice: ID) {
  vote(questionGlobalId: $question, choiceGlobalId: $choice){
    question {
      id
      choiceSet {
        edges {
          node {
            id
            votes
          }
        }
      }
    }
  }
}
```

TODO:

[] Frontend CRNA / Apollo

[] Add auth and user types
