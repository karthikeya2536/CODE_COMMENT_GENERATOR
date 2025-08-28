import streamlit as st
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

st.set_page_config(layout="wide")

st.title("Code Comment Generator")

@st.cache_resource
def load_model():
    bnb_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.bfloat16
    )

    device = "cuda" if torch.cuda.is_available() else "cpu"

    model_name = "edumunozsala/llama-2-7b-int4-python-code-20k"

    tokenizer = AutoTokenizer.from_pretrained(model_name)

    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
        device_map="auto"
    )
    return tokenizer, model, device

tokenizer, model, device = load_model()

code_input = st.text_area("Enter your Python code here:", height=300)

if st.button("Generate Comments"):
    if code_input:
        with st.spinner("Generating comments..."):
            prompt = f"""### Instruction:
Generate the following python code with inline comments where needed.

### Input:
{code_input}

### Response:
"""

            inputs = tokenizer(prompt, return_tensors="pt", truncation=True, max_length=2048).to(device)

            outputs = model.generate(
                **inputs,
                max_new_tokens=512,
                do_sample=True,
                top_p=0.9,
                temperature=0.7,
                eos_token_id=tokenizer.eos_token_id
            )

            result = tokenizer.decode(outputs[0], skip_special_tokens=True)
            st.code(result.split("### Response:")[-1].strip(), language="python")
    else:
        st.warning("Please enter some code to generate comments.")
