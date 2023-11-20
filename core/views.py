from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# importing the openai API
import openai
from .forms import OpenAICommandForm
from .models import OpenAICommand
from django.contrib.auth.decorators import login_required


from decouple import config
from dotenv import load_dotenv

load_dotenv()

# import the generated API key from the secret_key file
# from .secret_key import API_KEY
# loading the API key from the secret_key file
# openai = openai.OpenAI()
openai.api_key = config("OPENAI_KEY")




# Create your views here.
# this is the home view for handling home page logic
def openai_command(prompt, template, category):
    # the try statement is for sending request to the API and getting back the response
    # formatting it and rendering it in the template
    try:
        # making a request to the API
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a women's health chatbot. Your name is Ayla."},
                {"role": "user", "content": prompt},
            ]
        )
        # formatting the response input
        # formatted_response = response['choices'][0]['message']['content'].strip()
        formatted_response = response.choices[0].message.content

        # this will render the results in the chatbot.html template
        return formatted_response
    # the except statement will capture any error
    except:
        # this will redirect to the 404 page after any error is caught
        return redirect('error_handler')

def FetchHistory(request, category):
    
    history_data  = OpenAICommand.objects.filter(user=request.user, category=category).order_by('date')

    return history_data 

def GetFormData(request, code_form, extra_prompt, template, category):
    # Get form data
    title = code_form.cleaned_data['title']
    version = code_form.cleaned_data['version']
    category = category
    prompt = code_form.cleaned_data['prompt']

    # Add the extra_prompt
    prompt = extra_prompt + ' ' + prompt

    chatbot_response = openai_command(prompt, template, category)

    # Create OpenAICommand instance
    chatbot_entry = OpenAICommand.objects.create(
        title=title,
        version=version,
        category=category,
        response=chatbot_response,
        prompt=prompt,
        user=request.user
    )

    return chatbot_entry, category


@login_required
def codehub(request):
        
    template = 'core/codehub.html'
    extra_prompt = "Review the provided software code and perform refactoring, debugging, code duplicate detection, code security analysis, code review summarization, and comments using the AI-Powered Code Review Assistant with the OpenAI API. Additionally, integrate insights from a knowledge base by linking to relevant documentation and articles for a thorough and improved code assessment."
    category = 'Code Review'
    
    history = FetchHistory(request, category)

    # checking if the request method is POST
    if request.method == 'POST':
        code_form = OpenAICommandForm(request.POST, instance=request.user)
        if code_form.is_valid():

            # category, chatbot_entry = GetFormData(request, code_form, extra_prompt, template, category)
            chatbot_entry, category = GetFormData(request, code_form, extra_prompt, template, category)

            # Redirect to the result view with the newly created instance's primary key
            return redirect('core:result', pk=chatbot_entry.pk, category=category)
    

        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')

    # this runs if the request method is GET
    else:
        code_form = OpenAICommandForm(instance=request.user)

        context = {
            'code_form': code_form,
            'history': history
        }
        # this will render when there is no request POST or after every POST request
        return render(request, template, context)


@login_required
def automate(request):
    template = 'core/automate.html'
    extra_prompt = "Auto-generate comprehensive documentation, connect with external knowledge base, assess Documentation Health Score, pull inline code comments, and include Live Code examples for the provided software code."
    category = 'Automate'

    history = FetchHistory(request, category)

    # checking if the request method is POST
    if request.method == 'POST':
        code_form = OpenAICommandForm(request.POST, instance=request.user)
        if code_form.is_valid():

            # category, chatbot_entry = GetFormData(request, code_form, extra_prompt, template, category)
            chatbot_entry, category = GetFormData(request, code_form, extra_prompt, template, category)

            # Redirect to the result view with the newly created instance's primary key
            return redirect('core:result', pk=chatbot_entry.pk, category=category)

        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')


    else:
        code_form = OpenAICommandForm(instance=request.user)

        # this runs if the request method is GET
        context = {
                'code_form': code_form,
                'history': history,
            }
            # this will render when there is no request POST or after every POST request
        return render(request, template, context)


@login_required
def tester(request):

    template = 'core/tester.html'
    extra_prompt = "Review the provided software code and generate thorough and exhaustive test cases using the Automated Test Case Generator with the OpenAI API. Employ dynamic test data generation, an AI-based test oracle, test case documentation, randomized testing, stateful test generator, feedback loop with developers, and adversarial testing to enhance testing procedures and ensure comprehensive test coverage."
    category = 'Tester'

    history = FetchHistory(request, category)
    
        # checking if the request method is POST
    if request.method == 'POST':
        code_form = OpenAICommandForm(request.POST, instance=request.user)
        if code_form.is_valid():

            # category, chatbot_entry = GetFormData(request, code_form, extra_prompt, template, category)
            chatbot_entry, category = GetFormData(request, code_form, extra_prompt, template, category)

            # Redirect to the result view with the newly created instance's primary key
            return redirect('core:result', pk=chatbot_entry.pk, category=category)

        else:
            messages.error(request, 'There was an error updating your profile. Please check the form.')

    # this runs if the request method is GET
    else:
        code_form = OpenAICommandForm(instance=request.user)

        context = {
            'code_form': code_form,
            'history': history,
        }
        # this will render when there is no request POST or after every POST request
        return render(request, template, context)
    
    return render(request, template)


@login_required
def result(request, pk, category):
    history = FetchHistory(request, category)

    result = OpenAICommand.objects.get(user=request.user, pk=pk)

    context = {
        'pk': pk,
        'history': history,
        'category': category,
        'result': result
    }
    return render(request, 'core/result.html', context)


# this is the view for handling errors
def error_handler(request):
    return render(request, '404.html')
