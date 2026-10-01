# When we want to use the gemini api, but it is not responding properly 
# from google import genai
# from config import GEMINI_API_KEY

# client = genai.Client(api_key=GEMINI_API_KEY)
# chat = client.chats.create(
#     model="gemini-3.8-flash"
# )
# def main():
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() == "exit":
#             print("Agent: Goodbye!")
#             break
#         response = chat.send_message(user_input)
#         print("\nAgent:", response.text)
# if __name__ == "__main__":
#     main()

# Switching to the local llms throuh ollama
import ollama
def main():
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break
        try:
            response = ollama.chat(
                model="qwen3:4b",
                messages=[
                    {
                        "role": "user",
                        "content": user_input
                    }
                ]
            )
            print("\nAgent:", response["message"]["content"])
        except Exception as e:
            print("\nAgent: Something went wrong.")
            print("Error:", e)
if __name__ == "__main__":
    main()