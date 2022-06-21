import 'dart:async';

import 'package:camera/camera.dart';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class AutomaticMode extends StatefulWidget {
  List<CameraDescription>? cameras;
  AutomaticMode({
    Key? key,
    required this.cameras,
  }) : super(key: key);

  @override
  AutomaticModeState createState() => AutomaticModeState();
}

class AutomaticModeState extends State<AutomaticMode> {
  late CameraController _controller;
  late Future<void> _initializeControllerFuture;

  @override
  void initState() {
    super.initState();
    // To display the current output from the Camera,
    _controller = CameraController(
      // Get a specific camera from the list of available cameras.
      widget.cameras![0],
      // Define the resolution to use.
      ResolutionPreset.medium,
    );
    // Next, initialize the controller. This returns a Future.
    _initializeControllerFuture = _controller.initialize();
  }

  @override
  void dispose() {
    // Dispose of the controller when the widget is disposed.
    _controller.dispose();
    super.dispose();
  }

  late XFile image;
  Future<XFile> captureImages() async {
    image = await _controller.takePicture();
    print(image);
    return image;
  }

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;
    return Column(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: <Widget>[
        // If the Future is complete, display the preview.
        _controller.value.isInitialized
            ? Container(
                height: height * 0.75, child: CameraPreview(_controller))
            : Center(child: CircularProgressIndicator()),
        Container(
          // height: height*0.5,
          child: ElevatedButton(
            // Provide an onPressed callback.
            onPressed: () async {
              // Take the Picture in a try / catch block. If anything goes wrong,
              // catch the error.
              await _initializeControllerFuture;
              var uri = Uri.parse('http://192.168.43.191:8000/fileUploadApi/');
              const duration = Duration(milliseconds: 500);
              try {
                Timer.periodic(duration, (Timer t) async {
                  XFile imageFile = await captureImages();
                  var imageName = imageFile.path;
                  var request = http.MultipartRequest('POST', uri);
                  request.files.add(await http.MultipartFile.fromPath(
                      'file_uploaded', imageName));
                  // await Future.delayed(Duration(seconds: 5));
                  var response = await request.send();
                });
              } catch (e) {
                // If an error occurs, log the error to the console.
                print(e);
              }
            },
            child: const Text("LET'S GO"),
          ),
        ),
      ], // floatingActionButton:
    );
  }
}
