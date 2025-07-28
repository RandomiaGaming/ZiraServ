import win32com.client
import os
import threading
import flask

def FormatInput(inputString):
    inputString = "".join([ "." if c in "?!:;" else c for c in inputString ])
    inputString = "".join([ " " if c in "\n\r\t" else c for c in inputString ])
    inputString = "".join([ c if c in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ .\"\'1234567890,()*/-+&%$#@" else "" for c in inputString ])
    inputString = " ".join(inputString.split())
    return inputString

def SpeekToFile(inputString, outputPath):
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    speaker.Rate = 6
    ziraInstalled = False
    for voice in speaker.GetVoices():
        if "zira" in voice.GetDescription().lower():
            speaker.Voice = voice
            ziraInstalled = True
            break
    if not ziraInstalled:
        raise RuntimeError("Microsoft Zira voice is not installed or could not be found.")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    stream.Open(outputPath, 3, False)
    speaker.AudioOutputStream = stream
    speaker.Speak(inputString)
    stream.Close()

InProgressRequest = None

def flaskThreadMain():
    app = flask.Flask(__name__)

    @app.route("/api/speek", methods=["POST"])
    def api_speek():
        global InProgressRequest
        if InProgressRequest != None:
            return "A request is already in progress.",500
        InProgressRequest = flask.request.get_data(as_text=True)
        return "",200

    @app.route("/api/in_request", methods=["POST"])
    def api_query():
        return str(InProgressRequest != None),200

    @app.route("/api/get_audio")
    def api_audio():
        if InProgressRequest != None:
            return "A request is currently modifying that file.",500
        else:
            return flask.send_from_directory(os.getcwd(), "output.wav")

    @app.route("/")
    def serve_file():
        return flask.send_from_directory(os.getcwd(), "index.html")

    app.run(host="0.0.0.0", port=41875) # Port is (('Z' + 'I') << 8) | ('R' + 'A')

flaskThread = threading.Thread(target=flaskThreadMain, daemon=True)
flaskThread.start()

while True:
    if InProgressRequest == None:
        continue
    print("Main thread got new request.")
    requestFormatted = FormatInput(InProgressRequest)
    SpeekToFile(requestFormatted, "output.wav")
    InProgressRequest = None
    print("Request complete.")