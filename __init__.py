import json

import requests

from custom_nodes.DTGlobalVariables import variables
from custom_nodes.DTPromptAgent import config


class DTPromptAgentString:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), "clip": ("CLIP", )}}
    RETURN_TYPES = ("STRING","CLIP")
    FUNCTION = "encode"

    CATEGORY = "DoubTech/Agents"


    @classmethod
    def IS_CHANGED(s, text):
        return True

    def encode(self,  text, clip):
        text = variables.apply(text)
        # Request a prompt from the prompt agent rest api
        response = requests.get("https://api.aiart.doubtech.com/gpt/agent", params={"key": config.agent_key, "prompt": text})

        # Get the first item from content
        # ex response: {"content":"[\"A lone astronaut floats above a breathtaking view of Earth. {tag:astronaut}{tag:space}{tag:Earth}\"]"}

        try:
            response = response.json()
            try:
                prompt = json.loads(response["content"])[0]
            except:
                prompt = response["content"]
        except Exception as e:
            print(e)
            prompt = text

        print("Generated prompt: " + prompt)

        # Strip out anything wrapped by {tag:...} and create a list of tags from them
        tags = []
        while "{tag:" in prompt:
            start = prompt.index("{tag:")
            end = prompt.index("}", start)
            tag = prompt[start+5:end]
            tags.append(tag)
            prompt = prompt[:start] + prompt[end+1:]

        if "tags" not in variables.state:
            # Convert the list into a comma separated string
            stags = ",".join(tags)
            # Set the tags variable
            variables.state["tags"] = stags
        else:
            # Split the tags variable into a list, don't keep empty strings
            current_tags = variables.state["tags"].split(",")
            current_tags = [t for t in current_tags if t != ""]
            # Merge the two lists
            variables.state["tags"] = ",".join(list(set(current_tags + tags)))

        variables.state["prompt"] = prompt
        variables.generated_prompt = prompt
        print("Output prompt: " + prompt)
        return (prompt,clip)

class DTPromptAgent:
    @classmethod
    def INPUT_TYPES(s):
        return {"required": {"text": ("STRING", {"multiline": True}), "clip": ("CLIP", )}}
    RETURN_TYPES = ("CONDITIONING",)
    FUNCTION = "encode"

    CATEGORY = "DoubTech/Conditioning"


    @classmethod
    def IS_CHANGED(s, clip, text):
        return True

    def encode(self, clip, text):
        text = variables.apply(text)
        # Request a prompt from the prompt agent rest api
        # ex: https://api.aiart.doubtech.com/gpt/agent?key=40abb6c8-d2f4-4f97-9449-72b65ff1158d&prompt=create%20a%20random%20space%20prompt
        response = requests.get("https://api.aiart.doubtech.com/gpt/agent", params={"key": "c52b8649-600a-48d5-b43a-7407383c992e", "prompt": text})

        # Get the first item from content
        # ex response: {"content":"[\"A lone astronaut floats above a breathtaking view of Earth. {tag:astronaut}{tag:space}{tag:Earth}\"]"}

        try:
            response = response.json()
            try:
                prompt = json.loads(response["content"])[0]
            except:
                prompt = response["content"]
        except Exception as e:
            print(e)
            prompt = text

        print("Generated prompt: " + prompt)

        # Strip out anything wrapped by {tag:...} and create a list of tags from them
        tags = []
        while "{tag:" in prompt:
            start = prompt.index("{tag:")
            end = prompt.index("}", start)
            tag = prompt[start+5:end]
            tags.append(tag)
            prompt = prompt[:start] + prompt[end+1:]

        if "tags" not in variables.state:
            # Convert the list into a comma separated string
            stags = ",".join(tags)
            # Set the tags variable
            variables.state["tags"] = stags
        else:
            # Split the tags variable into a list, don't keep empty strings
            current_tags = variables.state["tags"].split(",")
            current_tags = [t for t in current_tags if t != ""]
            # Merge the two lists
            variables.state["tags"] = ",".join(list(set(current_tags + tags)))

        variables.state["prompt"] = prompt
        variables.generated_prompt = prompt
        return ([[clip.encode(prompt), {}]], )


# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "DTPromptAgent": DTPromptAgent,
    "DTPromptAgentString": DTPromptAgentString
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "DTPromptAgent": "Prompt Agent",
    "DTPromptAgentString": "Prompt Agent (String)"
}
