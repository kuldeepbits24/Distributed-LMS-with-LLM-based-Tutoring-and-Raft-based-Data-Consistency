import grpc
from concurrent import futures
import tutoring_pb2
import tutoring_pb2_grpc
import logging
import cohere 
co = cohere.ClientV2("9rZaWYoS4JsQMcOMZjozd66X0DqbStcRVe8LimVQ")
logging.basicConfig(level=logging.INFO)

# Function to get response from the Cohere model
def generate_gpt2_response(query):
    # Using co.chat() API with the "command-r-plus" model
    response = co.chat(
        model="command-r-plus", 
        messages=[{"role": "user", "content": query}]
    )
    
    # Extract the content from the response object correctly
 
    return (response.message.content[0].text)
    

class TutoringServer(tutoring_pb2_grpc.TutoringServicer):
    def GetLLMAnswer(self, request, context):
        logging.info(f"Received tutoring request: {request.query}")
        # Get response using Cohere's chat model
        answer = generate_gpt2_response(request.query)
        return tutoring_pb2.GetLLMAnswerResponse(success=True, answer=answer)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    tutoring_pb2_grpc.add_TutoringServicer_to_server(TutoringServer(), server)
    server.add_insecure_port('172.20.10.5:50052')
    logging.info("Tutoring server running on port 50052")
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
