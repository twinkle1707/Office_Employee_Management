from django.shortcuts import render,redirect
from .models import *

def index(request):
    feedbacks = CustomerFeedback.objects.all()
    return render(request,'surveys.html',{"feedbacks": feedbacks})


def customer_feedback(request,id):
    feedback = CustomerFeedback.objects.get(id=id)
    if request.method == "POST":
        for question in feedback.question.all():
            response_text = request.POST.get(f"response_{question.id}")
            selected_option_ids = request.POST.getlist(f"options_{question.id}")

            response = CustomerResponse.objects.create(
                feedback = feedback,
                question = question,
                response_text = response_text if question.question_type in ["Text","BigText"] else None

            )
            if selected_option_ids:
                selected_options = Options.objects.filter(id__in = selected_option_ids)
                response.selected_options.set(selected_options)
        return redirect("/thank-you/")
    return render(request,'survey.html',{"questions":feedback.question.all()})


def thank_you(request):
    return render(request,"thank_you.html")