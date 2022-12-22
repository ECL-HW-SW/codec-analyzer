from HttpContent import HttpContent
import json

http = HttpContent("http://localhost:8080/api/codec-database")

# print(http.POST())

print(http.GET())