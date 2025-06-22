import os
from litellm import completion
from dotenv import load_dotenv


load_dotenv()

def main():
    gemini_api_key = os.getenv("GEMINI_API_KEY")

    if not gemini_api_key:
        print("Error: Api key not found")
        return
    
    user_input = input("Ask anything: ")

    response = completion(
        model = "gemini/gemini-2.0-flash",
        api_key = gemini_api_key,
        messages=[
            {
                "role": "user",
                "content" : user_input,
            }


        ],
        temperature = 0.7,
        max_tokens = 100
    )

    print(response.choices[0].message.content)

    



if __name__ == "__main__":
    main()
