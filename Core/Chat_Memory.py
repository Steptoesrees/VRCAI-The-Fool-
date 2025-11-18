
#import chromadb
import uuid
from datetime import datetime
import json
from Config_Manager import Config_Manager

# class vector_memory():
#     def __init__(self, mem_name):
#         self.client = chromadb.PersistentClient(path="./my_vectors")
#         self.time = datetime.now()
#         self.collection = self.client.get_or_create_collection(
#             name=mem_name
#             )




    
#     def add_memory(self, memory):
#         # Check if memory is important enough to store
#         if not self._check_valid(memory):
#             print(f"Memory not important enough to store: {memory}")
#             return False
            
#         self.collection.add(
#             ids= str(uuid.uuid4()),
#             documents= memory,
#             metadatas= {'time':  str(datetime.now())}
#         )
#         print(f"Memory stored: {memory}")
#         return True
    

#     def _check_valid(self, memory):
#         """
#         Check if a memory is important enough to be stored in long-term memory.
#         Uses LLM to evaluate memory significance based on criteria like:
#         - Personal significance to the user
#         - Emotional content
#         - Practical utility for future conversations
#         - Uniqueness and novelty
#         - Long-term relevance
#         """
#         # Skip very short or trivial memories
#         if len(memory.strip()) < 10:
#             return False
            
#         # Skip common greetings and small talk
#         trivial_patterns = [
#             "hello", "hi", "hey", "how are you", "good morning", "good night",
#             "thanks", "thank you", "bye", "goodbye", "see you", "ok", "okay"
#         ]
        
#         if any(pattern in memory.lower() for pattern in trivial_patterns):
#             return False
            
#         # Use LLM to evaluate memory importance
#         importance_check_prompt = [
#             {
#                 "role": "system",
#                 "content": """You are a memory importance evaluator. Analyze the given memory and determine if it's significant enough to store in long-term memory.
                
#                 Consider these criteria for importance:
#                 1. Personal significance - Does it reveal personal preferences, experiences, or identity?
#                 2. Emotional content - Does it contain strong emotions or meaningful experiences?
#                 3. Practical utility - Could this information be useful in future conversations?
#                 4. Uniqueness - Is this a unique or novel piece of information?
#                 5. Long-term relevance - Will this remain relevant over time?
                
#                 Respond with ONLY "YES" if the memory is important enough to store, or "NO" if it's not significant enough.
#                 Be conservative - only store truly meaningful memories."""
#             },
#             {
#                 "role": "user",
#                 "content": f"Memory to evaluate: {memory}"
#             }
#         ]
        
#         try:
#             from callLLM import call
#             response = call(importance_check_prompt, max_tokens=100, model='meta-llama/llama-3.1-8b-instruct')
#             response = response.strip().upper()
            
#             # Check if response indicates importance
#             if "YES" in response:
#                 return True
#             else:
#                 return False
                
#         except Exception as e:
#             # Fallback: use basic heuristics if LLM call fails
#             print(f"LLM importance check failed: {e}. Using fallback heuristics.")
            
#             # Fallback heuristics for memory importance
#             important_keywords = [
#                 "love", "hate", "favorite", "important", "remember", "never forget",
#                 "experience", "story", "memory", "childhood", "family", "friend",
#                 "dream", "goal", "achievement", "accomplishment", "traumatic",
#                 "emotional", "significant", "meaningful", "preference", "opinion"
#             ]
            
#             # Check for important keywords
#             if any(keyword in memory.lower() for keyword in important_keywords):
#                 return True
                
#             # Check for personal revelations (contains "I" statements with substance)
#             if "i " in memory.lower() and len(memory.split()) > 5:
#                 return True
                
#             return False

#     def _process_memory(self, memory):
#         pass


#     def get_memories(self, input_text, no_of_memories=1, filters={}):
        
#         if filters == {}:
#             results = self.collection.query(
#             query_texts=input_text,
#             n_results=no_of_memories
#             )
#         else:
#             results = self.collection.query(
#             query_texts=input_text,
#             where=filters,
#             n_results=no_of_memories
#             )   

#         print("**GET MEMORIES RESULTS TEST**")
#         print("=")*70
#         print(results)
#         print("-")*70
#         print(results[0])
#         print("=")*70
#         return results




class short_memory():
    def __init__(self, max_history = 30):
        with open('Core/config/vrchat_bot_prompt.md', 'r') as file:
            sys_prompt = file.read()

        self.config = Config_Manager()
        self.memory = [{'role': 'system', 'content': sys_prompt}]
        self.max_history = max_history


    def save_memory(self):
        json_data = self.memory
        try:
            with open("Core/Log/ChatLog.json", "w") as file:
                file.write("")
                file.seek(0)
                json.dump(json_data, file, indent=4) #updates the file
                
        except:
            print("failed to save log")
        

    def add_user_message(self,message):
        self.memory.append({'role': 'user', 'content': message})

    def add_ai_message(self, message):
        self.memory.append({'role': 'assistant', 'content': message})
        self.save_memory()

    def inject_memory(self, memory):
        self.memory.insert(len(self.memory)-2,{'role': 'system', 'content': memory})

    def update_sys_prompt(self):
        try:
            with open("Core/Log/ChatLog.json", "r") as file:
                prompt = file.read()
        except:
            print("prompt update failed")
            return
        
        name = self.config.get("AI.name")
        prompt.replace("{{name}}", name)
        self.memory[0].update({"content": prompt})


    def _trim_memory(self):
        if len(self.memory) > self.max_history:
            self.memory = [self.memory[0] + self.memory[-(self.max_history-1)]] # -(self.max_history - 1) negative indexing = last items, 
                                                                                # so e.g. max history = 30, -(max_history - 1) = -29, gets the last 29 items in the list
                                                                                