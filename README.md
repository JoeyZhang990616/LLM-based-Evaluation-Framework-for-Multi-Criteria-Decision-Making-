# LLM BASED EVALUATION FRAMEWORK FOR MULTI CRITERIA DECISION MAKING

## INSTALLING DEPENDENCIES
openai==0.28.0  
pandas==2.1.4  
scikit-learn==1.5.2  

## MODEL AND API CONFIGURATION
You can replace the default model and API key configuration to work with different models or APIs. Here's an example of how to set up the model and API key for OpenAI GPT-3.5, and how to modify it if you want to use a different model.

## RUNNING THE SCRIPTS
### STEP 1: RUN LLMS-MCDM.PY
This script is responsible for setting up the MCDM tasks and running the initial evaluation using different LLMs. It prepares the data for further analysis.

### STEP 2: RUN EVALUATION.PY
Once Llms-MCDM.py has been executed, you can proceed to run evaluation.py to compare the results of the LLMs with human evaluations. This script loads the results from Llms-MCDM.py and evaluates the models' accuracy by comparing them with human-provided ground truth.
