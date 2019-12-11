class Handler:
    def __init__(self, request):
        self.request = request
        self.data = dict(request.params)
        if request.method == "POST":
            if request.content_type == "application/json":
                self.data.update(request.json)
            else:
                self.data.update(request.POST)
        request.add_finished_callback(self.cleanup)
    def cleanup(self, request):
        print("Cleanup!")
