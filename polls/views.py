from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.db.models import F
from django.urls import reverse
from django.views import View, generic
from django.utils import timezone

from .models import Questions, Choice
from .forms import *


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Questions.objects.filter(pub_date__lte=timezone.now()).order_by(
            "-pub_date"
        )[:5]

    # def get(self, request):
    #     return render(
    #         request, "polls/index.html", {"latest_question_list": self.get_queryset()}
    #     )


class DetailView(generic.DetailView):
    model = Questions
    template_name = "polls/detail.html"
    context_object_name = "question"


class ResultsView(generic.DetailView):
    model = Questions
    template_name = "polls/results.html"
    context_object_name = "question"


class VoteView(View):
    context_object_name = "question"

    def get(self, request, question_id):
        question = get_object_or_404(Questions, pk=question_id)

        return render(request, "polls/detail.html", {"question": question})

    def post(self, request, question_id):
        question = get_object_or_404(Questions, pk=question_id)

        try:
            selected_choice = question.choice_set.get(pk=request.POST["choice"])
        except (KeyError, Choice.DoesNotExist):
            return render(
                "polls/detail.html",
                {"question": question, "error_message": "You didn't select a choice."},
            )
        else:
            selected_choice.votes = F("votes") + 1
            selected_choice.save()

            return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))


class QuestionsView(View):
    context_object_name = "question"

    def get(self, request):
        from django.utils import timezone

        form = QuestionsForm()

        return render(request, "polls/question_create.html", {"form": form})

    def post(self, request):
        from django.utils import timezone

        form = QuestionsForm(request.POST)

        if form.is_valid():
            question = Questions(
                question_text=form.cleaned_data["question_text"],
                pub_date=timezone.now(),
            )
            question.save()

        return HttpResponseRedirect(reverse("polls:vote", args=(question.id,)))


class ChoiceView(View):
    context_object_name = "choice"

    def get(self, request, question_id):
        question = get_object_or_404(Questions, pk=question_id)

        form = ChoiceForm()

        return render(
            request, "polls/choice_create.html", {"form": form, "question": question}
        )

    def post(self, request, question_id):
        choice = get_object_or_404(Questions, pk=question_id)

        form = ChoiceForm(request.POST)

        if form.is_valid():
            choice = choice.choice_set.create(
                choice_text=form.cleaned_data["choice_text"],
                votes=0,
            )
            choice.save()

        return HttpResponseRedirect(reverse("polls:vote", args=(question_id,)))
