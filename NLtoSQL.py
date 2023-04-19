# Importing required packages
import openai
import os
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Setting up Azure Key Vault connection
KVUri = f"https://openaibot-kv.vault.azure.net/"
credential = DefaultAzureCredential()
client = SecretClient(vault_url=KVUri, credential=credential)

# Setting API Key and API endpoint for OpenAI
openai.api_key = client.get_secret("NLtoSQL-openai").value
openai.api_type = "azure"
openai.api_base = "https://openaibot-aoai.openai.azure.com/"
openai.api_version = "2022-12-01"

deployment_engine = "text-davinci-003"

response = openai.Completion.create(
  engine= deployment_engine,
  prompt="### Postgres SQL tables, with their properties:\n#\n# Employee(id, name, department_id)\n# Department(id, name, address)\n# Salary_Payments(id, employee_id, amount, date)\n#\n### A query to list the names of the departments which employed more than 10 employees in the last 3 months\n\nSELECT",
  temperature=0,
  max_tokens=150,
  top_p=1,
  frequency_penalty=0,
  presence_penalty=0,
  best_of=1,
  stop=["#",";"])

print(response['choices'][0]['text'])