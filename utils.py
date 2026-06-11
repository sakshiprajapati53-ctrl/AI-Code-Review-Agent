import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found")

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.5-flash")


def ask_gemini(prompt, debug=False):

# MOCK MODE

    if debug:

        if "Review code" in prompt:
            return """
            Review Summary

            -> No syntax errors found
            -> Time Complexity: O(n)
            -> Variable naming can be improved
            -> Add edge case handling
            """

        elif "Inject realistic bugs" in prompt:
            return """
            int i = 0;

            while(i <= n){
                cout << arr[i];
                i++;
            }
            """

        elif "Explain bugs" in prompt:
            return """
            Bug: Off-by-One Error

            Why:
            Loop runs one extra iteration.

            Impact:
            Array index goes out of bounds.

            Fix:
            Use i < n instead of i <= n.
            """

        elif "interview" in prompt.lower():
            return """
        1. What is Time Complexity?
        2. Difference between Array and Linked List?
        3. What is Dynamic Programming?
        4. What are Edge Cases?
        """

        elif "Difficulty Score" in prompt:
            return """
            Difficulty Score: 7/10

            Complexity: Medium

            Topics:
            - Arrays
            - Loops
            - Edge Cases
            """

        else:
            return f"""
        MOCK MODE

        Prompt Preview:

        {prompt[:300]}
        """

# REAL GEMINI MODE

    try:

        response = model.generate_content(prompt)

        print("FULL RESPONSE:")
        print(response)

        if hasattr(response, "text") and response.text:
            return response.text

        return "No text returned from Gemini."

    except Exception as e:

        return f"""
Gemini Error:

{str(e)}
"""