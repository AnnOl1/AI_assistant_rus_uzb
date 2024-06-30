from openai import OpenAI
import keys

MODEL = "gpt-3.5-turbo"

client_openai = OpenAI(api_key=keys.OPEN_AI)

def create_answer(phrase):
  completion = client_openai.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": "Разговаривай как ассистент цифрового киоска. Задавай вопросы по тексту сообщения. \
     Учитывай что сообщение может быть на узбекском или русском языке"},
    {"role": "user", "content": f"{phrase}"}])

  print(completion.choices[0].message.content)
  return completion.choices[0].message.content