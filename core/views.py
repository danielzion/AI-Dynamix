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
    context = {}
    # checking if the request method is POST
    if request.method == 'POST':
        # getting prompt data from the form
        prompt = request.POST.get('prompt')

        client = openai.OpenAI()
        client.api_key = config("OPENAI_KEY")

        response = client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[
                {
                    "role": "system",
                    "content": "You will be provided with related pieces of Python code, and your task is to write unit tests for it wherever possible. Infer the purpose of the code as best as you can."
                },
                {
                    "role": "user",
                    "content": "```py\nfrom math_operations import add, subtract\nfrom string_operations import reverse_string\n\ndef main():\n    # Example usage of imported functions\n    result_add = add(5, 3)\n    result_subtract = subtract(10, 4)\n    reversed_string = reverse_string(\"hello\")\n\n    print(\"Addition result:\", result_add)\n    print(\"Subtraction result:\", result_subtract)\n    print(\"Reversed string:\", reversed_string)\n\nif __name__ == \"__main__\":\n    main()\n\n```\n\n```py\ndef reverse_string(s):\n    return s[::-1]\n\ndef concatenate_strings(s1, s2):\n    return s1 + s2\n\n```\n\n```py\ndef add(a, b):\n    return a + b\n\ndef subtract(a, b):\n    return a - b\n\ndef multiply(a, b):\n    return a * b\n\ndef divide(a, b):\n    if b == 0:\n        raise ValueError(\"Cannot divide by zero\")\n    return a / b\n\n```"
                },
                {
                    "role": "assistant",
                    "content": "The provided Python code consists of several functions that perform basic mathematical operations (addition, subtraction, multiplication, and division) and string operations (reversing a string and concatenating two strings). \n\nHere are the unit tests for these functions:\n\n```py\nimport unittest\nfrom math_operations import add, subtract, multiply, divide\nfrom string_operations import reverse_string, concatenate_strings\n\nclass TestMathOperations(unittest.TestCase):\n    def test_add(self):\n        self.assertEqual(add(5, 3), 8)\n        self.assertEqual(add(-1, 1), 0)\n        self.assertEqual(add(0, 0), 0)\n\n    def test_subtract(self):\n        self.assertEqual(subtract(10, 4), 6)\n        self.assertEqual(subtract(-1, 1), -2)\n        self.assertEqual(subtract(0, 0), 0)\n\n    def test_multiply(self):\n        self.assertEqual(multiply(5, 3), 15)\n        self.assertEqual(multiply(-1, 1), -1)\n        self.assertEqual(multiply(0, 0), 0)\n\n    def test_divide(self):\n        self.assertEqual(divide(10, 2), 5)\n        self.assertEqual(divide(-1, 1), -1)\n        with self.assertRaises(ValueError):\n            divide(10, 0)\n\nclass TestStringOperations(unittest.TestCase):\n    def test_reverse_string(self):\n        self.assertEqual(reverse_string(\"hello\"), \"olleh\")\n        self.assertEqual(reverse_string(\"Python\"), \"nohtyP\")\n        self.assertEqual(reverse_string(\"\"), \"\")\n\n    def test_concatenate_strings(self):\n        self.assertEqual(concatenate_strings(\"hello\", \" world\"), \"hello world\")\n        self.assertEqual(concatenate_strings(\"Python\", \" programming\"), \"Python programming\")\n        self.assertEqual(concatenate_strings(\"\", \"\"), \"\")\n\nif __name__ == \"__main__\":\n    unittest.main()\n```\n\nThese tests check the correctness of the functions by comparing the actual output of the functions with the expected output for a given input."
                },
                {
                    "role": "user",
                    "content": f'```\n{prompt}```'
                }
            ],
            temperature=0,
            max_tokens=1024,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )

        # Add the response to the context
        context['response'] = response
        context['last_message'] = response.choices[0].message.content

    # this runs if the request method is GET
    else:
        code_form = OpenAICommandForm(instance=request.user)

        context['code_form'] = code_form

    return render(request, template, context)

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
