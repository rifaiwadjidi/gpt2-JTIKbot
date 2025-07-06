import gradio as gr
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("rifaiwadjidi/gpt2-JTIKbot")
tokenizer = AutoTokenizer.from_pretrained("rifaiwadjidi/gpt2-JTIKbot")

def chat(prompt):
    inputs = tokenizer.encode(prompt, return_tensors="pt")
    outputs = model.generate(inputs, max_length=200, pad_token_id=tokenizer.eos_token_id)
    reply = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return reply[len(prompt):]

gr.Interface(fn=chat, inputs="text", outputs="text").launch()
