import 'package:flutter/material.dart';
import 'package:joystick/joystick.dart';
import 'package:http/http.dart' as http;

class ManualMode extends StatefulWidget {
  const ManualMode({Key? key}) : super(key: key);

  @override
  State<ManualMode> createState() => _ManualModeState();
}

String scannedData = 'Waiting...';

class _ManualModeState extends State<ManualMode> {
  Future<void> getData() async {
    while (true) {
      var url = Uri.parse('http://192.168.43.191:8000/GetScannedNum/');
      var response = await http.get(url);
      scannedData = response.body;
      setState(() {});
    }
  }

  @override
  Widget build(BuildContext context) {
    double height = MediaQuery.of(context).size.height;
    double width = MediaQuery.of(context).size.width;
    return Stack(
      children: [
        Column(
          children: [
            Container(
                alignment: Alignment.center,
                height: height * 0.4,
                width: double.infinity,
                child: Text(scannedData, style: TextStyle(fontSize: 20)),
                color: Colors.amber.shade100),
            ElevatedButton(
              onPressed: (() {
                var url =
                    Uri.parse('http://192.168.43.191:8000/PostDirection/');
                http.post(url, body: {'direction': 's'});
              }),
              child: Text('STOP'),
            ),
          ],
        ),
        Container(
          height: height,
          width: width * 0.8,
          child: Joystick(
            size: 210,
            isDraggable: true,
            backgroundColor: Color.fromARGB(255, 187, 159, 236),
            joystickMode: JoystickModes.all,
            onUpPressed: () {
              var url = Uri.parse('http://192.168.43.191:8000/PostDirection/');
              http.post(url, body: {'direction': 'f'});
            },
            onDownPressed: () {
              var url = Uri.parse('http://192.168.43.191:8000/PostDirection/');
              http.post(url, body: {'direction': 'b'});
            },
            onLeftPressed: () {
              var url = Uri.parse('http://192.168.43.191:8000/PostDirection/');
              http.post(url, body: {'direction': 'l'});
            },
            onRightPressed: () {
              var url = Uri.parse('http://192.168.43.191:8000/PostDirection/');
              http.post(url, body: {'direction': 'r'});
            },
          ),
        ),
      ],
    );
  }
}
