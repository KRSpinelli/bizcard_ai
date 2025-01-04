import base64
import json
import os
from PIL import Image
import tempfile


import gradio as gr
from langchain.chains import TransformChain
from pydantic import BaseModel, Field
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain import globals
from langchain_core.runnables import chain
from langchain_core.output_parsers import JsonOutputParser


class BusinessCardInformation(BaseModel):
    """Relevant contact information for a business card."""

    name: str = Field(description="the name in the picture")
    phone_numbers: list[str] = Field(
        description="list of phone numbers in the picture"
    )
    email: str = Field(description="email in the picture")
    address: str = Field(description="address in the picture")
    role: str = Field(description="role in the picture")
    company: str = Field(description="company in the picture")
    other_info: list[str] = Field(
        description="other information in the picture"
    )


parser = JsonOutputParser(pydantic_object=BusinessCardInformation)


def encode_image(inputs: dict) -> dict:
    """Read an image from a given filepath and encode it as base64."""
    image_path = inputs["image_path"]
    with open(image_path, "rb") as image_file:
        image_base64 = base64.b64encode(image_file.read()).decode("utf-8")
    return {"image_base64": image_base64}


load_image_chain = TransformChain(
    input_variables=["image_path"],
    output_variables=["image_base64"],
    transform=encode_image,
)


@chain
def image_model(inputs: dict) -> str | list[str] | dict:
    """Invoke model with image and prompt."""
    model = ChatOpenAI(temperature=0.5, model="gpt-4o-mini", max_tokens=300)
    image_data = f"data:image/jpeg;base64,{inputs['image_base64']}"
    msg = model.invoke(
        [
            HumanMessage(
                content=[
                    {"type": "text", "text": inputs["prompt"]},
                    {"type": "text", "text": parser.get_format_instructions()},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_data},
                    },
                ]
            )
        ]
    )
    return msg.content


def get_image_information(image_path: str, debug: bool = False) -> dict:
    """Extract contact information from a business card image."""
    if debug:
        globals.set_debug(True)
    vision_prompt = (
        "I want you to extract all of the contact details from this image of "
        "a business card including name, phone numbers, email, address, role, "
        "and company. Put any other information into a field labelled 'other'."
    )
    vision_chain = load_image_chain | image_model | parser
    return vision_chain.invoke(
        {"image_path": f"{image_path}", "prompt": vision_prompt}
    )


def process_image(image: Image.Image) -> str:
    """Process an image to extract contact information."""
    with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as temp_file:
        image.save(temp_file.name)
        temp_file_path = os.path.abspath(temp_file.name)
        image_info_dict = get_image_information(temp_file_path)
        data = json.dumps(image_info_dict)
    return data


def load_test_gui():
    """Load the Gradio interface for testing."""
    iface = gr.Interface(
        fn=process_image,
        inputs=gr.Image(type="pil"),
        outputs=gr.Textbox(label="Extracted Text"),
        title="Bizcard AI Playground",
        description=(
            "Upload an image, and the llm will attempt to extract contact "
            "details."
        ),
    )
    iface.launch()
