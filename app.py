# Import third party library
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi import File, UploadFile, HTTPException

# Import core library
from time import time

# Import Local functions
from utilis import extract_data_from_pdf, validate_response, response_concate, verify_response
from logger_file import log_func
logger = log_func()

app = FastAPI(title="Invoice Processor", description="upload pdf file of the invoice and it will return the json of the fields.")

#middleware
origins = ["http://localhost", "http://localhost:8080", "http://localhost:8000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# route
@app.post("/Invoice_reader", description="Upload pdf here", name= "API for Upload Invoice PDF")
def data_extractor(file : UploadFile = File(...)) -> JSONResponse:
    """
    This Function calls different function.
    First convert pdf to image.
    then process image to byte format to load in llm.
    feed the image to llm and get response in form JSON.
    Function returns JSON response.
    """
    try:
        if file.filename.endswith(".pdf"):
            response, time_token, img = extract_data_from_pdf(f"Payout/{file.filename}")
            validated_response, invalidated_field = validate_response(response)
            print(time_token)
            
            logger.info(f"Data Extracted from {file.filename}. Time and Token {str(time_token)} \n {invalidated_field} fields are invalid.")
            if "Invalid Image" in response:
                return JSONResponse(status_code=400, content="Give PDF of Invoice")
            
            if len(invalidated_field) != 0:
                try:              
                    answer, keys, time_token_second_inference = verify_response(image=img, empty_keys=invalidated_field)
                    print("LLM usage:-", time_token_second_inference)
                    validated_answer, _ = validate_response(answer)
                    final = response_concate(final=validated_response,answer=validated_answer)            
                    # validated_final = validate_response(final)
                    logger.info(f"{keys} are Extracted from image as it was invalid in first attempt. Time and Token used {str(time_token_second_inference)}")
                    return JSONResponse(status_code=200, content=final)
                except Exception as e:
                    logger.error(f"Error:- {str(e)} ocurred while reExtracting Invalide data from {file.filename}.")
                    return JSONResponse(status_code=200, content=validated_response) 
            else:
                return JSONResponse(status_code=200, content=validated_response)
                       
        else: 
            logger.error(f"Invalid File Given. filename:- {file.filename}")
            return JSONResponse(status_code=400, content="Give PDF file, Given file does not support.")
    except HTTPException as h:
        logger.error(f"{str(h)}")
        return JSONResponse(status_code=h.status_code, content=f"{str(h)} Error Occurred")
    except Exception as e:
        logger.error(f"Error:- {str(e)} ocurred while extracting data from {file.filename}.")
        return JSONResponse(status_code=500, content="Error:- something went wrong")


# {
#   "id": "chatcmpl-f51b2cd2-bef7-417e-964e-a08f0b513c22",
#   "object": "chat.completion",
#   "created": 1730241104,
#   "model": "llama3-8b-8192",
#   "choices": [
#     {
#       "index": 0,
#       "message": {
#         "role": "assistant",
#         "content": "Fast language models have gained significant attention in recent years due to their ability to process and generate human-like text quickly and efficiently. The importance of fast language models can be understood from their potential applications and benefits:\n\n1. **Real-time Chatbots and Conversational Interfaces**: Fast language models enable the development of chatbots and conversational interfaces that can respond promptly to user queries, making them more engaging and useful.\n2. **Sentiment Analysis and Opinion Mining**: Fast language models can quickly analyze text data to identify sentiments, opinions, and emotions, allowing for improved customer service, market research, and opinion mining.\n3. **Language Translation and Localization**: Fast language models can quickly translate text between languages, facilitating global communication and enabling businesses to reach a broader audience.\n4. **Text Summarization and Generation**: Fast language models can summarize long documents or even generate new text on a given topic, improving information retrieval and processing efficiency.\n5. **Named Entity Recognition and Information Extraction**: Fast language models can rapidly recognize and extract specific entities, such as names, locations, and organizations, from unstructured text data.\n6. **Recommendation Systems**: Fast language models can analyze large amounts of text data to personalize product recommendations, improve customer experience, and increase sales.\n7. **Content Generation for Social Media**: Fast language models can quickly generate engaging content for social media platforms, helping businesses maintain a consistent online presence and increasing their online visibility.\n8. **Sentiment Analysis for Stock Market Analysis**: Fast language models can quickly analyze social media posts, news articles, and other text data to identify sentiment trends, enabling financial analysts to make more informed investment decisions.\n9. **Language Learning and Education**: Fast language models can provide instant feedback and adaptive language learning, making language education more effective and engaging.\n10. **Domain-Specific Knowledge Extraction**: Fast language models can quickly extract relevant information from vast amounts of text data, enabling domain experts to focus on high-level decision-making rather than manual information gathering.\n\nThe benefits of fast language models include:\n\n* **Increased Efficiency**: Fast language models can process large amounts of text data quickly, reducing the time and effort required for tasks such as sentiment analysis, entity recognition, and text summarization.\n* **Improved Accuracy**: Fast language models can analyze and learn from large datasets, leading to more accurate results and more informed decision-making.\n* **Enhanced User Experience**: Fast language models can enable real-time interactions, personalized recommendations, and timely responses, improving the overall user experience.\n* **Cost Savings**: Fast language models can automate many tasks, reducing the need for manual labor and minimizing costs associated with data processing and analysis.\n\nIn summary, fast language models have the potential to transform various industries and applications by providing fast, accurate, and efficient language processing capabilities."
#       },
#       "logprobs": null,
#       "finish_reason": "stop"
#     }
#   ],
#   "usage": {
#     "queue_time": 0.037493756,
#     "prompt_tokens": 18,
#     "prompt_time": 0.000680594,
#     "completion_tokens": 556,
#     "completion_time": 0.463333333,
#     "total_tokens": 574,
#     "total_time": 0.464013927
#   },
#   "system_fingerprint": "fp_179b0f92c9",
#   "x_groq": { "id": "req_01jbd6g2qdfw2adyrt2az8hz4w" }
# }