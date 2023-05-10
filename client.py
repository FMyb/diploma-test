#%pip install grpcio

import grpc
import bidirectional_pb2_grpc
import bidirectional_pb2

host = "158.160.4.227"
channel = grpc.insecure_channel(target=f"{host}:50051")
stub = bidirectional_pb2_grpc.ChatServerStub(channel)
stream = stub.ChatStream(bidirectional_pb2.Empty())
note = bidirectional_pb2.Note()
note.name = 'test'
note.message = 'test'
r = stub.SendNote(note)
print(r)
for x in stream:
    print(x)
