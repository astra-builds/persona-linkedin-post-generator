from few_shot import FewShotPosts
from llm_helper import llm
from langchain_core.prompts import PromptTemplate

PERSONA = (
    "You are an authentic AI learner who shares honest struggles, small wins, "
    "and real emotions about the learning journey. Your tone is humble, relatable, "
    "and slightly reflective — never bragging or overly technical."
)

def get_user_input(prompt_text, options=None):
    while True:
        val = input(prompt_text).strip().lower()
        if not options or val in options:
            return val
        print(f"Please choose from: {', '.join(options)}")

def build_prompt(topic, language, examples):
    example_section = ""
    if examples:
        example_section = "Here are some examples of my previous posts for style reference:\n\n" + \
            "\n---\n".join(f"Example {i+1}:\n{ex}" for i, ex in enumerate(examples)) + "\n\n"

    instructions = "Write a LinkedIn post in first-person about the given topic."
    if language and language != "any":
        instructions += f" Write it in {language.capitalize()}."
    instructions += "\nReturn ONLY valid JSON with a single key 'text' containing the post."

    return f"""{PERSONA}

{example_section}{instructions}

Topic: {topic}"""

def main():
    print("=" * 50)
    print("  LinkedIn Post Generator")
    print("=" * 50)

    topic = input("\nWhat do you want to post about? ").strip()
    language = get_user_input("\nLanguage (english / any): ", {"english", "any"})
    length = get_user_input("\nLength (short / medium / long / any): ",
                            {"short", "medium", "long", "any"})
    tag = get_user_input("\nTag (AI / Learning / Motivation / Progress / any): ",
                         {"ai", "learning", "motivation", "progress", "any"})

    if tag == "any":
        tag = None

    fsp = FewShotPosts()
    examples = fsp.get_few_shots(length=length if length != "any" else None,
                                  language=language if language != "any" else None,
                                  tag=tag)

    prompt = build_prompt(topic, language, examples)

    template = PromptTemplate.from_template("{prompt}")
    chain = template | llm
    response = chain.invoke(input={"prompt": prompt})

    import json
    try:
        result = json.loads(response.content)
        print("\n" + "=" * 50)
        print("  Generated Post")
        print("=" * 50)
        print(result.get("text", response.content))
    except json.JSONDecodeError:
        print("\n" + "=" * 50)
        print("  Generated Post")
        print("=" * 50)
        print(response.content)

if __name__ == "__main__":
    main()
