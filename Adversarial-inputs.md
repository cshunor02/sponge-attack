# Adversarial input, deceptive input

One of the types of Sponge attacks is Adversarial input, deceptive input. This concept means the scenario where we try to give a seemingly innocent, 
but tricky, confusing prompt to the LLM model that could cause the model to make unexpected, wrong decisions, errors or possibly exhaust the model. 
This type of sponge attack’s goal is to break the LLM model’s reasoning, make bad decisions/outputs or misjudgement. 

# Inputs

We tried out different type of inputs like tricky questions, brain teasers, wrong sentences, random caracterseries, or just pleading the LLM model to do something, that peviously said no for.


# Methology

Every previosly mentioned input was tried out with multiple different LLM models (3-4), to see the differences, and to see the outlying answers.
When we got an outlyingly slow or long answer for a simple but wrong sentence/question, we tied to ask the same question but with correct information, to have a reference point which we are able to compare to.

# Errors

Some deceptive input "killed" some models, so for reproduction purposes, we tried the inputs for multiple different models; and after restarting the whole virtual machine environment (and tried out the model with simple talk) we were able to "kill" the model multiple times.
In this case "killing" an LLM model means, that after the error, it doesn't answer any input, not even in a different new chat, or for a different user. 
The error message for and after "killing a model":

As it was already mentioned we reproduced this multiple times, even after restarting the whole system. This happend to multiple models (3: deepseek, llava, mistral), and we tried it in different days too.
No other user was on the server at the time of the tests, so no other Sponge attack could cause this scenario and interfer with these results.

#Ooutputs, results

