#when your ready for multiple
#Define get_response Function 
def get_response(self, user_input):  
    # i. Check local memory for context  
    context = self.get_context_from_db(user_input)  
      
    try:  
        # ii. Send input + context to OpenAI API  
        response = self.client.chat.completions.create(  
            model="gpt-3.5-turbo",  
            messages=[  
                {"role": "system", "content": context},  
                {"role": "user", "content": user_input}  
            ]  
        )  
        result = response.choices[0].message.content  
          
    except Exception as e:  
        # iii. If API fails, use fallback logic  
        result = self.fallback_response(user_input)  
      
    # iv. Return formatted response  
    self.save_to_db(user_input, context, result)  
    return self.format_response(result)
#end


#Define get_multi_response Function 
async def get_multi_response(self, user_input):  
    # Query multiple LLM APIs concurrently  
    responses = await asyncio.gather(  
        self.query_openai(user_input),  
        self.query_claude(user_input),  
        self.query_llama(user_input),  
        self.query_mistral(user_input),  
        return_exceptions=True  
    )  
      
    # Filter successful responses  
    valid_responses = [r for r in responses if not isinstance(r, Exception)]  
      
    # Aggregate and rank responses  
    best_response = self.select_best_response(valid_responses)  
      
    return self.format_response(best_response)  
  
def select_best_response(self, responses):  
    # Implement logic to score and select best response  
    # Could use factors like: length, confidence, relevance, etc.  
    return max(responses, key=lambda x: self.score_response(x))
#end
