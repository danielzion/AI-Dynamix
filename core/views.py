from django.shortcuts import render, redirect
# importing render and redirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# importing the openai API
import openai
from .forms import OpenAICommandForm
from .models import OpenAICommand


from decouple import config
from dotenv import load_dotenv

load_dotenv()

# import the generated API key from the secret_key file
# from .secret_key import API_KEY
# loading the API key from the secret_key file
openai.api_key = config("OPENAI_KEY")



# Create your views here.
# this is the home view for handling home page logic
def openai_command(prompt, template, category):
    # the try statement is for sending request to the API and getting back the response
    # formatting it and rendering it in the template
    try:
        # making a request to the API
        response = openai.Completion.create(model="text-davinci-003", prompt=prompt, temperature=1, max_tokens=1000)
        # formatting the response input
        formatted_response = response['choices'][0]['text']
        # bundling everything in the context
        context = {
            'formatted_response': formatted_response,
            'prompt': prompt
        }
        # this will render the results in the chatbot.html template
        return context
    # the except statement will capture any error
    except:
        # this will redirect to the 404 page after any error is caught
        return redirect('error_handler')


def codehub(request):
        
    template = 'core/codehub.html'
    extra_prompt = "Review the provided software code and perform refactoring, debugging, code duplicate detection, code security analysis, code review summarization, and comments using the AI-Powered Code Review Assistant with the OpenAI API. Additionally, integrate insights from a knowledge base by linking to relevant documentation and articles for a thorough and improved code assessment."
    # checking if the request method is POST
    if request.method == 'POST':
        code_form = OpenAICommandForm(request.Post, instance=request.user)
        # getting prompt data from the form
        prompt = request.POST.get('prompt')

        prompt = extra_prompt + ' ' + prompt

        openai_command(request, prompt, template, 'Code Review')
    # this runs if the request method is GET
    else:
        code_form = OpenAICommandForm(instance=request.user)

        context = {
            'code_form': code_form
        }
        # this will render when there is no request POST or after every POST request
        return render(request, template, context)
    
    return render(request, template)

def automate(request):
    template = 'core/automate.html'
    extra_prompt = "Auto-generate comprehensive documentation, connect with external knowledge base, assess Documentation Health Score, pull inline code comments, and include Live Code examples for the provided software code."
    # checking if the request method is POST
    if request.method == 'POST':
        # getting prompt data from the form
        prompt = request.POST.get('prompt')

        prompt = extra_prompt + ' ' + prompt

        openai_command(request, prompt, template, 'Automate')
    # this runs if the request method is GET
    else:
        # this will render when there is no request POST or after every POST request
        return render(request, template)
    
    return render(request, template)

def tester(request):

    template = 'core/tester.html'
    extra_prompt = "Review the provided software code and generate thorough and exhaustive test cases using the Automated Test Case Generator with the OpenAI API. Employ dynamic test data generation, an AI-based test oracle, test case documentation, randomized testing, stateful test generator, feedback loop with developers, and adversarial testing to enhance testing procedures and ensure comprehensive test coverage."
    # checking if the request method is POST
    if request.method == 'POST':
        # getting prompt data from the form
        prompt = request.POST.get('prompt')

        prompt = extra_prompt + ' ' + prompt

        openai_command(request, prompt, template, 'Tester')
    # this runs if the request method is GET
    else:
        # this will render when there is no request POST or after every POST request
        return render(request, template)
    
    return render(request, template)


# this is the view for handling errors
def error_handler(request):
    return render(request, '404.html')


# @csrf_exempt
# def webhook(request):
#     # build a request object
#     req = json.loads(request.body)
#     # get action from json
#     # action = req.get('queryResult').get('action')
#     query_input = req.get('queryResult').get('queryText')

#     # message = req['message']

#     # text_input = dialogflow.types.TextInput(text=message, language_code="en-US")
#     # query_input = dialogflow.types.QueryInput(text=text_input)
#     # making a request to the API
#     response = openai.Completion.create(model="text-davinci-003",
#                                         prompt=query_input,
#                                         temperature=0.7,
#                                         max_tokens=150,
#                                         top_p=1,
#                                         n=1,
#                                         frequency_penalty=0,
#                                         presence_penalty=0.6)
#     # formatting the response input
#     formatted_response = response['choices'][0]['text']
#     # bundling everything in the context
#     context = {
#         'formatted_response': formatted_response,
#         'prompt': prompt
#     }
    
    
#     # return a fulfillment message
#     fulfillmentText = {'fulfillmentText': formatted_response}
#     # return response
#     return JsonResponse(fulfillmentText, safe=False)