"""Dr. Pet - AI Veterinary Chatbot for PawCare (Powered by Groq)"""
GROQ_API_KEY = "secret key"

import base64
import requests
import json


class DrPetChatbot:
    def __init__(self, pet_name, pet_type, breed, pet_dob, owner_name):
        self.pet_name = pet_name
        self.pet_type = pet_type
        self.breed = breed
        self.pet_dob = pet_dob
        self.owner_name = owner_name
        self.conversation_history = []
        self.model = "llama-3.3-70b-versatile"
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def get_system_prompt(self):
        return f"""You are Dr. Pet, a friendly and knowledgeable AI veterinary assistant inside the PawCare app.

You are talking to {self.owner_name}, the loving owner of a {self.pet_type} named {self.pet_name} (Breed: {self.breed}, Date of Birth: {self.pet_dob}).

Your role:
- Provide helpful, caring, and accurate pet health advice
- Answer questions about symptoms, diet, nutrition, behaviour, grooming, and general care
- Give breed-specific tips when relevant
- Provide emergency guidance and always recommend visiting a real vet for serious issues
- Be warm, friendly, and reassuring like a trusted vet friend
- When analyzing photos, assess: skin/fur condition, visible wounds or injuries, body condition and weight, and general health observations

Strict rules:
- Always refer to the pet by name ({self.pet_name}) to make responses personal
- Keep responses concise and easy to read (3-5 sentences max unless detail is truly needed)
- Use plain text — no markdown asterisks, no bullet symbols, no headers
- For emergencies (difficulty breathing, seizures, poisoning, severe bleeding), ALWAYS say to visit a vet immediately
- Never diagnose definitively — always recommend a vet visit for serious concerns
- Be warm and empathetic, especially if the owner seems worried
- When analyzing an image, clearly note what you observe and what you cannot determine from a photo alone

When you receive a photo, cover these points naturally in plain text:
1. What you observe (appearance, coat, visible body condition)
2. Any concerns or reassurances
3. Whether a vet visit is recommended

You are not a replacement for a real veterinarian. Always remind the owner to consult a vet for serious medical issues."""

    def chat(self, user_message, image_data=None, image_media_type=None):
        """Send a message (with optional image) to Dr. Pet and get a response"""

        try:
            # Build the user message content
            if image_data:
                content = [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{image_media_type or 'image/jpeg'};base64,{image_data}"
                        }
                    },
                    {
                        "type": "text",
                        "text": user_message if user_message else (
                            f"Please analyze this photo of {self.pet_name} and share your observations "
                            f"about their skin/fur condition, any wounds or injuries, body condition, and general health."
                        )
                    }
                ]
                model = "meta-llama/llama-4-scout-17b-16e-instruct"  # vision model for images
            else:
                content = user_message
                model = self.model

            # Add user message to history
            self.conversation_history.append({
                "role": "user",
                "content": content
            })

            # Build messages with system prompt
            messages = [
                {"role": "system", "content": self.get_system_prompt()}
            ] + self.conversation_history

            # Call Groq API
            headers = {
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": model,
                "messages": messages,
                "max_tokens": 1024,
                "temperature": 0.7
            }

            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()

            result = response.json()
            assistant_message = result["choices"][0]["message"]["content"]

            # Save assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })

            return assistant_message

        except Exception as e:
            return f"Sorry, I'm having trouble connecting right now. Please try again in a moment. ({str(e)})"