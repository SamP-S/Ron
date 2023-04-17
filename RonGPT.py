import openai

class Ron:
    def __init__(self):
        # initialise gpt
        openai.api_key = "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"
        self.messages = []
        self.responses = []
        self.messages.append({"role":"system","content":"chatbot"})


    def send_gpt(self, message):
        print("ChatGPT: asking gpt")
        # adds message to transcript
        self.messages.append({"role":"user","content": message})
        # sends message to gpt
        self.response=openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=self.messages
        )
        # parse return and return
        self.reply = self.response["choices"][0]["message"]["content"]
        print("ChatGPT: got response")
        return self.reply


if __name__ == "__main__":
    ron = Ron()
    while True:
        message = input("User: ")
        if message == "exit":
            break
        
        reply = ron.send_gpt(message)
        print("AI: " + reply)
    print("finished")