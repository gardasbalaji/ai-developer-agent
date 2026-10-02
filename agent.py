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

# ===========================================================================
# Switching to the local llms throuh ollama
# import ollama
# def main():
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() == "exit":
#             print("Agent: Goodbye!")
#             break
#         try:
#             response = ollama.chat(
#                 model="qwen3:4b",
#                 messages=[
#                     {
#                         "role": "user",
#                         "content": user_input
#                     }
#                 ]
#             )
#             print("\nAgent:", response["message"]["content"])
#         except Exception as e:
#             print("\nAgent: Something went wrong.")
#             print("Error:", e)
# if __name__ == "__main__":
#     main()

# ===========================================================================

# Connecting the llm and the tools
# import ollama
# from tools.file_tools import create_file, read_file, list_files
# def main():
#     tools = [
#         create_file,
#         read_file,
#         list_files
#     ]
#     messages = []
#     while True:
#         user_input = input("\nYou: ")
#         if user_input.lower() == "exit":
#             print("Agent: Goodbye!")
#             break
#         messages.append({
#             "role": "user",
#             "content": user_input
#         })
#         try:
#             response = ollama.chat(
#                 model="qwen3:4b",
#                 messages=messages,
#                 tools=tools
#             )
#             # Add the LLM response to conversation history
#             messages.append(response["message"])
#             # Check whether the LLM requested a tool
#             if response["message"].get("tool_calls"):
#                 for tool_call in response["message"]["tool_calls"]:
#                     function_name = tool_call["function"]["name"]
#                     arguments = tool_call["function"]["arguments"]
#                     print(f"\n[Agent wants to use tool: {function_name}]")
#                     # Execute the requested tool
#                     if function_name == "create_file":
#                         result = create_file(
#                             arguments["filename"],
#                             arguments["content"]
#                         )
#                     elif function_name == "read_file":
#                         result = read_file(
#                             arguments["filename"]
#                         )
#                     elif function_name == "list_files":
#                         result = list_files()
#                     else:
#                         result = "Error: Unknown tool."
#                     print(f"[Tool result: {result}]")
#                     # Send tool result back to the LLM
#                     messages.append({
#                         "role": "tool",
#                         "content": result
#                     })
#                 # Ask LLM to produce final response
#                 final_response = ollama.chat(
#                     model="qwen3:4b",
#                     messages=messages,
#                     tools=tools
#                 )

#                 messages.append(final_response["message"])
#                 print("\nAgent:", final_response["message"]["content"])
#             else:
#                 print("\nAgent:", response["message"]["content"])
#         except Exception as e:
#             print("\nAgent: Something went wrong.")
#             print("Error:", e)
# if __name__ == "__main__":
#     main()

# ===========================================================================

# making agent work as a loop
import ollama
from tools.file_tools import create_file, read_file, list_files
def main():
    # All tools available to the agent
    tools = [
        create_file,
        read_file,
        list_files
    ]
    # Map tool names to actual Python functions
    tool_functions = {
        "create_file": create_file,
        "read_file": read_file,
        "list_files": list_files
    }
    messages = []
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == "exit":
            print("Agent: Goodbye!")
            break
        messages.append({
            "role": "user",
            "content": user_input
        })
        try:
            # Keep asking the LLM what to do until it gives a final answer
            while True:
                response = ollama.chat(
                    model="qwen3:4b",
                    messages=messages,
                    tools=tools
                )
                assistant_message = response["message"]
                # Save the LLM's response to conversation history
                messages.append(assistant_message)
                # --------------------------------
                # CASE 1: LLM wants to use a tool
                # --------------------------------
                if assistant_message.get("tool_calls"):
                    for tool_call in assistant_message["tool_calls"]:
                        function_name = tool_call["function"]["name"]
                        arguments = tool_call["function"]["arguments"]
                        print(
                            f"\n[Agent wants to use tool: {function_name}]"
                        )
                        # Find the actual Python function
                        function = tool_functions.get(function_name)
                        if function is None:
                            result = f"Error: Unknown tool '{function_name}'."
                        else:
                            # Execute the tool
                            result = function(**arguments)
                        print(f"[Tool result: {result}]")
                        # Give the tool result back to the LLM
                        messages.append({
                            "role": "tool",
                            "content": result
                        })
                    # Continue the loop.
                    #
                    # The LLM now sees the tool result and
                    # decides what to do next.
                    continue
                # --------------------------------
                # CASE 2: LLM has final answer
                # --------------------------------
                print("\nAgent:", assistant_message["content"])
                break
        except Exception as e:
            print("\nAgent: Something went wrong.")
            print("Error:", e)
if __name__ == "__main__":
    main()